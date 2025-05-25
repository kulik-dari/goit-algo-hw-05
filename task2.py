"""
Завдання 2: Двійковий пошук для відсортованого масиву з дробовими числами

Функція повертає кортеж з кількістю ітерацій та "верхньою межею" - 
найменшим елементом, який є більшим або рівним заданому значенню.
"""

def binary_search_with_upper_bound(arr, target):
    """
    Виконує двійковий пошук з поверненням кількості ітерацій та верхньої межі.
    
    Args:
        arr (list): Відсортований масив дробових чисел
        target (float): Значення для пошуку
        
    Returns:
        tuple: (кількість_ітерацій, верхня_межа)
            - кількість_ітерацій: кількість ітерацій, потрібних для пошуку
            - верхня_межа: найменший елемент >= target, або None якщо такого немає
    """
    if not arr:
        return (0, None)
    
    left = 0
    right = len(arr) - 1
    iterations = 0
    upper_bound = None
    
    while left <= right:
        iterations += 1
        mid = (left + right) // 2
        
        if arr[mid] == target:
            # Знайшли точне значення - воно і є верхньою межею
            return (iterations, arr[mid])
        elif arr[mid] < target:
            left = mid + 1
        else:
            # arr[mid] > target - це потенційна верхня межа
            upper_bound = arr[mid]
            right = mid - 1
    
    # Якщо не знайшли точне значення, але знайшли верхню межу
    if upper_bound is not None:
        return (iterations, upper_bound)
    
    # Якщо верхня межа не знайдена, перевіряємо, чи є елементи більші за target
    for element in arr:
        if element >= target:
            return (iterations, element)
    
    # Всі елементи менші за target
    return (iterations, None)


def binary_search_detailed(arr, target):
    """
    Детальна версія двійкового пошуку з логуванням кроків.
    
    Args:
        arr (list): Відсортований масив
        target (float): Значення для пошуку
        
    Returns:
        tuple: (кількість_ітерацій, верхня_межа, лог_кроків)
    """
    if not arr:
        return (0, None, ["Масив порожній"])
    
    left = 0
    right = len(arr) - 1
    iterations = 0
    upper_bound = None
    log = []
    
    log.append(f"Початковий масив: {arr}")
    log.append(f"Шукаємо: {target}")
    
    while left <= right:
        iterations += 1
        mid = (left + right) // 2
        
        log.append(f"Ітерація {iterations}: left={left}, right={right}, mid={mid}")
        log.append(f"  arr[{mid}] = {arr[mid]}")
        
        if arr[mid] == target:
            log.append(f"  Знайдено точне значення!")
            return (iterations, arr[mid], log)
        elif arr[mid] < target:
            log.append(f"  {arr[mid]} < {target}, рухаємося вправо")
            left = mid + 1
        else:
            log.append(f"  {arr[mid]} > {target}, рухаємося вліво")
            upper_bound = arr[mid]
            log.append(f"  Нова верхня межа: {upper_bound}")
            right = mid - 1
    
    if upper_bound is not None:
        log.append(f"Верхня межа знайдена: {upper_bound}")
        return (iterations, upper_bound, log)
    
    # Якщо верхня межа не знайдена під час пошуку, шукаємо мінімальний елемент >= target
    for element in arr:
        if element >= target:
            log.append(f"Верхня межа (лінійний пошук): {element}")
            return (iterations, element, log)
    
    log.append("Верхня межа не знайдена - всі елементи менші за target")
    return (iterations, None, log)


def test_binary_search():
    """
    Тестує функцію двійкового пошуку на різних випадках.
    """
    print("🔍 Тестування двійкового пошуку з верхньою межею")
    print("=" * 60)
    
    # Тестові масиви
    test_arrays = [
        [1.1, 2.3, 3.5, 4.7, 5.9, 7.1, 8.3, 9.5],
        [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0],
        [10.0, 20.0, 30.0, 40.0, 50.0],
        [3.14159, 2.71828, 1.41421, 0.57722],  # Несортований для демонстрації
        []  # Порожній масив
    ]
    
    # Сортуємо несортований масив
    test_arrays[3] = sorted(test_arrays[3])
    
    test_cases = [
        # (масив_індекс, значення_для_пошуку, опис)
        (0, 3.5, "точне значення в середині"),
        (0, 3.6, "значення між елементами"),
        (0, 0.5, "значення менше мінімального"),
        (0, 10.0, "значення більше максимального"),
        (0, 1.1, "точне значення на початку"),
        (0, 9.5, "точне значення в кінці"),
        (1, 2.25, "значення між елементами"),
        (1, 5.5, "значення більше максимального"),
        (2, 25.0, "значення між елементами"),
        (2, 5.0, "значення менше мінімального"),
        (3, 1.5, "значення в відсортованому масиві"),
        (4, 1.0, "пошук в порожньому масиві"),
    ]
    
    for i, (arr_idx, target, description) in enumerate(test_cases, 1):
        print(f"\n📋 Тест {i}: {description}")
        
        if arr_idx < len(test_arrays):
            arr = test_arrays[arr_idx]
            print(f"   Масив: {arr}")
            print(f"   Шукаємо: {target}")
            
            iterations, upper_bound = binary_search_with_upper_bound(arr, target)
            
            print(f"   ✅ Результат: ({iterations} ітерацій, верхня межа: {upper_bound})")
            
            # Перевірка правильності
            if upper_bound is not None:
                # Перевіряємо, що upper_bound >= target
                if upper_bound >= target:
                    print(f"   ✓ Верхня межа коректна: {upper_bound} >= {target}")
                else:
                    print(f"   ✗ Помилка: {upper_bound} < {target}")
                
                # Перевіряємо, що це найменший такий елемент
                smaller_elements = [x for x in arr if x >= target and x < upper_bound]
                if not smaller_elements:
                    print(f"   ✓ Це найменший елемент >= {target}")
                else:
                    print(f"   ✗ Знайдено менші елементи: {smaller_elements}")
            else:
                # Перевіряємо, що дійсно немає елементів >= target
                valid_elements = [x for x in arr if x >= target]
                if not valid_elements:
                    print(f"   ✓ Коректно: немає елементів >= {target}")
                else:
                    print(f"   ✗ Помилка: знайдено елементи >= {target}: {valid_elements}")


