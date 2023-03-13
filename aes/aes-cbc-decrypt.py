# AES 256 CBC

from base64 import b64decode
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad


try:
    iv = b64decode('/h+bk0oPfqaCjrEHpmkbCQ==')
    ciphertext = b64decode('rc0lALT3hpylphn0Tw9hBYJ1Y4LJ5blNJJGhwpVGAmE=')
    key = b64decode('quBGevVd6tEKzdYyUy2L4teYSXwFwfuRCvIclrN+kgY=')
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    print("Original message was: ", plaintext)
except (ValueError, KeyError):
    print("ERROR!")
