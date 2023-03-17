# Prime Number Sieve
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)

import math
import random


def is_prime_trial_div(number: int) -> bool:
    # Returns True if number is a prime number, otherwise False.

    # Uses the trial division algorithm for testing primality.

    # All numbers less than 2 are not prime:
    if number < 2:
        return False

    # See if number is divisible by any number up to the square root of number:
    for i in range(2, int(math.sqrt(number)) + 1):
        if number % i == 0:
            return False
    return True


def prime_sieve(sieve_size: int) -> list[int]:
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


def rabin_miller(number: int) -> bool:
    # Returns True if number is a prime number.
    if number % 2 == 0 or number < 2:
        return False  # Rabin-Miller doesn't work on even integers.
    if number == 3:
        return True
    s = number - 1
    t = 0
    while s % 2 == 0:
        # Keep halving s until it is odd (and use t
        # to count how many times we halve s):
        s = s // 2
        t += 1
    for _trials in range(5):  # Try to falsify number's primality 5 times.
        a = random.randrange(2, number - 1)
        v = pow(a, s, number)
        if v != 1:  # (This test does not apply if v is 1.)
            i = 0
            while v != (number - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v**2) % number
    return True


# Most of the time we can quickly determine if number is not prime
# by dividing by the first few dozen prime numbers. This is quicker
# than rabin_miller(), but does not detect all composites.
LOW_PRIMES = prime_sieve(100)


def is_prime(number):
    # Return True if number is a prime number. This function does a quicker
    # prime number check before calling rabin_miller().
    if number < 2:
        return False  # 0, 1, and negative numbers are not prime.
    # See if any of the low prime numbers can divide number:
    for prime in LOW_PRIMES:
        if number % prime == 0:
            return False
        if number == prime:
            return True
    # If all else fails, call rabin_miller() to determine if number is a prime:
    return rabin_miller(number)


def generate_large_prime(keysize=1024):
    # Return a random prime number that is keysize bits in size:
    while True:
        number = random.randrange(2 ** (keysize - 1), 2**keysize)
        if is_prime(number):
            return number
