# AES 256 CBC

from base64 import b64encode
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
from Cryptodome.Random import get_random_bytes


cleartext = b"This is a secret text."

key = get_random_bytes(32)  # must be 16, 24 or 32 bytes long
cipher = AES.new(key, AES.MODE_CBC)
ciphertext = cipher.encrypt(pad(cleartext, AES.block_size))

print(f"iv: {b64encode(cipher.iv).decode('utf-8')}")
print(f"ciphertext: {b64encode(ciphertext).decode('utf-8')}")
print(f"key: {b64encode(key).decode('utf-8')}")
