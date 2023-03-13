# RSA cipher
# http://inventwithpython.com/hacking (BSD Licensed)

import sys

# IMPORTANT: The block size MUST be less than or equal to the key size!
# (Note: The block size is in bytes, the key size is in bits. There
# are 8 bits in 1 byte.)
DEFAULT_BLOCK_SIZE = 128  # 128 bytes
BYTE_SIZE = 256  # One byte has 256 different values.


def main():
    # Runs a test that encrypts a message to a file or decrypts a message
    # from a file.
    filename = "encrypted_file.txt"  # the file to write to/read from
    mode = "encrypt"  # set to 'encrypt' or 'decrypt'

    if mode == "encrypt":
        message = (
            "Journalists belong in the gutter because that is where the ruling classes"
            " throw their guilty secrets. Gerald Priestland. The Founding Fathers gave"
            " the free press the protection it must have to bare the secrets of"
            " government and inform the people. Hugo Black."
        )
        public_key_filename = "al_sweigart_pubkey.txt"
        print("Encrypting and writing to %s..." % (filename))
        encrypted_text = encrypt_and_write_to_file(
            filename, public_key_filename, message
        )

        print("Encrypted text:")
        print(encrypted_text)

    elif mode == "decrypt":
        private_key_filename = "al_sweigart_privkey.txt"
        print("Reading from %s and decrypting..." % (filename))
        decrypted_text = read_from_file_and_decrypt(filename, private_key_filename)

        print("Decrypted text:")
        print(decrypted_text)


def get_blocks_from_text(message, blocksize=DEFAULT_BLOCK_SIZE):
    # Converts a string message to a list of block integers. Each integer
    # represents 128 (or whatever blocksize is set to) string characters.

    message_bytes = message.encode("ascii")  # convert the string to bytes

    block_ints = []
    for block_start in range(0, len(message_bytes), blocksize):
        # Calculate the block integer for this block of text
        block_int = 0
        for i in range(block_start, min(block_start + blocksize, len(message_bytes))):
            block_int += message_bytes[i] * (BYTE_SIZE ** (i % blocksize))
        block_ints.append(block_int)
    return block_ints


def get_text_from_blocks(block_ints, message_length, blocksize=DEFAULT_BLOCK_SIZE):
    # Converts a list of block integers to the original message string.
    # The original message length is needed to properly convert the last
    # block integer.
    message = []
    for block_int in block_ints:
        block_message = []
        for i in range(blocksize - 1, -1, -1):
            if len(message) + i < message_length:
                # Decode the message string for the 128 (or whatever
                # blocksize is set to) characters from this block integer.
                ascii_number = block_int // (BYTE_SIZE**i)
                block_int = block_int % (BYTE_SIZE**i)
                block_message.insert(0, chr(ascii_number))
        message.extend(block_message)
    return "".join(message)


def encrypt_message(message, key, blocksize=DEFAULT_BLOCK_SIZE):
    # Converts the message string into a list of block integers, and then
    # encrypts each block integer. Pass the PUBLIC key to encrypt.
    encrypted_blocks = []
    n, e = key

    for block in get_blocks_from_text(message, blocksize):
        # ciphertext = plaintext ^ e mod n
        encrypted_blocks.append(pow(block, e, n))
    return encrypted_blocks


def decrypt_message(
    encrypted_blocks, message_length, key, blocksize=DEFAULT_BLOCK_SIZE
):
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


def encrypt_and_write_to_file(
    message_filename, key_filename, message, blocksize=DEFAULT_BLOCK_SIZE
):
    # Using a key from a key file, encrypt the message and save it to a
    # file. Returns the encrypted message string.
    keysize, n, e = read_key_file(key_filename)

    # Check that key size is greater than block size.
    if keysize < blocksize * 8:  # * 8 to convert bytes to bits
        sys.exit(
            "ERROR: Block size is %s bits and key size is %s bits. The RSA cipher"
            " requires the block size to be equal to or greater than the key size."
            " Either decrease the block size or use different keys."
            % (blocksize * 8, keysize)
        )

    # Encrypt the message
    encrypted_blocks = encrypt_message(message, (n, e), blocksize)

    # Convert the large int values to one string value.
    for i in range(len(encrypted_blocks)):
        encrypted_blocks[i] = str(encrypted_blocks[i])
    encrypted_content = ",".join(encrypted_blocks)

    # Write out the encrypted string to the output file.
    encrypted_content = "%s_%s_%s" % (len(message), blocksize, encrypted_content)
    fo = open(message_filename, "w")
    fo.write(encrypted_content)
    fo.close()
    # Also return the encrypted string.
    return encrypted_content


def read_from_file_and_decrypt(message_filename, key_filename):
    # Using a key from a key file, read an encrypted message from a file
    # and then decrypt it. Returns the decrypted message string.
    keysize, n, d = read_key_file(key_filename)

    # Read in the message length and the encrypted message from the file.
    fo = open(message_filename)
    content = fo.read()
    message_length, blocksize, encrypted_message = content.split("_")
    message_length = int(message_length)
    blocksize = int(blocksize)

    # Check that key size is greater than block size.
    if keysize < blocksize * 8:  # * 8 to convert bytes to bits
        sys.exit(
            "ERROR: Block size is %s bits and key size is %s bits. The RSA cipher"
            " requires the block size to be equal to or greater than the key size. Did"
            " you specify the correct key file and encrypted file?"
            % (blocksize * 8, keysize)
        )

    # Convert the encrypted message into large int values.
    encrypted_blocks = []
    for block in encrypted_message.split(","):
        encrypted_blocks.append(int(block))

    # Decrypt the large int values.
    return decrypt_message(encrypted_blocks, message_length, (n, d), blocksize)


# If rsa_cipher.py is run (instead of imported as a module) call
# the main() function.
if __name__ == "__main__":
    main()
