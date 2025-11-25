import unittest
import sys
import os

# Додаємо батьківську директорію до шляху, щоб імпортувати модуль з кореня проекту
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from binary_search_with_upper_bound import binary_search

class TestBinarySearch(unittest.TestCase):

    def test_basic_search_found(self):
        """Тест: елемент точно присутній у масиві."""
        arr = [0.1, 0.5, 1.3, 2.4, 3.7]
        target = 1.3
        iterations, upper_bound = binary_search(arr, target)
        
        self.assertEqual(upper_bound, 1.3)
        self.assertTrue(iterations > 0)

    def test_search_upper_bound(self):
        """Тест: елемента немає, повертаємо найменший елемент >= target."""
        arr = [0.1, 0.5, 1.3, 2.4, 3.7]
        target = 2.0
        # 2.4 є найменшим числом, яке >= 2.0
        iterations, upper_bound = binary_search(arr, target)
        
        self.assertEqual(upper_bound, 2.4)

    def test_target_smaller_than_all(self):
        """Тест: ціль менша за всі елементи масиву."""
        arr = [1.1, 2.2, 3.3]
        target = 0.5
        # Перший елемент (1.1) є верхньою межею
        iterations, upper_bound = binary_search(arr, target)
        self.assertEqual(upper_bound, 1.1)

    def test_target_larger_than_all(self):
        """Тест: ціль більша за всі елементи масиву."""
        arr = [1.1, 2.2, 3.3]
        target = 10.0
        # Немає елемента >= 10.0
        iterations, upper_bound = binary_search(arr, target)
        self.assertIsNone(upper_bound)

    def test_empty_list(self):
        """Тест: порожній масив."""
        iterations, upper_bound = binary_search([], 5.0)
        self.assertEqual(iterations, 0)
        self.assertIsNone(upper_bound)

    def test_single_element_match(self):
        """Тест: масив з одним елементом, точний збіг."""
        iterations, upper_bound = binary_search([5.5], 5.5)
        self.assertEqual(upper_bound, 5.5)
        self.assertEqual(iterations, 1)

    def test_single_element_no_match(self):
        """Тест: масив з одним елементом, без збігу (більше за значення)."""
        iterations, upper_bound = binary_search([5.5], 6.0)
        self.assertIsNone(upper_bound)
        self.assertEqual(iterations, 1)

    def test_duplicates(self):
        """Тест: масив з дублікатами."""
        # Повинен повернути 2.0, оскільки 2.0 >= 2.0
        arr = [1.0, 2.0, 2.0, 3.0]
        iterations, upper_bound = binary_search(arr, 2.0)
        self.assertEqual(upper_bound, 2.0)

    def test_bad_input_none_list(self):
        """Bad Input: передано None замість списку."""
        with self.assertRaises(TypeError):
            binary_search(None, 10)

    def test_bad_input_incompatible_types(self):
        """Bad Input: порівняння чисел з рядками (викличе TypeError в Python 3)."""
        arr = [1, 2, 3]
        target = "string"
        with self.assertRaises(TypeError):
            binary_search(arr, target)

    def test_bad_input_unsortable_elements_in_list(self):
        """Bad Input: список містить несумісні типи, пошук дійде до порівняння і впаде."""
        arr = [1, "mixed", 3]
        target = 2
        # Залежно від того, куди потрапить mid, може впасти або ні.
        # Але якщо ми спробуємо порівняти 2 з "mixed", буде помилка.
        # При 3 елементах mid=1 -> arr[1]="mixed". 
        with self.assertRaises(TypeError):
            binary_search(arr, target)

if __name__ == '__main__':
    unittest.main()
