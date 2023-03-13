# Cryptomath Module
# https://www.nostarch.com/crackingcodes (BSD Licensed)
# - naming conventions
# - type hints
# - value error instead on returning None


def gcd(a: int, b: int) -> int:
    while a != 0:
        a, b = b % a, a
    return b


def find_mod_inverse(a: int, m: int) -> int:
    # Return the modular inverse of a % m, which is
    # the number x such that a*x % m = 1

    # No mod inverse exists if a & m aren't relatively prime.
    if gcd(a, m) != 1:
        raise ValueError(f"mod inverse of {a!r} and {m!r} does not exist")

    # Calculate using the Extended Euclidean Algorithm:
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m
