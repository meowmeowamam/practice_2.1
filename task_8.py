print('ПРОГРАММА ПОИСКА ЧИСЕЛ, КРАТНЫХ 7')
print('С операцией над числом: x * 100 / (73**2 + 29)')

divider = 7
factor = 100 / (73**2 + 29)
found_count = 0

try:
    with open('resource/numbers.txt', 'r') as f:
        print('\nНайденные числа, кратные 7:')

        cur_sym = ''

        while True:
            sym = f.read(1)

            if not sym:
                if cur_sym:
                    try:
                        num = int(cur_sym)
                        if not num % divider:
                            result = num * factor
                            found_count += 1
                            print(f'{num} -> {result:.5f}')
                    except ValueError:
                        pass
                break

            if sym.isdigit():
                cur_sym += sym

            elif sym == '-':
                if cur_sym:
                    try:
                        num = int(cur_sym)
                        if not num % divider:
                            result = num * factor
                            found_count += 1
                            print(f'{num} -> {result:.5f}')
                    except ValueError:
                        pass
                cur_sym = '-'

            else:
                if cur_sym:
                    try:
                        num = int(cur_sym)
                        if not num % divider:
                            result = num * factor
                            found_count += 1
                            print(f'{num} -> {result:.5f}')
                    except ValueError:
                        pass
                cur_sym = ''

        if not found_count:
            print('Числа, кратные 7, не найдены.')
        else:
            print(f'\nВсего найдено: {found_count}')
except FileNotFoundError:
    print('\nОшибка: Файл "numbers.txt" не найден.')
except Exception as e:
    print(f'\nОшибка при чтении: {e}')