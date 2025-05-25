"""
Завдання 1: Додати метод delete для видалення пар ключ-значення в HashTable

Реалізація хеш-таблиці з методом видалення, що використовує метод ланцюжків 
для розв'язання колізій.
"""

class HashTable:
    def __init__(self, size):
        """
        Ініціалізує хеш-таблицю заданого розміру.
        
        Args:
            size (int): Розмір хеш-таблиці
        """
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def hash_function(self, key):
        """
        Хеш-функція для перетворення ключа в індекс таблиці.
        
        Args:
            key: Ключ для хешування
            
        Returns:
            int: Індекс в таблиці
        """
        return hash(key) % self.size

    def insert(self, key, value):
        """
        Вставляє пару ключ-значення в хеш-таблицю.
        
        Args:
            key: Ключ для вставки
            value: Значення для вставки
            
        Returns:
            bool: True, якщо операція успішна
        """
        key_hash = self.hash_function(key)
        key_value = [key, value]

        if not self.table[key_hash]:
            self.table[key_hash] = [key_value]
            return True
        else:
            # Перевіряємо, чи існує вже такий ключ
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    pair[1] = value  # Оновлюємо значення
                    return True
            # Якщо ключ не знайдено, додаємо нову пару
            self.table[key_hash].append(key_value)
            return True

    def get(self, key):
        """
        Повертає значення за ключем.
        
        Args:
            key: Ключ для пошуку
            
        Returns:
            Значення, пов'язане з ключем, або None, якщо ключ не знайдено
        """
        key_hash = self.hash_function(key)
        if self.table[key_hash]:
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None

    def delete(self, key):
        """
        Видаляє пару ключ-значення з хеш-таблиці.
        
        Args:
            key: Ключ для видалення
            
        Returns:
            bool: True, якщо ключ було знайдено та видалено, False - інакше
        """
        key_hash = self.hash_function(key)
        
        # Перевіряємо, чи існує ланцюжок за цим індексом
        if not self.table[key_hash]:
            return False
        
        # Шукаємо ключ у ланцюжку
        for i, pair in enumerate(self.table[key_hash]):
            if pair[0] == key:
                # Видаляємо пару зі списку
                del self.table[key_hash][i]
                return True
        
        # Ключ не знайдено
        return False

    def display(self):
        """
        Виводить весь вміст хеш-таблиці для відладки.
        """
        print("Хеш-таблиця:")
        for i, bucket in enumerate(self.table):
            if bucket:
                print(f"  Індекс {i}: {bucket}")
            else:
                print(f"  Індекс {i}: порожньо")

    def keys(self):
        """
        Повертає список всіх ключів у хеш-таблиці.
        
        Returns:
            list: Список всіх ключів
        """
        all_keys = []
        for bucket in self.table:
            for pair in bucket:
                all_keys.append(pair[0])
        return all_keys

    def values(self):
        """
        Повертає список всіх значень у хеш-таблиці.
        
        Returns:
            list: Список всіх значень
        """
        all_values = []
        for bucket in self.table:
            for pair in bucket:
                all_values.append(pair[1])
        return all_values

    def items(self):
        """
        Повертає список всіх пар ключ-значення у хеш-таблиці.
        
        Returns:
            list: Список кортежів (ключ, значення)
        """
        all_items = []
        for bucket in self.table:
            for pair in bucket:
                all_items.append((pair[0], pair[1]))
        return all_items

    def __len__(self):
        """
        Повертає кількість елементів у хеш-таблиці.
        
        Returns:
            int: Кількість елементів
        """
        count = 0
        for bucket in self.table:
            count += len(bucket)
        return count

    def __contains__(self, key):
        """
        Перевіряє, чи містить хеш-таблиця заданий ключ.
        
        Args:
            key: Ключ для перевірки
            
        Returns:
            bool: True, якщо ключ існує, False - інакше
        """
        return self.get(key) is not None