def demo_detailed_search():
    """
    Демонструє детальний пошук з логуванням.
    """
    print("\n" + "=" * 60)
    print("🔬 Детальна демонстрація пошуку")
    print("=" * 60)
    
    arr = [1.1, 2.3, 3.5, 4.7, 5.9, 7.1, 8.3, 9.5]
    targets = [3.6, 7.1, 0.5, 10.0]
    
    for target in targets:
        print(f"\n🎯 Детальний пошук для {target}:")
        print("-" * 40)
        
        iterations, upper_bound, log = binary_search_detailed(arr, target)
        
        for line in log:
            print(f"   {line}")
        
        print(f"\n   📊 Підсумок:")
        print(f"   • Ітерацій: {iterations}")
        print(f"   • Верхня межа: {upper_bound}")


def benchmark_search():
    """
    Порівнює ефективність двійкового пошуку з лінійним.
    """
    import time
    import random
    
    print("\n" + "=" * 60)
    print("⚡ Порівняння ефективності")
    print("=" * 60)
    
    # Створюємо великий відсортований масив
    size = 100000
    arr = sorted([random.uniform(0, 1000) for _ in range(size)])
    
    # Тестові значення
    test_targets = [random.uniform(0, 1000) for _ in range(1000)]
    
    # Лінійний пошук верхньої межі
    def linear_search_upper_bound(arr, target):
        iterations = 0
        for element in arr:
            iterations += 1
            if element >= target:
                return iterations, element
        return iterations, None
    
    print(f"📊 Тестуємо на масиві з {size:,} елементів")
    print(f"🎯 Виконуємо {len(test_targets)} пошуків")
    
    # Двійковий пошук
    start_time = time.time()
    binary_results = []
    total_binary_iterations = 0
    
    for target in test_targets:
        iterations, upper_bound = binary_search_with_upper_bound(arr, target)
        binary_results.append((iterations, upper_bound))
        total_binary_iterations += iterations
    
    binary_time = time.time() - start_time
    
    # Лінійний пошук (тестуємо на меншій кількості для швидкості)
    small_test = test_targets[:100]  # Тестуємо тільки 100 випадків
    start_time = time.time()
    linear_results = []
    total_linear_iterations = 0
    
    for target in small_test:
        iterations, upper_bound = linear_search_upper_bound(arr, target)
        linear_results.append((iterations, upper_bound))
        total_linear_iterations += iterations
    
    linear_time = time.time() - start_time
    
    print(f"\n📈 Результати:")
    print(f"   Двійковий пошук:")
    print(f"     • Час: {binary_time:.4f} сек")
    print(f"     • Середня кількість ітерацій: {total_binary_iterations/len(test_targets):.1f}")
    print(f"     • Загальна кількість ітерацій: {total_binary_iterations:,}")
    
    print(f"   Лінійний пошук (100 тестів):")
    print(f"     • Час: {linear_time:.4f} сек")
    print(f"     • Середня кількість ітерацій: {total_linear_iterations/len(small_test):.1f}")
    print(f"     • Прогнозований час для всіх тестів: {linear_time * 10:.4f} сек")
    
    speedup = (linear_time * 10) / binary_time
    print(f"   ⚡ Прискорення: {speedup:.1f}x")


if __name__ == "__main__":
    test_binary_search()
    demo_detailed_search()
    benchmark_search()
    
    print("\n✅ Тестування завершено!")
    print("\n💡 Ключові особливості реалізації:")
    print("   • Повертає кількість ітерацій та верхню межу")
    print("   • Верхня межа - найменший елемент >= target")
    print("   • Обробляє випадки, коли верхня межа відсутня")
    print("   • Ефективність O(log n) порівняно з O(n) лінійного пошуку")
