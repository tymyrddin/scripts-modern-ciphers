# Fibonacci LFSR


def main() -> None:
    print("Fibonacci LFSR output : \n")
    lfsr_fib("1100", (2, 3))


def lfsr_fib(input_string: str, taps: tuple[int, int]) -> None:
    count, xor = 0, 0
    n = len(input_string)
    while count < (pow(2, n) - 1):
        for t in taps:
            xor += int(input_string[t - 1])
        if xor % 2 == 0.0:
            xor = 0
        else:
            xor = 1

        print(input_string, xor, int(input_string, 2))

        input_string, xor = str(xor) + input_string[:-1], 0
        count = count + 1


if __name__ == "__main__":
    main()
