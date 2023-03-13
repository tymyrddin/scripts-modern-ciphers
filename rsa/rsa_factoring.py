# https://www.di-mgt.com.au/rsa_factorize_n.html
# When factoring n, integers p and q can be found, such that
# n = p * q.
# Calculate Y = (p - 1)(q - 1) to find the private key exponent
# d = 1/e mod Y.
#
# To decrypt one of the values c in an intercepted message,
# calculate m = c^d mod n, where m is the decrypted message.
# This works because (m^e)^d mod n is equal to 1.

import argparse  # https://docs.python.org/3/library/argparse.html
import math
import random
import textwrap  # https://docs.python.org/3/library/textwrap.html


def main():
    options = get_args()
    factors = rsafactor(options.d, options.e, options.n)
    print(factors)


def get_args():
    parser = argparse.ArgumentParser(
        description="Columnar transposition cipher encryption",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """Example:
            columnar_encrypt.py -t sometext
            columnar_encrypt.py -t sometext -k 13
        """
        ),
    )
    parser.add_argument(
        "-n",
        "--RSA modulus",
        type=int,
        default=13,
        help="RSA modulus (n)",
    )
    parser.add_argument(
        "-e",
        "--Derived number (e)",
        type=int,
        default=13,
        help="Key (Number)",
    )
    parser.add_argument(
        "-d",
        "--Private key",
        type=int,
        default=13,
        help="Key (Number)",
    )
    values = parser.parse_args()
    return values


def rsafactor(d: int, e: int, n: int) -> list[int]:
    k = d * e - 1
    p = 0
    q = 0
    while p == 0:
        g = random.randint(2, n - 1)
        t = k
        while True:
            if t % 2 == 0:
                t = t // 2
                x = (g**t) % n
                y = math.gcd(x - 1, n)
                if x > 1 and y > 1:
                    p = y
                    q = n // y
                    break  # find the correct factors
            else:
                break  # t is not divisible by 2, break and choose another g
    return sorted([p, q])


# If rsa_hack.py is run (instead of imported as a module) call
# the main() function.
if __name__ == "__main__":
    main()
