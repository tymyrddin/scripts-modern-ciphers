# AES CBC decrypt

import argparse  # https://docs.python.org/3/library/argparse.html
import textwrap  # https://docs.python.org/3/library/textwrap.html
from base64 import b64decode

from Cryptodome.Cipher import AES


def main() -> None:
    # Get and parse the arguments
    options = get_args()

    try:
        iv = b64decode(options.iv)
        ciphertext = b64decode(options.ciphertext)
        key = b64decode(options.key)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_plaintext = cipher.decrypt(ciphertext)
        plaintext = unpad(padded_plaintext, AES.block_size)
        print("Original message was: ", plaintext.decode("utf8"))
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


def unpad(message: bytes, blocksize: int) -> bytes:
    # PKCS #5 (or #7) Remove padding (except for dropping
    # strings not conforming to the standard)
    padding_length = message[-1]
    if not 1 <= padding_length <= blocksize:
        raise
    for i in range(padding_length):
        if message[-i - 1] != padding_length:
            raise
    return message[:-padding_length]


if __name__ == "__main__":
    main()
