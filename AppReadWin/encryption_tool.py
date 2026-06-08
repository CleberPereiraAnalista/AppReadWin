from cryptography.fernet import Fernet
import base64
import logging
import traceback

class EncryptionTool:

    def __init__(self, key):
        self.ENCRYPT_KEY = key

    def encrypt(self, txt):
        try:
            # convert integer etc to string first
            txt = str(txt)
            # get the key from settings
            encoder = Fernet(self.ENCRYPT_KEY) # key should be byte
            # #input should be byte, so convert the text to byte
            encrypted_text = encoder.encrypt(txt.encode('utf-8'))
            # encode to urlsafe base64 format
            encrypted_text = base64.urlsafe_b64encode(encrypted_text).decode("utf-8") 
            return encrypted_text
        except Exception as e:
            # log the error if any
            logging.getLogger("error_logger").error(traceback.format_exc())
            return e #None

    def decrypt(self, txt):
        try:
            # base64 decode
            #bytes_txt = bytes(txt, 'utf-8')
            bytes_txt = base64.urlsafe_b64decode(txt)
            token_decoder = Fernet(self.ENCRYPT_KEY)
            decoded_text = token_decoder.decrypt(bytes_txt).decode("utf-8")     
            return decoded_text
            
        except Exception as e:
            # log the error
            logging.getLogger("error_logger").error(traceback.format_exc())
            return e #None

