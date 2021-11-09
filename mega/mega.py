#!/usr/bin/env python3


from math import ceil
from os import path
from time import time
from json import dumps, loads
from hashlib import pbkdf2_hmac
from logging import getLogger
from random import randint
from binascii import unhexlify
from Crypto.PublicKey import RSA
from Crypto.Util import Counter
from pyrogram.errors.exceptions.bad_request_400 import ExpireDateInvalid
from requests import post
from tenacity import retry, wait_exponential, retry_if_exception_type
from mega.crypto import *
from mega.errors import *

logger = getLogger(__name__)

class Mega:
    def __init__(self, options=None):
        self.schema = 'https'
        self.domain = 'mega.co.nz'
        self.timeout = 160  # max secs to wait for resp from api requests
        self.sid = None
        self.sequence_num = randint(0, 0xFFFFFFFF)
        self.request_id = make_id(10)
        self._trash_folder_node_id = None

        if options is None:
            options = {}
        self.options = options

    def login(self, email=None, password=None):
        self._login_user(email, password)
        self._trash_folder_node_id = self.get_node_by_type(4)[0]
        logger.info('Login complete')
        return self
    
    def _login_user(self, email, password):
        logger.info('Logging in user...')
        email = email.lower()
        get_user_salt_resp = self._api_request({'a': 'us0', 'user': email})
        user_salt = None
        try:
            user_salt = base64_to_a32(get_user_salt_resp['s'])
        except KeyError:
            # v1 user account
            password_aes = prepare_key(str_to_a32(password))
            user_hash = stringhash(email, password_aes)
        else:
            # v2 user account
            pbkdf2_key = pbkdf2_hmac(hash_name='sha512',
                                    password=password.encode(),
                                    salt=a32_to_str(user_salt),
                                    iterations=100000,
                                    dklen=32)
            password_aes = str_to_a32(pbkdf2_key[:16])
            user_hash = base64_url_encode(pbkdf2_key[-16:])
        resp = self._api_request({'a': 'us', 'user': email, 'uh': user_hash})
        if isinstance(resp, int):
            raise RequestError(resp)
        self._login_process(resp, password_aes)

    def _login_process(self, resp, password):
        encrypted_master_key = base64_to_a32(resp['k'])
        self.master_key = decrypt_key(encrypted_master_key, password)
        if 'tsid' in resp:
            tsid = base64_url_decode(resp['tsid'])
            key_encrypted = a32_to_str(
                encrypt_key(str_to_a32(tsid[:16]), self.master_key))
            if key_encrypted == tsid[-16:]:
                self.sid = resp['tsid']
        elif 'csid' in resp:
            encrypted_rsa_private_key = base64_to_a32(resp['privk'])
            rsa_private_key = decrypt_key(encrypted_rsa_private_key,
                                          self.master_key)

            private_key = a32_to_str(rsa_private_key)
            # The private_key contains 4 MPI integers concatenated together.
            rsa_private_key = [0, 0, 0, 0]
            for i in range(4):
                # An MPI integer has a 2-byte header which describes the number
                # of bits in the integer.
                bitlength = (private_key[0] * 256) + private_key[1]
                bytelength = ceil(bitlength / 8)
                # Add 2 bytes to accommodate the MPI header
                bytelength += 2
                rsa_private_key[i] = mpi_to_int(private_key[:bytelength])
                private_key = private_key[bytelength:]

            first_factor_p = rsa_private_key[0]
            second_factor_q = rsa_private_key[1]
            private_exponent_d = rsa_private_key[2]
            # In MEGA's webclient javascript, they assign [3] to a variable
            # called u, but I do not see how it corresponds to pycryptodome's
            # RSA.construct and it does not seem to be necessary.
            rsa_modulus_n = first_factor_p * second_factor_q
            phi = (first_factor_p - 1) * (second_factor_q - 1)
            public_exponent_e = modular_inverse(private_exponent_d, phi)

            rsa_components = (
                rsa_modulus_n,
                public_exponent_e,
                private_exponent_d,
                first_factor_p,
                second_factor_q,
            )
            rsa_decrypter = RSA.construct(rsa_components)

            encrypted_sid = mpi_to_int(base64_url_decode(resp['csid']))

            sid = '%x' % rsa_decrypter._decrypt(encrypted_sid)
            sid = unhexlify('0' + sid if len(sid) % 2 else sid)
            self.sid = base64_url_encode(sid[:43])

    def get_node_by_type(self, type):
        """
        Get a node by it's numeric type id, e.g:
        0: file
        1: dir
        2: special: root cloud drive
        3: special: inbox
        4: special trash bin
        """
        nodes = self.get_files()
        for node in list(nodes.items()):
            if node[1]['t'] == type:
                return node
    
    @retry(retry=retry_if_exception_type(RuntimeError),
           wait=wait_exponential(multiplier=2, min=2, max=60))
    def _api_request(self, data):
        params = {'id': self.sequence_num}
        self.sequence_num += 1

        if self.sid:
            params.update({'sid': self.sid})

        # ensure input data is a list
        if not isinstance(data, list):
            data = [data]

        url = f'{self.schema}://g.api.{self.domain}/cs'
        response = post(
            url,
            params=params,
            data=dumps(data),
            timeout=self.timeout,
        )
        json_resp = loads(response.text)
        try:
            if isinstance(json_resp, list):
                int_resp = json_resp[0] if isinstance(json_resp[0],
                                                      int) else None
            elif isinstance(json_resp, int):
                int_resp = json_resp
        except IndexError:
            int_resp = None
        if int_resp is not None:
            if int_resp == 0:
                return int_resp
            if int_resp == -3:
                msg = 'Request failed, retrying'
                logger.info(msg)
                raise RuntimeError(msg)
            raise RequestError(int_resp)
        return json_resp[0]

    def _init_shared_keys(self, files, shared_keys):
        """
        Init shared key not associated with a user.
        Seems to happen when a folder is shared,
        some files are exchanged and then the
        folder is un-shared.
        Keys are stored in files['s'] and files['ok']
        """
        ok_dict = {}
        for ok_item in files['ok']:
            shared_key = decrypt_key(base64_to_a32(ok_item['k']),
                                     self.master_key)
            ok_dict[ok_item['h']] = shared_key
        for s_item in files['s']:
            if s_item['u'] not in shared_keys:
                shared_keys[s_item['u']] = {}
            if s_item['h'] in ok_dict:
                shared_keys[s_item['u']][s_item['h']] = ok_dict[s_item['h']]
        self.shared_keys = shared_keys
    
    def _process_file(self, file, shared_keys):
        if file['t'] == 0 or file['t'] == 1:
            keys = dict(
                keypart.split(':', 1) for keypart in file['k'].split('/')
                if ':' in keypart)
            uid = file['u']
            key = None
            # my objects
            if uid in keys:
                key = decrypt_key(base64_to_a32(keys[uid]), self.master_key)
            # shared folders
            elif 'su' in file and 'sk' in file and ':' in file['k']:
                shared_key = decrypt_key(base64_to_a32(file['sk']),
                                         self.master_key)
                key = decrypt_key(base64_to_a32(keys[file['h']]), shared_key)
                if file['su'] not in shared_keys:
                    shared_keys[file['su']] = {}
                shared_keys[file['su']][file['h']] = shared_key
            # shared files
            elif file['u'] and file['u'] in shared_keys:
                for hkey in shared_keys[file['u']]:
                    shared_key = shared_keys[file['u']][hkey]
                    if hkey in keys:
                        key = keys[hkey]
                        key = decrypt_key(base64_to_a32(key), shared_key)
                        break
            if file['h'] and file['h'] in shared_keys.get('EXP', ()):
                shared_key = shared_keys['EXP'][file['h']]
                encrypted_key = str_to_a32(
                    base64_url_decode(file['k'].split(':')[-1]))
                key = decrypt_key(encrypted_key, shared_key)
                file['shared_folder_key'] = shared_key
            if key is not None:
                # file
                if file['t'] == 0:
                    k = (key[0] ^ key[4], key[1] ^ key[5], key[2] ^ key[6],
                         key[3] ^ key[7])
                    file['iv'] = key[4:6] + (0, 0)
                    file['meta_mac'] = key[6:8]
                # folder
                else:
                    k = key
                file['key'] = key
                file['k'] = k
                attributes = base64_url_decode(file['a'])
                attributes = decrypt_attr(attributes, k)
                file['a'] = attributes
            # other => wrong object
            elif file['k'] == '':
                file['a'] = False
        elif file['t'] == 2:
            self.root_id = file['h']
            file['a'] = {'n': 'Cloud Drive'}
        elif file['t'] == 3:
            self.inbox_id = file['h']
            file['a'] = {'n': 'Inbox'}
        elif file['t'] == 4:
            self.trashbin_id = file['h']
            file['a'] = {'n': 'Rubbish Bin'}
        return file
    
    def get_files(self):
        logger.info('Getting all files...')
        files = self._api_request({'a': 'f', 'c': 1, 'r': 1})
        files_dict = {}
        shared_keys = {}
        self._init_shared_keys(files, shared_keys)
        for file in files['f']:
            processed_file = self._process_file(file, shared_keys)
            # ensure each file has a name before returning
            if processed_file['a']:
                files_dict[file['h']] = processed_file
        return files_dict

    async def upload(self, filename, initalTime, dest=None, dest_filename=None, upstatusmsg=None):
        # determine storage node
        if dest is None:
            # if none set, upload to cloud drive node
            if not hasattr(self, 'root_id'):
                self.get_files()
            dest = self.root_id

        # Upload Status message of Pyrogram Bot
        if upstatusmsg is not None:
            uploadstatus_msg = upstatusmsg
        else:
            print("\n\n Can't Get Upload Status Message! Returning... \n\n")
            return

        # request upload url, call 'u' method
        with open(filename, 'rb') as input_file:
            file_size = path.getsize(filename)
            ul_url = self._api_request({'a': 'u', 's': file_size})['p']

            # generate random aes key (128) for file
            ul_key = [randint(0, 0xFFFFFFFF) for _ in range(6)]
            k_str = a32_to_str(ul_key[:4])
            count = Counter.new(
                128, initial_value=((ul_key[4] << 32) + ul_key[5]) << 64)
            aes = AES.new(k_str, AES.MODE_CTR, counter=count)

            upload_progress = 0
            completion_file_handle = None

            mac_str = '\0' * 16
            mac_encryptor = AES.new(k_str, AES.MODE_CBC,
                                    mac_str.encode("utf8"))
            iv_str = a32_to_str([ul_key[4], ul_key[5], ul_key[4], ul_key[5]])
            if file_size > 0:
                for chunk_start, chunk_size in get_chunks(file_size):
                    chunk = input_file.read(chunk_size)

                    upload_progress += len(chunk)

                    completedFloat = (upload_progress/1024)/1024
                    completed = int(completedFloat)
                    stream = upload_progress/file_size
                    progress = int(18*stream)
                    progress_bar = '■' * progress + '□' * (18 - progress)
                    percentage = int((stream)*100)
                    speed = round((completedFloat/(time() - initalTime)), 1)
                    if speed == 0:
                        speed = 0.1
                    remaining = int((((file_size - upload_progress)/1024)/1024)/speed)
                    
                    timeTaken = time() - initalTime

                    encryptor = AES.new(k_str, AES.MODE_CBC, iv_str)
                    for i in range(0, len(chunk) - 16, 16):
                        block = chunk[i:i + 16]
                        encryptor.encrypt(block)

                    # fix for files under 16 bytes failing
                    if file_size > 16:
                        i += 16
                    else:
                        i = 0

                    block = chunk[i:i + 16]
                    if len(block) % 16:
                        block += makebyte('\0' * (16 - len(block) % 16))
                    mac_str = mac_encryptor.encrypt(encryptor.encrypt(block))

                    # encrypt file and upload
                    chunk = aes.encrypt(chunk)
                    output_file = post(ul_url + "/" +
                                                str(chunk_start),
                                                data=chunk,
                                                timeout=self.timeout)
                    completion_file_handle = output_file.text
                    # Edit status message
                    try:
                        await uploadstatus_msg.edit(f"<b>Downloading... !! Keep patience...\n {progress_bar}\n📊Percentage: {percentage}%\n✅Completed: {completed} MB\n🚀Speed: {speed} MB/s\n⌚️Remaining Time: {remaining} seconds</b>", parse_mode = 'html')
                        logger.info('%s of %s uploaded', upload_progress,
                                    file_size)
                    except Exception as e:
                        print(e)
            else:
                output_file = post(ul_url + "/0",
                                            data='',
                                            timeout=self.timeout)
                completion_file_handle = output_file.text

            logger.info('Chunks uploaded')
            logger.info('Setting attributes to complete upload')
            logger.info('Computing attributes')
            file_mac = str_to_a32(mac_str)

            # determine meta mac
            meta_mac = (file_mac[0] ^ file_mac[1], file_mac[2] ^ file_mac[3])

            dest_filename = dest_filename or path.basename(filename)
            attribs = {'n': dest_filename}

            encrypt_attribs = base64_url_encode(
                encrypt_attr(attribs, ul_key[:4]))
            key = [
                ul_key[0] ^ ul_key[4], ul_key[1] ^ ul_key[5],
                ul_key[2] ^ meta_mac[0], ul_key[3] ^ meta_mac[1], ul_key[4],
                ul_key[5], meta_mac[0], meta_mac[1]
            ]
            encrypted_key = a32_to_base64(encrypt_key(key, self.master_key))
            logger.info('Sending request to update attributes')
            # update attributes
            data = self._api_request({
                'a':
                'p',
                't':
                dest,
                'i':
                self.request_id,
                'n': [{
                    'h': completion_file_handle,
                    't': 0,
                    'a': encrypt_attribs,
                    'k': encrypted_key
                }]
            })
            logger.info('Upload complete')
            return data

