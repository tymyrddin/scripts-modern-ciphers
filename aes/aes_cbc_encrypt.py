# AES CBC encrypt

import argparse  # https://docs.python.org/3/library/argparse.html
import textwrap  # https://docs.python.org/3/library/textwrap.html
from base64 import b64encode

from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes


def main() -> None:
    # Get and parse the arguments
    options = get_args()
    key = get_random_bytes(options.keysize)  # must be 16, 24 or 32 bytes long

    ciphertext = encrypt(key, options.plaintext.encode("utf-8"))

    print(f"iv: {b64encode(ciphertext[1]).decode('utf-8')}")
    print(f"ciphertext: {b64encode(ciphertext[0]).decode('utf-8')}")
    print(f"key: {b64encode(key).decode('utf-8')}")


def get_args():
    parser = argparse.ArgumentParser(
        description="AES CBC encrypt",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """Example:
            aes_cbc_encrypt.py -p "This is my very, very, very secret message." -k 16
        """
        ),
    )
    parser.add_argument(
        "-p",
        "--plaintext",
        default="This is my very, very, very secret message.",
        help="Message to encrypt",
    )
    parser.add_argument(
        "-k",
        "--keysize",
        type=int,
        default=16,
        choices=[16, 24, 32],
        help="Keysize",
    )
    values = parser.parse_args()
    return values


# Adds padding to the plain text to make it a multiple of 16 bytes
def pad(message: bytes, blocksize: int) -> bytes:
    # PKCS #5 (or #7) with padding
    padding_length = blocksize - len(message) % blocksize
    padding = (chr(padding_length) * padding_length).encode()
    return bytearray(message + padding)


# Encrypt a plaintext with a key in AES CBC mode
def encrypt(key: bytes, plaintext: bytes) -> tuple[bytes, bytes]:
    cipher = AES.new(key, AES.MODE_CBC)
    padded_plaintext = pad(plaintext, AES.block_size)
    ciphertext = cipher.encrypt(padded_plaintext)
    iv = cipher.iv
    return ciphertext, iv


if __name__ == "__main__":
    main()
