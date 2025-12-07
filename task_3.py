import timeit


# KMP
def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1


# Boyer-Moore
def build_shift_table(pattern):
    table = {}
    length = len(pattern)

    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1

    table.setdefault(pattern[-1], length)
    return table


def boyer_moore_search(text, pattern):

    shift_table = build_shift_table(pattern)
    i = 0

    while i <= len(text) - len(pattern):
        j = len(pattern) - 1

        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1

        if j < 0:
            return i

        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    return -1


# Rabin-Karp
def polynomial_hash(s, base=256, modulus=101):
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value


def rabin_karp_search(main_string, substring):
    substring_length = len(substring)
    main_string_length = len(main_string)

    base = 256
    modulus = 101

    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)

    h_multiplier = pow(base, substring_length - 1) % modulus

    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i : i + substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (
                current_slice_hash - ord(main_string[i]) * h_multiplier
            ) % modulus
            current_slice_hash = (
                current_slice_hash * base + ord(main_string[i + substring_length])
            ) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1


# Calc time
def measure_time(func, text, pattern):
    return timeit.timeit(lambda: func(text, pattern), number=1000)


# Check the fastest         
def find_fastest(result_dict):
    total = {alg: v["real"] + v["fake"] for alg, v in result_dict.items()}
    return min(total, key=total.get)


if __name__ == "__main__":
    with open("article.txt", "r", encoding="utf-8") as f:
        text1 = f.read()

    with open("article_2.txt", "r", encoding="utf-8") as f:
        text2 = f.read()

    real = "використання"
    fake = "wer"

    algorithms = {"BM": boyer_moore_search, "KMP": kmp_search, "RK": rabin_karp_search}

    results = {"text1": {}, "text2": {}}

    for text_name, text_value in [("text1", text1), ("text2", text2)]:
        for alg_name, alg_func in algorithms.items():
            results[text_name][alg_name] = {
                "real": measure_time(alg_func, text_value, real),
                "fake": measure_time(alg_func, text_value, fake),
            }

    print(f"Results for text 1:")
    print(f"{results['text1']}\n")

    print(f"Results for text 2:")
    print(f"{results['text2']}\n")

    print("Fastest for text1:", find_fastest(results["text1"]))
    print("Fastest for text2:", find_fastest(results["text2"]))
