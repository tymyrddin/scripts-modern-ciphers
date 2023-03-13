# Prime Number Sieve
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)

import math
import random


def is_prime_trial_div(num):
    # Returns True if num is a prime number, otherwise False.

    # Uses the trial division algorithm for testing primality.

    # All numbers less than 2 are not prime:
    if num < 2:
        return False

    # See if num is divisible by any number up to the square root of num:
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True


def prime_sieve(sieve_size: object) -> object:
    # Returns a list of prime numbers calculated using
    # the Sieve of Eratosthenes algorithm.

    sieve = [True] * sieve_size
    sieve[0] = False  # Zero and one are not prime numbers.
    sieve[1] = False

    # Create the sieve:
    for i in range(2, int(math.sqrt(sieve_size)) + 1):
        pointer = i * 2
        while pointer < sieve_size:
            sieve[pointer] = False
            pointer += i

    # Compile the list of primes:
    primes = []
    for i in range(sieve_size):
        if sieve[i]:
            primes.append(i)

    return primes


def rabin_miller(num):
    # Returns True if num is a prime number.
    if num % 2 == 0 or num < 2:
        return False  # Rabin-Miller doesn't work on even integers.
    if num == 3:
        return True
    s = num - 1
    t = 0
    while s % 2 == 0:
        # Keep halving s until it is odd (and use t
        # to count how many times we halve s):
        s = s // 2
        t += 1
    for _trials in range(5):  # Try to falsify num's primality 5 times.
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)
        if v != 1:  # (This test does not apply if v is 1.)
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v**2) % num
    return True


# Most of the time we can quickly determine if num is not prime
# by dividing by the first few dozen prime numbers. This is quicker
# than rabin_miller(), but does not detect all composites.
LOW_PRIMES = prime_sieve(100)


def is_prime(num):
    # Return True if num is a prime number. This function does a quicker
    # prime number check before calling rabin_miller().
    if num < 2:
        return False  # 0, 1, and negative numbers are not prime.
    # See if any of the low prime numbers can divide num:
    for prime in LOW_PRIMES:
        if num % prime == 0:
            return False
        if num == prime:
            return True
    # If all else fails, call rabin_miller() to determine if num is a prime:
    return rabin_miller(num)


def generate_large_prime(keysize=1024):
    # Return a random prime number that is keysize bits in size:
    while True:
        num = random.randrange(2 ** (keysize - 1), 2**keysize)
        if is_prime(num):
            return num
