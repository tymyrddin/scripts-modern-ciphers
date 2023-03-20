# Public Key Generator
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)

import os
import random
import sys

import cryptomath
import prime_numbers


def main() -> None:
    # Create a public/private keypair with 1024-bit keys:
    print("Making key files...")
    create_key_files("named_keyfile", 1024)
    print("Key files made.")


def generate_key(keysize: int) -> tuple[tuple[int, int], tuple[int, int]]:
    # Creates a public/private keys keysize bits in size.
    p = 0
    q = 0
    # Create two prime numbers, p and q. Calculate n = p * q.
    print("Generating p & q primes...")
    while p == q:
        p = prime_numbers.generate_large_prime(keysize)
        q = prime_numbers.generate_large_prime(keysize)
    n = p * q

    # Create a number e that is relatively prime to (p-1)*(q-1):
    print("Generating e that is relatively prime to (p-1)*(q-1)...")
    while True:
        # Keep trying random numbers for e until one is valid:
        e = random.randrange(2 ** (keysize - 1), 2**keysize)
        if cryptomath.gcd(e, (p - 1) * (q - 1)) == 1:
            break

    # Calculate d, the mod inverse of e:
    print("Calculating d that is mod inverse of e...")
    d = cryptomath.find_mod_inverse(e, (p - 1) * (q - 1))

    public_key = (n, e)
    private_key = (n, d)

    print("Public key:", public_key)
    print("Private key:", private_key)

    return public_key, private_key


def create_key_files(name: str, key_size: int) -> None:
    # Creates two files 'x_pubkey.txt' and 'x_privkey.txt' (where x
    # is the value in name) with the n,e and d,e integers written in
    # them, delimited by a comma.

    # Safety check to prevent overwriting old key files:
    if os.path.exists("%s_pubkey.txt" % name) or os.path.exists(
        "%s_privkey.txt" % name
    ):
        sys.exit(
            "WARNING: The file %s_pubkey.txt or %s_privkey.txt already exists! Use a"
            " different name or delete these files and re-run this program."
            % (name, name)
        )

    public_key, private_key = generate_key(key_size)

    print()
    print(
        "The public key is a %s and a %s digit number."
        % (len(str(public_key[0])), len(str(public_key[1])))
    )
    print("Writing public key to file %s_pubkey.txt..." % name)
    fo = open("%s_pubkey.txt" % name, "w")
    fo.write("%s,%s,%s" % (key_size, public_key[0], public_key[1]))
    fo.close()

    print()
    print(
        "The private key is a %s and a %s digit number."
        % (len(str(private_key[0])), len(str(private_key[1])))
    )
    print("Writing private key to file %s_privkey.txt..." % name)
    fo = open("%s_privkey.txt" % name, "w")
    fo.write("%s,%s,%s" % (key_size, private_key[0], private_key[1]))
    fo.close()


# If generate_public_private_keys.py is run (instead of imported as a module),
# call the main() function:
if __name__ == "__main__":
    main()
