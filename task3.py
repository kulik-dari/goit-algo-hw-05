"""
Завдання 3: Порівняння ефективності алгоритмів пошуку підрядка

Реалізація та порівняння алгоритмів:
- Боєра-Мура (Boyer-Moore)
- Кнута-Морріса-Пратта (Knuth-Morris-Pratt)
- Рабіна-Карпа (Rabin-Karp)
"""

import timeit
import hashlib


def boyer_moore_search(text, pattern):
    """
    Алгоритм пошуку підрядка Боєра-Мура.
    
    Args:
        text (str): Текст для пошуку
        pattern (str): Підрядок для знаходження
        
    Returns:
        list: Список позицій, де знайдено підрядок
    """
    def build_bad_char_table(pattern):
        """Будує таблицю зсувів для поганих символів."""
        table = {}
        for i in range(len(pattern)):
            table[pattern[i]] = i
        return table
    
    if not pattern:
        return []
    
    bad_char_table = build_bad_char_table(pattern)
    positions = []
    i = 0
    
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1
        
        # Порівнюємо з кінця шаблону
        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1
        
        if j < 0:
            # Знайдено збіг
            positions.append(i)
            i += 1
        else:
            # Використовуємо правило поганого символа
            bad_char = text[i + j]
            if bad_char in bad_char_table:
                i += max(1, j - bad_char_table[bad_char])
            else:
                i += j + 1
    
    return positions


def kmp_search(text, pattern):
    """
    Алгоритм пошуку підрядка Кнута-Морріса-Пратта.
    
    Args:
        text (str): Текст для пошуку
        pattern (str): Підрядок для знаходження
        
    Returns:
        list: Список позицій, де знайдено підрядок
    """
    def build_lps_array(pattern):
        """Будує масив найдовших префіксів-суфіксів."""
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
    
    if not pattern:
        return []
    
    lps = build_lps_array(pattern)
    positions = []
    i = 0  # індекс для тексту
    j = 0  # індекс для шаблону
    
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        
        if j == len(pattern):
            positions.append(i - j)
            j = lps[j - 1]
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    
    return positions


def rabin_karp_search(text, pattern):
    """
    Алгоритм пошуку підрядка Рабіна-Карпа.
    
    Args:
        text (str): Текст для пошуку
        pattern (str): Підрядок для знаходження
        
    Returns:
        list: Список позицій, де знайдено підрядок
    """
    if not pattern:
        return []
    
    # Параметри для хешування
    d = 256  # кількість символів в алфавіті
    q = 101  # просте число для модуля
    
    pattern_len = len(pattern)
    text_len = len(text)
    pattern_hash = 0
    text_hash = 0
    h = 1
    positions = []
    
    # Обчислюємо h = pow(d, pattern_len-1) % q
    for i in range(pattern_len - 1):
        h = (h * d) % q
    
    # Обчислюємо хеш шаблону та першого вікна тексту
    for i in range(pattern_len):
        pattern_hash = (d * pattern_hash + ord(pattern[i])) % q
        text_hash = (d * text_hash + ord(text[i])) % q
    
    # Ковзаємо шаблон по тексту
    for i in range(text_len - pattern_len + 1):
        # Перевіряємо хеші
        if pattern_hash == text_hash:
            # Перевіряємо символи один за одним
            if text[i:i + pattern_len] == pattern:
                positions.append(i)
        
        # Обчислюємо хеш для наступного вікна
        if i < text_len - pattern_len:
            text_hash = (d * (text_hash - ord(text[i]) * h) + ord(text[i + pattern_len])) % q
            if text_hash < 0:
                text_hash += q
    
    return positions


