# AES CBC decrypt

import argparse  # https://docs.python.org/3/library/argparse.html
import textwrap  # https://docs.python.org/3/library/textwrap.html
from base64 import b64decode

from Cryptodome.Cipher import AES


def main() -> None:
    # Get and parse the arguments
    options = get_args()

    try:
        plaintext = decrypt(
            b64decode(options.key), b64decode(options.ciphertext), b64decode(options.iv)
        )
        print(f"Original message was: {plaintext.decode('utf8')}")
    except (ValueError, KeyError):
        print("ERROR!")


def get_args():
    parser = argparse.ArgumentParser(
        description="AES CBC decrypt",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """Example:
            aes_cbc_decrypt.py -i /rB4uLusPoAcqiSqOK2sFg==
             -c e9czIy7NPMcXclQjbESJ7/wfRL85GWfwfI4pXjsY6qQMkT6ywnUuc2wT96opvs9c
             -k kBw8iQ4p/uAC1Flp1W9qGQ==
        """
        ),
    )
    parser.add_argument(
        "-i",
        "--iv",
        default="9xMenf44ATU8ypJG0cTe6g==",
        help="Initialization Vector",
    )
    parser.add_argument(
        "-c",
        "--ciphertext",
        default="qX69xo/poHeqVW7REQPKlZv56W4kjMkoiqM+lrrWRsz0D6G/Cb8NTtldCrvfB7I4",
        help="Cipertext to decrypt",
    )
    parser.add_argument(
        "-k",
        "--key",
        default="dvgN929hueyd6F+/7A7SwQ==",
        help="Cipertext to decrypt",
    )
    values = parser.parse_args()
    return values


# Function to verify if the bytestream ends with
# a suffix of X times 'X' (PKCS7)
def validate_padding(padded_text: bytes) -> bool:
    for i in range(1, 17):  # find padding
        if bytes([padded_text[-1]]) == bytes([i]):
            for j in range(1, i + 1):  # check padding
                if bytes([padded_text[-j]]) != bytes([i]):
                    return False
            return True
    return False


# Function to remove PKCS5 or PKCS5 padding, if exists
def unpad(message: bytes) -> bytes | None:
    if validate_padding(message):
        padding_length = message[-1]
        return message[:-padding_length]
    return None


# Decrypt a ciphertext with a key and iv in AES CBC mode
def decrypt(key: bytes, ciphertext: bytes, iv: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_plaintext = cipher.decrypt(ciphertext)
    plaintext = unpad(padded_plaintext)
    return plaintext


if __name__ == "__main__":
    main()
