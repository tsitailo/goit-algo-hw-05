import timeit
import os


# --- Алгоритм Боєра-Мура ---
def build_shift_table(pattern):
    table = {}
    length = len(pattern)
    for i in range(length - 1):
        table[pattern[i]] = length - 1 - i
    return table


def boyer_moore_search(text, pattern):
    shift_table = build_shift_table(pattern)
    n = len(text)
    m = len(pattern)
    i = 0

    if m > n:
        return -1

    while i <= n - m:
        j = m - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            return i  # Знайдено
        else:
            char_shift = shift_table.get(text[i + m - 1], m)
            i += char_shift
    return -1


# --- Алгоритм Кнута-Морріса-Пратта ---
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


def kmp_search(text, pattern):
    M = len(pattern)
    N = len(text)
    lps = compute_lps(pattern)
    i = 0
    j = 0
    while i < N:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == M:
            return i - j  # Знайдено
        elif i < N and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1


# --- Алгоритм Рабіна-Карпа ---
def polynomial_hash(s, base=256, modulus=101):
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value


def rabin_karp_search(text, pattern):
    n = len(text)
    m = len(pattern)
    if m > n:
        return -1

    base = 256
    modulus = 16777619

    pattern_hash = polynomial_hash(pattern, base, modulus)
    current_slice_hash = polynomial_hash(text[:m], base, modulus)

    h_multiplier = pow(base, m - 1) % modulus

    for i in range(n - m + 1):
        if pattern_hash == current_slice_hash:
            if text[i:i + m] == pattern:
                return i

        if i < n - m:
            current_slice_hash = (current_slice_hash - ord(text[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(text[i + m])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus
    return -1


# --- Функція для вимірювання часу ---
def measure_time(algorithm, text, pattern):
    # Виконуємо 100 повторень для більшої точності
    timer = timeit.timeit(lambda: algorithm(text, pattern), number=100)
    return timer


# --- Головна логіка ---
def run_comparison():
    # Зчитування файлів (з обробкою можливих проблем кодування)
    files = ["стаття 1.txt", "стаття 2.txt"]
    texts = {}

    for filename in files:
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    texts[filename] = f.read()
            except UnicodeDecodeError:
                # Спроба відкрити в іншому кодуванні, якщо utf-8 не підійде (для Windows)
                with open(filename, 'r', encoding='cp1251') as f:
                    texts[filename] = f.read()
        else:
            print(f"Файл {filename} не знайдено. Використовую тестовий текст.")
            texts[filename] = "Це тестовий текст для перевірки алгоритмів пошуку." * 1000

    # Підрядки для пошуку
    # Стаття 1 (Алгоритми):
    #   Існуючий: "алгоритм" (зустрічається часто)
    #   Вигаданий: "марсохід"
    # Стаття 2 (Рекомендаційні системи):
    #   Існуючий: "рекомендацій"
    #   Вигаданий: "філософія"

    patterns = {
        "стаття 1.txt": {"existing": "алгоритм", "fake": "марсохід"},
        "стаття 2.txt": {"existing": "рекомендацій", "fake": "філософія"}
    }

    results = []

    print(f"{'File':<15} | {'Pattern Type':<10} | {'Algorithm':<15} | {'Time (sec)':<10}")
    print("-" * 60)

    for filename, text in texts.items():
        if filename not in patterns: continue

        for p_type, pattern in patterns[filename].items():
            time_bm = measure_time(boyer_moore_search, text, pattern)
            time_kmp = measure_time(kmp_search, text, pattern)
            time_rk = measure_time(rabin_karp_search, text, pattern)

            print(f"{filename:<15} | {p_type:<10} | {'Boyer-Moore':<15} | {time_bm:.5f}")
            print(f"{filename:<15} | {p_type:<10} | {'KMP':<15} | {time_kmp:.5f}")
            print(f"{filename:<15} | {p_type:<10} | {'Rabin-Karp':<15} | {time_rk:.5f}")
            print("-" * 60)


if __name__ == "__main__":
    run_comparison()