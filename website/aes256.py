from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from hashlib import shake_256

# encryption AES 256
class aes256:
    # encrypt AES 128
    def encrypt(self, key, message, iv):
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ct_bytes = cipher.encrypt(message)
        print(ct_bytes)
        ct = b64encode(ct_bytes).decode('utf-8')  # cipher text
        return ct

    def decrypt(self, cipher, key, iv):
        cipher_d = AES.new(key, AES.MODE_CBC, iv)
        pt = cipher_d.decrypt(b64decode(cipher))  # plain text
        return pt

    def shake_256(self, val, size):
        m = shake_256()
        m.update(val)
        u = m.hexdigest(size)
        return bytes.fromhex(u)



