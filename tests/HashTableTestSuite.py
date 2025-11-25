import unittest
import sys
import os

# Додаємо кореневу директорію до шляху пошуку модулів, щоб імпортувати hash_table
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hash_table import HashTable

class TestHashTable(unittest.TestCase):
    def setUp(self):
        # Ініціалізуємо таблицю перед кожним тестом
        self.ht = HashTable(10)

    def test_initialization(self):
        """Перевірка коректності створення таблиці."""
        self.assertEqual(self.ht.size, 10)
        self.assertEqual(len(self.ht.table), 10)
        # Переконуємося, що всі елементи - це порожні списки
        for bucket in self.ht.table:
            self.assertEqual(bucket, [])

    def test_insert_and_get_simple(self):
        """Базова перевірка вставки та отримання."""
        self.assertTrue(self.ht.insert("apple", 10))
        self.assertTrue(self.ht.insert("banana", 20))
        
        self.assertEqual(self.ht.get("apple"), 10)
        self.assertEqual(self.ht.get("banana"), 20)

    def test_insert_update_existing(self):
        """Перевірка оновлення значення для існуючого ключа."""
        self.ht.insert("apple", 10)
        self.ht.insert("apple", 50)  # Оновлюємо
        
        self.assertEqual(self.ht.get("apple"), 50)
        # Перевіряємо, що дублікатів не створено в кошику
        key_hash = self.ht.hash_function("apple")
        bucket = self.ht.table[key_hash]
        self.assertEqual(len(bucket), 1)

    def test_get_non_existent(self):
        """Спроба отримати неіснуючий ключ."""
        self.assertIsNone(self.ht.get("cherry"))

    def test_collisions_handling(self):
        """Перевірка роботи з колізіями (малий розмір таблиці)."""
        # Створюємо дуже маленьку таблицю, щоб гарантувати колізії
        small_ht = HashTable(2) 
        # Вставляємо 3 елементи, за принципом Діріхле мінімум один кошик матиме >1 елемента
        small_ht.insert("key1", "val1")
        small_ht.insert("key2", "val2")
        small_ht.insert("key3", "val3")

        self.assertEqual(small_ht.get("key1"), "val1")
        self.assertEqual(small_ht.get("key2"), "val2")
        self.assertEqual(small_ht.get("key3"), "val3")

    def test_delete_success(self):
        """Успішне видалення."""
        self.ht.insert("apple", 10)
        self.assertTrue(self.ht.delete("apple"))
        self.assertIsNone(self.ht.get("apple"))

    def test_delete_fail_non_existent(self):
        """Видалення неіснуючого ключа."""
        self.assertFalse(self.ht.delete("ghost"))

    def test_delete_in_collision_chain(self):
        """Видалення елемента зі списку колізій."""
        # Форсуємо колізію, використовуючи малий розмір
        small_ht = HashTable(1)
        small_ht.insert("A", 1)
        small_ht.insert("B", 2)
        small_ht.insert("C", 3)
        
        # Видаляємо елемент з середини ланцюжка
        self.assertTrue(small_ht.delete("B"))
        
        self.assertEqual(small_ht.get("A"), 1)
        self.assertIsNone(small_ht.get("B"))
        self.assertEqual(small_ht.get("C"), 3)

    def test_bad_input_unhashable_key(self):
        """Спроба використати mutable тип (список) як ключ."""
        with self.assertRaises(TypeError):
            self.ht.insert(["list", "is", "unhashable"], 100)

    def test_none_as_key(self):
        """None є валідним хешованим ключем в Python."""
        self.ht.insert(None, "void")
        self.assertEqual(self.ht.get(None), "void")
        self.assertTrue(self.ht.delete(None))

    def test_bad_input_zero_size(self):
        """Створення таблиці з розміром 0 (має викликати помилку при хешуванні)."""
        ht_zero = HashTable(0)
        # Це викличе ZeroDivisionError всередині hash_function: hash(key) % 0
        with self.assertRaises(ZeroDivisionError):
            ht_zero.insert("test", 1)

    def test_str_representation(self):
        """Перевірка строкового представлення."""
        self.ht.insert("a", 1)
        representation = str(self.ht)
        self.assertIn("['a', 1]", representation)

    def test_coverage_manual_none_bucket(self):
        """
        Технічний тест для покриття гілки `if self.table[key_hash] is None`.
        У поточному __init__ це неможливо штатно, тому ми емулюємо ситуацію.
        """
        key = "test_none"
        key_hash = self.ht.hash_function(key)
        # Вручну ламаємо структуру, щоб перевірити логіку відновлення (якщо вона передбачена)
        self.ht.table[key_hash] = None 
        
        self.ht.insert(key, "restored")
        # Перевіряємо, чи вставилось воно як список
        self.assertEqual(self.ht.get(key), "restored")
        self.assertIsInstance(self.ht.table[key_hash], list)

if __name__ == '__main__':
    unittest.main()
