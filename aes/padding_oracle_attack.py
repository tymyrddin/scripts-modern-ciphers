# Padding oracle attack

from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from base64 import b64encode

KEYSIZE = AES.key_size
BLOCKSIZE = 16  # AES.block_size
SECRET_KEY = get_random_bytes(BLOCKSIZE)  # key doesn't matter, but must be of right size


def main() -> None:
    plaintext = b"This is a very, very super-secret message."
    print(f"Plaintext: {plaintext.decode('utf-8')}")

    ciphertext = encrypt(plaintext)
    print(f"Ciphertext: {b64encode(ciphertext).decode('utf-8')}")

    print("Starting the attack: ")
    hacked_plaintext = attack(ciphertext)
    print(f"Success: {hacked_plaintext}")


# Adds padding to the plain text to make it a multiple of 16 bytes
def pad(message: bytes) -> bytes:
    padding_length = BLOCKSIZE - len(message) % BLOCKSIZE
    padding = (chr(padding_length) * padding_length).encode()
    return bytearray(message + padding)


# Function to remove PKCS5 or PKCS5 padding, if exists
def unpad(message: bytes) -> bytes:
    padding_length = message[-1]
    if not 1 <= padding_length <= BLOCKSIZE:
        raise
    for i in range(padding_length):
        if message[-i - 1] != padding_length:
            raise
    return message[:-padding_length]


def encrypt(plaintext: bytes) -> bytes:
    iv = get_random_bytes(BLOCKSIZE)
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(pad(plaintext))


def decrypt(ciphertext: bytes) -> bytes:
    iv = ciphertext[:BLOCKSIZE]
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext[BLOCKSIZE:]))


# Simulate vulnerable API endpoint that returns 200 if the
# ciphertext gives a plaintext with valid padding, and 500 if not.
def padding_oracle(ciphertext: bytes) -> int:
    try:
        decrypt(ciphertext)
        return 1
    except RuntimeError:
        return 0


# Function to cut a bytestream into blocks
def blockify(text: bytes, blocksize: int = BLOCKSIZE) -> list[bytes]:
    blocks = []
    for i in range(0, len(text), blocksize):
        blocks.append(text[i: i + blocksize])
    return blocks


def attack(ciphertext: bytes) -> str:
    cipher_blocks = blockify(ciphertext, BLOCKSIZE)

    hacked_plaintext = ""
    for block_idx in range(1, len(cipher_blocks)):
        auxiliary = b""
        for padding_length in range(1, BLOCKSIZE + 1):
            for guess in range(256):
                new_auxiliary = bytes([guess]) + auxiliary
                auxiliary_block = (
                    get_random_bytes(BLOCKSIZE - padding_length) + new_auxiliary
                )
                auxiliary_blocks = (
                    cipher_blocks[: -block_idx - 1]
                    + [auxiliary_block]
                    + [cipher_blocks[-block_idx]]
                )

                if padding_oracle(b"".join(auxiliary_blocks)):
                    cipher_block = cipher_blocks[-block_idx - 1]
                    p = padding_length ^ cipher_block[-padding_length] ^ guess
                    hacked_plaintext += chr(p)
                    print("Byte decrypted: 0x%02x" % p)

                    auxiliary = bytes(
                        [
                            byte ^ padding_length ^ (padding_length + 1)
                            for byte in new_auxiliary
                        ]
                    )
                    break

    return hacked_plaintext[::-1]


if __name__ == "__main__":
    main()
