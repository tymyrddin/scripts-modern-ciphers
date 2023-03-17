# Galois LFSR


def main() -> None:
    print("\n\nGalois LFSR output: ")
    lfsr_galois("1100", [2, 3])


def lfsr_galois(input_string: str, taps: list[int]) -> None:
    count = 0
    n = len(input_string)
    m = len(taps)
    for j in range(0, m):
        taps[j] = taps[j] - 1

    while count < (pow(2, n) - 1):
        input_string_copy = input_string
        print(input_string, int(input_string, 2))
        input_string = input_string_copy[n - 1] + input_string[:-1]
        input_string_list = list(input_string)
        for i in range(0, m):
            if taps[i] + 1 < n:
                input_string_list[taps[i] + 1] = str(
                    int(input_string_copy[taps[i]]) ^ int(input_string_copy[n - 1])
                )

        input_string = "".join(input_string_list)

        count = count + 1


if __name__ == "__main__":
    main()
