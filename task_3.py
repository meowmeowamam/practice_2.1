import csv

products = []

try:
    with open('resource/products.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            products.append({'Название':row['Название'],
                             'Цена':int(row['Цена']),
                             'Количество':int(row['Количество'])})
    print(f'Загружено {len(products)} товаров из файла.')
except FileNotFoundError:
    print('Ошибка: Файл "products.csv" не найден.')
    exit()
except Exception as e:
    print(f'Ошибка при чтении файла: {e}')
    exit()

while True:
    print('\nМЕНЮ:')
    print('1 - Показать все товары')
    print('2 - Добавить новый товар')
    print('3 - Поиск товара по названию')
    print('4 - Общая стоимость всех товаров')
    print('5 - Сохранить отсортированные продукты по возрастанию цены (отдельный файл)')
    print('6 - Сохранить изменения')
    print('0 - Выйти (без сохранения)')

    choice = input("Выберите действие: ").strip()

    match choice:
        case '1':
            if not products:
                print('\nСписок товаров пуст.')
            else:
                print('\nСПИСОК ВСЕХ ТОВАРОВ:')
                print(f'{'Название':<15} {'Цена':<10} {'Количество':<10} {'Стоимость':<15}')
                for p in products:
                    cost = p['Цена'] * p['Количество']
                    print(f'{p['Название']:<15} {p['Цена']:<10} {p['Количество']:<10} {cost:<10}')
        case '2':
            print('\nДОБАВЛЕНИЕ НОВОГО ТОВАРА')
            name = input('Введите название товара: ').strip()
            if not name or name.isdigit():
                print('\nНазвание не может быть пустым или содержать только цифры.')
                continue

            flag = False
            for p in products:
                if p['Название'].lower() == name.lower():
                    print(f'Товар "{name}" уже существует.')
                    flag = True
                    break
            if flag:
                continue

            try:
                price = int(input('Введите цену: '))
                if price <= 0:
                    print('Цена должна быть положительной.')
                    continue

                qty = int(input('Введите количество: '))
                if qty < 0:
                    print('Количество не может быть отрицательным.')
                    continue

                products.append({'Название':name,
                                 'Цена':price,
                                 'Количество':qty})
                
                print(f'Товар "{name}" добавлен.')
            except ValueError:
                print('Ошибка: цена и количество должны содержать только числа.')
        case '3':
            print('\nПОИСК ТОВАРА')
            name = input('Введите полное или часть названия товара для поиска: ').strip()
            if not name:
                print('Введите название для поиска.')
                continue

            found = []
            for p in products:
                if name.lower() in p['Название'].lower():
                    found.append(p)

            if found:
                print(f'Найдено товаров: {len(found)}')
                for p in found:
                    print(f'\nНазвание: {p['Название']}')
                    print(f'Цена: {p['Цена']} руб.')
                    print(f'Количество: {p['Количество']} шт.')
                    print(f'Общая стоимость: {p['Цена'] * p['Количество']} руб.')
            else:
                print(f'\nТовар по запросу "{name}" не найден.')
        case '4':
            print('\nОБЩАЯ СТОИМОСТЬ ТОВАРОВ НА СКЛАДЕ:')
            total = 0
            for p in products:
                cost = p['Цена'] * p['Количество']
                total += cost
                print(f'{p['Название']}: {p['Цена']} руб. × {p['Количество']} шт. = {cost} руб.')
            print(f'ИТОГО: {total} руб.')
        case '5':
            try:
                sorted_products = sorted(products, key=lambda x: x['Цена'])

                with open('resource/sorted_products.csv', 'w', encoding='utf-8', newline='') as f:
                    titles = ['Название', 'Цена', 'Количество']
                    writer = csv.DictWriter(f, fieldnames=titles)
                    writer.writeheader()
                    for p in sorted_products:
                        writer.writerow({'Название':p['Название'],
                                         'Цена':p['Цена'],
                                         'Количество':p['Количество']})
                        
                print('\nОтсортированные продукты сохранены в "sorted_products.csv"')
            except Exception as e:
                print(f'\nОшибка при сохранении: {e}')
        case '6':
            try:
                with open('resource/products.csv', 'w', encoding='utf-8', newline='') as f:
                    titles = ['Название', 'Цена', 'Количество']
                    writer = csv.DictWriter(f, fieldnames=titles)
                    writer.writeheader()
                    for p in products:
                        writer.writerow({'Название':p['Название'],
                                         'Цена':p['Цена'],
                                         'Количество':p['Количество']})
                print('\nДанные сохранены.')
            except Exception as e:
                print(f'\nОшибка при сохранении: {e}')
        case '0':
            print('\nРабота с файлом завершена.')
            break
        case _:
            print('\nНекорректный выбор. Попробуйте снова.')
