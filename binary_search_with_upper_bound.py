def binary_search(arr, target):
    low = 0
    high = len(arr) - 1
    iterations = 0
    upper_bound = None

    while low <= high:
        iterations += 1
        mid = (low + high) // 2

        if arr[mid] < target:
            low = mid + 1
        else:
            # Якщо елемент більший або рівний target, він є кандидатом на upper_bound
            upper_bound = arr[mid]
            # Продовжуємо пошук ліворуч, щоб знайти найменший елемент, 
            # який задовольняє умову (верхню межу)
            high = mid - 1

    return iterations, upper_bound

if __name__ == "__main__":
    # Тестування на дробових числах
    sorted_floats = [0.1, 0.5, 1.3, 2.4, 3.7, 4.4, 5.9, 7.0]
    test_targets = [3.0, 0.1, 7.0, 8.0, -1.0]

    print(f"Масив: {sorted_floats}\n")

    for t in test_targets:
        result = binary_search(sorted_floats, t)
        print(f"Target: {t}, Result: {result} (Iterations: {result[0]}, Upper Bound: {result[1]})")