def load_text_files():
    """
    Завантажує текстові файли для тестування з обробкою різних кодувань.
    
    Returns:
        tuple: (текст1, текст2)
    """
    def try_read_file(filename):
        """Спробує прочитати файл з різними кодуваннями."""
        encodings = ['utf-8', 'cp1251', 'latin-1', 'cp866', 'utf-16']
        
        for encoding in encodings:
            try:
                with open(filename, 'r', encoding=encoding) as f:
                    content = f.read()
                    print(f"✅ Файл '{filename}' прочитано з кодуванням {encoding}")
                    return content
            except (FileNotFoundError, UnicodeDecodeError):
                continue
        
        # Якщо жоден варіант не спрацював
        print(f"⚠️  Не вдалося прочитати файл '{filename}', використовуємо зразок тексту")
        return None
    
    # Спробуємо завантажити перший файл
    text1 = try_read_file('стаття1.txt')
    if text1 is None:
        text1 = """
        Використання алгоритмів у бібліотеках мов програмування
        За всю історію комп'ютерних наук склалося розуміння, які алгоритми та структури даних 
        потрібні для вирішення практичних завдань. Алгоритми сортування використовуються 
        повсюдно: товари в магазині сортують за вартістю або терміну придатності, 
        а ресторани – за віддаленістю або рейтингу. Хеш-таблиці допомагають перевірити 
        коректність пароля та не зберігати його на сайті у відкритому вигляді.
        Двійковий пошук часто використовується через швидкий час пошуку. Цей вид пошуку 
        вимагає попереднього сортування набору даних. Алгоритм ділить вхідну колекцію 
        на рівні половини, і з кожною ітерацією порівнює цільовий елемент з елементом у середині.
        Жадібний алгоритм – метод розв'язання оптимізаційних задач, заснований на тому, 
        що процес прийняття рішення можна розбити на елементарні кроки.
        Лінійний пошук – найпростіший алгоритм пошуку, який рідко використовується через 
        свою неефективність. Це метод повного перебору, і він поступається іншим алгоритмам.
        Інтерполяційний пошук використовується для пошуку елементів у відсортованому масиві.
        Експоненціальний пошук використовується для пошуку елементів шляхом переходу в 
        експоненціальні позиції. Жадібні алгоритми відіграють важливу роль у теорії алгоритмів.
        """ * 10  # Повторюємо для збільшення розміру
    
    # Спробуємо завантажити другий файл
    text2 = try_read_file('стаття2.txt')
    if text2 is None:
        text2 = """
        Методи та структури даних для реалізації бази даних рекомендаційної системи
        Рекомендаційні системи є важливою складовою соціальних мереж та значним чином 
        впливають на те, яким користувачі сприймають інформаційний простір. Вибір методу 
        представлення даних має важливе значення для ефективності системи.
        Зв'язний список – це структура даних, у якій кожен елемент має вказівник на наступний. 
        Розгорнутий зв'язний список – це зв'язний список, кожен елемент якого містить масив елементів.
        Хеш-таблиця – це структура даних, у якій пошук елементу здійснюється на основі його ключа.
        B-дерево – це збалансоване, сильно розгалуджене дерево пошуку. B+-дерево зберігає 
        усі значення у листкових вузлах та має посилання на сусідів.
        Бінарні діаграми рішень – це економна форма представлення булевих функцій.
        Профілювання показало, що 75% часу роботи тесту варіанту з розгорнутим списком 
        зайняло генерування випадкових даних для програмного імітаційного моделювання.
        Структура розгорнутого списку дуже проста, тож це дасть можливість використовувати 
        багатопотокову роботу без блокувань.
        """ * 10
    
    return text1, text2


def benchmark_algorithms(text, existing_pattern, fake_pattern, text_name):
    """
    Порівнює швидкість алгоритмів пошуку.
    
    Args:
        text (str): Текст для пошуку
        existing_pattern (str): Підрядок, що існує в тексті
        fake_pattern (str): Вигаданий підрядок
        text_name (str): Назва тексту для звіту
        
    Returns:
        dict: Результати вимірювань
    """
    algorithms = {
        'Boyer-Moore': boyer_moore_search,
        'KMP': kmp_search,
        'Rabin-Karp': rabin_karp_search
    }
    
    results = {}
    
    print(f"\n🔍 Тестування на {text_name}")
    print("-" * 50)
    print(f"📊 Розмір тексту: {len(text):,} символів")
    print(f"🎯 Існуючий підрядок: '{existing_pattern}' (довжина: {len(existing_pattern)})")
    print(f"🎭 Вигаданий підрядок: '{fake_pattern}' (довжина: {len(fake_pattern)})")
    
    for alg_name, alg_func in algorithms.items():
        print(f"\n🔬 Тестуємо {alg_name}:")
        
        # Тест на існуючому підрядку
        positions_existing = alg_func(text, existing_pattern)
        time_existing = timeit.timeit(
            lambda: alg_func(text, existing_pattern), 
            number=10
        ) / 10
        
        # Тест на вигаданому підрядку
        positions_fake = alg_func(text, fake_pattern)
        time_fake = timeit.timeit(
            lambda: alg_func(text, fake_pattern), 
            number=10
        ) / 10
        
        results[alg_name] = {
            'existing_time': time_existing,
            'fake_time': time_fake,
            'existing_count': len(positions_existing),
            'fake_count': len(positions_fake)
        }
        
        print(f"   📍 Існуючий: {len(positions_existing)} збігів, {time_existing:.6f} сек")
        print(f"   🚫 Вигаданий: {len(positions_fake)} збігів, {time_fake:.6f} сек")
    
    return results


