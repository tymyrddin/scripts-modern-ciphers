# Public Key Cipher
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)
# Python naming conventions
# Added type hints

import math
import sys

# The public and private keys for this program are created by
# the generate_public_private_keys.py program.
# This program must be run in the same folder as the key files.

SYMBOLS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?."


def main() -> None:
    # Runs a test that encrypts a message to a file or decrypts a message
    # from a file.
    filename = "encrypted_file.txt"  # The file to write to/read from.
    mode = "encrypt"  # Set to either 'encrypt' or 'decrypt'.

    if mode == "encrypt":
        message = (
            "Journalists belong in the gutter because that is where the ruling classes"
            " throw their guilty secrets. Gerald Priestland. The Founding Fathers gave"
            " the free press the protection it must have to bare the secrets of"
            " government and inform the people. Hugo Black."
        )
        public_key_filename = "al_sweigart_pubkey.txt"
        print("Encrypting and writing to %s..." % filename)
        encrypted_text = encrypt_and_write_to_file(
            filename, public_key_filename, message
        )

        print("Encrypted text:")
        print(encrypted_text)

    elif mode == "decrypt":
        private_key_filename = "al_sweigart_privkey.txt"
        print("Reading from %s and decrypting..." % filename)
        decrypted_text = read_from_file_and_decrypt(filename, private_key_filename)

        print("Decrypted text:")
        print(decrypted_text)


def get_blocks_from_text(message: str, blocksize: int) -> list[int]:
    # Converts a string message to a list of block integers.
    for character in message:
        if character not in SYMBOLS:
            print("ERROR: The symbol set does not have the character %s" % character)
            sys.exit()
    block_ints = []
    for block_start in range(0, len(message), blocksize):
        # Calculate the block integer for this block of text:
        block_int = 0
        for i in range(block_start, min(block_start + blocksize, len(message))):
            block_int += (SYMBOLS.index(message[i])) * (len(SYMBOLS) ** (i % blocksize))
        block_ints.append(block_int)
    return block_ints


def get_text_from_blocks(
    block_ints: list[int], message_length: int, blocksize: int
) -> str:
    # Converts a list of block integers to the original message string.
    # The original message length is needed to properly convert the last
    # block integer.
    message: list[str] = []
    for block_int in block_ints:
        block_message: list[str] = []
        for i in range(blocksize - 1, -1, -1):
            if len(message) + i < message_length:
                # Decode the message string for the 128 (or whatever
                # blocksize is set to) characters from this block integer:
                character_index = block_int // (len(SYMBOLS) ** i)
                block_int = block_int % (len(SYMBOLS) ** i)
                block_message.insert(0, SYMBOLS[character_index])
        message.extend(block_message)
    return "".join(message)


def encrypt_message(message, key, blocksize):
    # Converts the message string into a list of block integers, and then
    # encrypts each block integer. Pass the PUBLIC key to encrypt.
    encrypted_blocks = []
    n, e = key

    for block in get_blocks_from_text(message, blocksize):
        # ciphertext = plaintext ^ e mod n
        encrypted_blocks.append(pow(block, e, n))
    return encrypted_blocks


def decrypt_message(encrypted_blocks, message_length, key, blocksize):
    # Decrypts a list of encrypted block ints into the original message
    # string. The original message length is required to properly decrypt
    # the last block. Be sure to pass the PRIVATE key to decrypt.
    decrypted_blocks = []
    n, d = key
    for block in encrypted_blocks:
        # plaintext = ciphertext ^ d mod n
        decrypted_blocks.append(pow(block, d, n))
    return get_text_from_blocks(decrypted_blocks, message_length, blocksize)


def read_key_file(key_filename):
    # Given the filename of a file that contains a public or private key,
    # return the key as a (n,e) or (n,d) tuple value.
    fo = open(key_filename)
    content = fo.read()
    fo.close()
    keysize, n, e_or_d = content.split(",")
    return int(keysize), int(n), int(e_or_d)


def encrypt_and_write_to_file(message_filename, key_filename, message, blocksize=None):
    # Using a key from a key file, encrypt the message and save it to a
    # file. Returns the encrypted message string.
    keysize, n, e = read_key_file(key_filename)
    if blocksize is None:
        # If blocksize isn't given, set it to the largest size allowed by
        # the key size and symbol set size.
        blocksize = int(math.log(2**keysize, len(SYMBOLS)))
    # Check that key size is large enough for the block size:
    if not (math.log(2**keysize, len(SYMBOLS)) >= blocksize):
        sys.exit(
            "ERROR: Block size is too large for the key and symbol set size. Did you"
            " specify the correct key file and encrypted file?"
        )
    # Encrypt the message:
    encrypted_blocks = encrypt_message(message, (n, e), blocksize)

    # Convert the large int values to one string value:
    for i in range(len(encrypted_blocks)):
        encrypted_blocks[i] = str(encrypted_blocks[i])
    encrypted_content = ",".join(encrypted_blocks)

    # Write out the encrypted string to the output file:
    encrypted_content = "%s_%s_%s" % (len(message), blocksize, encrypted_content)
    fo = open(message_filename, "w")
    fo.write(encrypted_content)
    fo.close()
    # Also return the encrypted string:
    return encrypted_content


def read_from_file_and_decrypt(message_filename, key_filename):
    # Using a key from a key file, read an encrypted message from a file
    # and then decrypt it. Returns the decrypted message string.
    keysize, n, d = read_key_file(key_filename)

    # Read in the message length and the encrypted message from the file:
    fo = open(message_filename)
    content = fo.read()
    message_length, blocksize, encrypted_message = content.split("_")
    message_length = int(message_length)
    blocksize = int(blocksize)

    # Check that key size is large enough for the block size:
    if not (math.log(2**keysize, len(SYMBOLS)) >= blocksize):
        sys.exit(
            "ERROR: Block size is too large for the key and symbol set size. Did you"
            " specify the correct key file and encrypted file?"
        )

    # Convert the encrypted message into large int values:
    encrypted_blocks = []
    for block in encrypted_message.split(","):
        encrypted_blocks.append(int(block))

    # Decrypt the large int values:
    return decrypt_message(encrypted_blocks, message_length, (n, d), blocksize)


# If public_key_cipher.py is run (instead of imported as a module) call
# the main() function.
if __name__ == "__main__":
    main()