def test_hashtable():
    """
    Тестує функціональність хеш-таблиці, включаючи метод delete.
    """
    print("🔧 Тестування HashTable з методом delete")
    print("=" * 50)
    
    # Створюємо хеш-таблицю
    H = HashTable(5)
    
    # Тестуємо вставку
    print("📝 Вставляємо елементи:")
    test_data = [
        ("apple", 10),
        ("orange", 20),
        ("banana", 30),
        ("grape", 40),
        ("cherry", 50),
        ("mango", 60)
    ]
    
    for key, value in test_data:
        H.insert(key, value)
        print(f"   Вставлено: {key} = {value}")
    
    print(f"\n📊 Кількість елементів: {len(H)}")
    print("🗂️  Всі ключі:", H.keys())
    
    # Відображаємо поточний стан
    print("\n🔍 Поточний стан хеш-таблиці:")
    H.display()
    
    # Тестуємо пошук
    print("\n🔎 Тестуємо пошук:")
    search_keys = ["apple", "banana", "nonexistent"]
    for key in search_keys:
        value = H.get(key)
        print(f"   {key}: {value if value is not None else 'не знайдено'}")
    
    # Тестуємо видалення
    print("\n🗑️  Тестуємо видалення:")
    
    # Видаляємо існуючий ключ
    print("   Видаляємо 'banana':")
    result = H.delete("banana")
    print(f"   Результат: {'успішно' if result else 'не вдалося'}")
    print(f"   Перевірка: banana = {H.get('banana')}")
    
    # Спробуємо видалити неіснуючий ключ
    print("\n   Спробуємо видалити 'nonexistent':")
    result = H.delete("nonexistent")
    print(f"   Результат: {'успішно' if result else 'не вдалося'}")
    
    # Видаляємо ще кілька ключів
    print("\n   Видаляємо 'apple' та 'grape':")
    for key in ["apple", "grape"]:
        result = H.delete(key)
        print(f"   {key}: {'видалено' if result else 'не знайдено'}")
    
    # Показуємо фінальний стан
    print(f"\n📊 Кількість елементів після видалення: {len(H)}")
    print("🗂️  Залишилися ключі:", H.keys())
    print("💎 Залишилися значення:", H.values())
    
    print("\n🔍 Фінальний стан хеш-таблиці:")
    H.display()
    
    # Тестуємо оператор in
    print("\n🔍 Тестуємо оператор 'in':")
    test_keys = ["orange", "banana", "cherry"]
    for key in test_keys:
        exists = key in H
        print(f"   '{key}' в таблиці: {exists}")
    
    # Тестуємо колізії (додаємо елементи, що можуть мати колізії)
    print("\n⚡ Тестуємо обробку колізій:")
    H.insert("test1", 100)
    H.insert("test2", 200)
    H.display()
    
    # Видаляємо один з елементів з колізією
    print("\n   Видаляємо один елемент з можливою колізією:")
    H.delete("test1")
    print(f"   test1 після видалення: {H.get('test1')}")
    print(f"   test2 після видалення test1: {H.get('test2')}")


def demo_edge_cases():
    """
    Демонструє роботу з граничними випадками.
    """
    print("\n" + "=" * 50)
    print("🧪 Тестування граничних випадків")
    print("=" * 50)
    
    H = HashTable(3)  # Маленька таблиця для демонстрації колізій
    
    # Заповнюємо таблицю
    items = [("a", 1), ("b", 2), ("c", 3), ("d", 4), ("e", 5)]
    for key, value in items:
        H.insert(key, value)
    
    print("📦 Заповнена таблиця:")
    H.display()
    
    # Видаляємо всі елементи
    print("\n🗑️  Видаляємо всі елементи:")
    for key, _ in items:
        result = H.delete(key)
        print(f"   Видалено {key}: {result}")
    
    print(f"\n📊 Розмір після повного очищення: {len(H)}")
    H.display()
    
    # Спробуємо видалити з порожньої таблиці
    print("\n🚫 Спроба видалення з порожньої таблиці:")
    result = H.delete("nonexistent")
    print(f"   Результат: {result}")


if __name__ == "__main__":
    test_hashtable()
    demo_edge_cases()
    
    print("\n✅ Тестування завершено!")
    print("\n💡 Ключові особливості реалізації методу delete:")
    print("   • Використовує хеш-функцію для знаходження правильного індексу")
    print("   • Перебирає ланцюжок для знаходження потрібного ключа")
    print("   • Видаляє елемент зі списку та повертає True при успіху")
    print("   • Повертає False, якщо ключ не знайдено")
    print("   • Правильно обробляє колізії та порожні ланцюжки")
