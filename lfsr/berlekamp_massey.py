# Berlekamp Massey implementation

import numpy as np
import copy

from numpy import dtype


def main() -> None:
    cipher = [1, 1, 0, 0, 1, 0, 1, 0]  # comma separated
    results = berlekamp_massey(cipher)
    print(f"Minimal LFSR: {results[0]}")
    print(f"Minimal polynomial: {results[1]}")


# Find the minimal LFSR and minimal polynomial to generate the data
def berlekamp_massey(data: list[int]) -> tuple[int, np.ndarray[int, dtype[int]]]:
    n = len(data)
    c_x, b_x = np.zeros(n, dtype=int), np.zeros(n, dtype=int)
    c_x[0], b_x[0] = 1, 1
    l, m, i = 0, -1, 0
    while i < n:
        v = data[(i - l) : i]
        v = v[::-1]
        cc = c_x[1 : l + 1]
        delta = (data[i] + np.dot(v, cc)) % 2
        if delta == 1:
            temp = copy.copy(c_x)
            p = np.zeros(n, dtype=int)
            for j in range(0, l):
                if b_x[j] == 1:
                    p[j + i - m] = 1
            c_x = (c_x + p) % 2
            if l <= 0.5 * i:
                l = i + 1 - l
                m = i
                b_x = temp
        i += 1
    c_x = c_x.tolist()
    ind = 0
    for x in c_x[::-1]:
        if x == 0:
            ind += 1
        else:
            break
    c_x = c_x[:-ind]
    return len(c_x) - 1, c_x


if __name__ == "__main__":
    main()