def analyze_results(results1, results2, text1_name, text2_name):
    """
    Аналізує та виводить підсумкові результати.
    
    Args:
        results1 (dict): Результати для першого тексту
        results2 (dict): Результати для другого тексту
        text1_name (str): Назва першого тексту
        text2_name (str): Назва другого тексту
    """
    print(f"\n" + "="*70)
    print("📊 ПІДСУМКОВИЙ АНАЛІЗ РЕЗУЛЬТАТІВ")
    print("="*70)
    
    algorithms = list(results1.keys())
    
    # Аналіз для кожного тексту окремо
    for results, text_name in [(results1, text1_name), (results2, text2_name)]:
        print(f"\n🔸 {text_name}:")
        
        # Найшвидший для існуючих підрядків
        fastest_existing = min(algorithms, key=lambda x: results[x]['existing_time'])
        print(f"   🏆 Найшвидший (існуючий підрядок): {fastest_existing}")
        print(f"      Час: {results[fastest_existing]['existing_time']:.6f} сек")
        
        # Найшвидший для вигаданих підрядків
        fastest_fake = min(algorithms, key=lambda x: results[x]['fake_time'])
        print(f"   🏆 Найшвидший (вигаданий підрядок): {fastest_fake}")
        print(f"      Час: {results[fastest_fake]['fake_time']:.6f} сек")
        
        # Детальна таблиця
        print(f"   📋 Детальні результати:")
        print(f"      {'Алгоритм':<15} {'Існуючий (сек)':<15} {'Вигаданий (сек)':<15}")
        print(f"      {'-'*45}")
        for alg in algorithms:
            existing_time = results[alg]['existing_time']
            fake_time = results[alg]['fake_time']
            print(f"      {alg:<15} {existing_time:<15.6f} {fake_time:<15.6f}")
    
    # Загальний аналіз
    print(f"\n🔸 Загальний аналіз:")
    
    # Середні часи для всіх тестів
    avg_times = {}
    for alg in algorithms:
        total_time = (results1[alg]['existing_time'] + results1[alg]['fake_time'] + 
                     results2[alg]['existing_time'] + results2[alg]['fake_time'])
        avg_times[alg] = total_time / 4
    
    fastest_overall = min(avg_times.keys(), key=lambda x: avg_times[x])
    print(f"   🏆 Найшвидший загалом: {fastest_overall}")
    print(f"   📊 Середні часи:")
    for alg in sorted(avg_times.keys(), key=lambda x: avg_times[x]):
        print(f"      {alg}: {avg_times[alg]:.6f} сек")
    
    # Відносна швидкість
    print(f"\n   ⚡ Співвідношення швидкості (відносно найповільнішого):")
    slowest_time = max(avg_times.values())
    for alg in sorted(avg_times.keys(), key=lambda x: avg_times[x]):
        speedup = slowest_time / avg_times[alg]
        print(f"      {alg}: {speedup:.2f}x швидше")


def main():
    """
    Головна функція для запуску всіх тестів.
    """
    print("🔍 Порівняння алгоритмів пошуку підрядків")
    print("="*50)
    print("📋 Алгоритми: Boyer-Moore, KMP, Rabin-Karp")
    print("📄 Тестування на двох текстових файлах")
    
    # Завантажуємо тексти
    text1, text2 = load_text_files()
    
    # Визначаємо підрядки для пошуку
    # Існуючі підрядки (знаємо, що вони є в текстах)
    existing_patterns = {
        'text1': 'алгоритм',
        'text2': 'структура даних'
    }
    
    # Вигадані підрядки (ймовірно відсутні)
    fake_patterns = {
        'text1': 'квантовий комп\'ютер',
        'text2': 'нейронна мережа blockchain'
    }
    
    # Тестуємо алгоритми
    results1 = benchmark_algorithms(
        text1, 
        existing_patterns['text1'], 
        fake_patterns['text1'], 
        "Стаття 1 (Алгоритми в бібліотеках)"
    )
    
    results2 = benchmark_algorithms(
        text2, 
        existing_patterns['text2'], 
        fake_patterns['text2'], 
        "Стаття 2 (Структури даних для БД)"
    )
    
    # Аналізуємо результати
    analyze_results(
        results1, results2, 
        "Стаття 1", "Стаття 2"
    )
    
    # Додаткові тести з різними довжинами підрядків
    print(f"\n" + "="*70)
    print("🧪 ДОДАТКОВІ ТЕСТИ З РІЗНИМИ ДОВЖИНАМИ ПІДРЯДКІВ")
    print("="*70)
    
    test_patterns = [
        ('а', 'короткий символ'),
        ('та', 'короткий підрядок'),
        ('алгоритм', 'середній підрядок'),
        ('структура даних', 'довгий підрядок'),
        ('xyz123nonexistent', 'неіснуючий підрядок')
    ]
    
    print(f"📊 Тестування на першому тексті:")
    for pattern, description in test_patterns:
        print(f"\n🔸 {description} ('{pattern}'):")
        
        times = {}
        for alg_name, alg_func in [('Boyer-Moore', boyer_moore_search), 
                                  ('KMP', kmp_search), 
                                  ('Rabin-Karp', rabin_karp_search)]:
            time_taken = timeit.timeit(lambda: alg_func(text1, pattern), number=5) / 5
            times[alg_name] = time_taken
            count = len(alg_func(text1, pattern))
            print(f"   {alg_name}: {time_taken:.6f} сек ({count} збігів)")
        
        fastest = min(times.keys(), key=lambda x: times[x])
        print(f"   🏆 Найшвидший: {fastest}")


if __name__ == "__main__":
    main()
    
    print("\n✅ Тестування завершено!")
    print("\n💡 Висновки:")
    print("   • Boyer-Moore ефективний для довгих підрядків та великих алфавітів")
    print("   • KMP показує стабільну продуктивність для всіх випадків")
    print("   • Rabin-Karp добре працює з короткими підрядками")
    print("   • Результати можуть залежати від характеристик тексту та підрядка")
