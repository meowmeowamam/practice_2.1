import math
from datetime import datetime

try:
    with open('resource/calculator.log', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    if not lines:
        print("Лог-файл пуст. История операций отсутствует.")
    else:
        last_lines = lines[-5:] if len(lines) >= 5 else lines
        print("ПОСЛЕДНИЕ 5 ОПЕРАЦИЙ:")
        for line in last_lines:
            print(line.strip())
except FileNotFoundError:
    print("Лог-файл ещё не создан. История операций отсутствует.")

print("\nКАЛЬКУЛЯТОР С ЛОГИРОВАНИЕМ")
while True:
    print("\nДоступные операции:")
    print("   +  - сложение")
    print("   -  - вычитание")
    print("   *  - умножение")
    print("   /  - деление")
    print("  log - натуральный логарифм (ln x)")
    print("  sin - синус (в радианах)")
    print("clear - очистить лог-файл")
    print(" exit - выход из программы")

    operation = input('Введите операцию: ').strip().lower()

    match operation:
        case '+' | '-' | '*' | '/':
            try:
                num1 = float(input('\nВведите первое число: '))
                num2 = float(input('Введите второе число: '))

                match operation:
                    case '+':
                        result = num1 + num2
                    case '-':
                        result = num1 - num2
                    case '*':
                        result = num1 * num2
                    case '/':
                        if num2 == 0:
                            print("\nОшибка: Деление на ноль невозможно.")
                            continue
                        result = num1 / num2

                ex = f'{num1} {operation} {num2}'
                print(f'Результат: {ex} = {result}')

                timestp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                with open('resource/calculator.log', 'a', encoding='utf-8') as f:
                    f.write(f'[{timestp}] {ex} = {result}\n')
            except ValueError:
                print('\nОшибка: Введите корректные числа.')
        case 'log' | 'sin':
            try:
                num = float(input('\nВведите число: '))

                match operation:
                    case 'log':
                        if num <= 0:
                            print('\nОшибка: Логарифм определён только для положительных чисел.')
                            continue
                        result = math.log(num)
                        ex = f'ln({num})'
                    case 'sin':
                        result = math.sin(num)
                        ex = f'sin({num})'

                print(f'Результат: {ex} = {result}')

                timestp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                with open('resource/calculator.log', 'a', encoding='utf-8') as f:
                    f.write(f'[{timestp}] {ex} = {result}\n')
            except ValueError:
                print(f'\nОшибка: Введите корректное число.')
        case 'clear':
            try:
                with open('resource/calculator.log', 'w') as f:
                    pass
                print('\nЛог-файл успешно очищен.')
            except Exception as e:
                print(f'\nОшибка при очистке лог-файла: {e}')
        case 'exit':
            print('\nРабота программы завершена.')
            break
        case _:
            print('\nОшибка: Неверная операция. Попробуйте снова.')
