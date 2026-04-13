import json

try:
    with open('resource/library.json', 'r', encoding='utf-8') as f:
        books = json.load(f)
    print(f'Загружено {len(books)} книг из файла.')
except FileNotFoundError:
    print('Ошибка: Файл "library.json" не найден.')
    exit()
except Exception as e:
    print(f'Ошибка при загрузке: {e}')
    exit()

print('\nСИСТЕМА УЧЁТА КНИГ В БИБЛИОТЕКЕ')

while True:
    print('\nМЕНЮ:')
    print('1 - Просмотр всех книг')
    print('2 - Поиск по автору/названию')
    print('3 - Добавление новой книги')
    print('4 - Изменение статуса доступности')
    print('5 - Удаление книги по ID')
    print('6 - Экспорт доступных книг в текстовый файл')
    print('0 - Выход')
    
    choice = input('Выберите действие: ').strip()
    
    match choice:
        case '1':
            if not books:
                print('\nБиблиотека пуста.')
            else:
                print('\nСПИСОК ВСЕХ КНИГ:')
                print(f'{'ID':<5} {'Название':<30} {'Автор':<20} {'Год':<10} {'Доступна':<5}')
                for book in books:
                    status = 'Да' if book['available'] else 'Нет'
                    title = book['title'][:30] + '...' if len(book['title']) > 30 else book['title']
                    print(f'{book['id']:<5} {title:<30} {book['author']:<20} {book['year']:<10} {status:<5}')
        case '2':
            if not books:
                print('\nБиблиотека пуста.')
                continue
            
            search = input('\nВведите автора или название для поиска: ').strip().lower()
            if not search:
                print('Ошибка: Введите текст для поиска.')
                continue
            
            found = []
            for book in books:
                if search in book['title'].lower() or search in book['author'].lower():
                    found.append(book)
            
            if found:
                print(f'\nНАЙДЕНО КНИГ: {len(found)}')
                print(f'{'ID':<5} {'Название':<30} {'Автор':<20} {'Год':<10} {'Доступна':<5}')
                for book in found:
                    status = 'Да' if book['available'] else 'Нет'
                    title = book['title'][:30] + '...' if len(book['title']) > 30 else book['title']
                    print(f'{book['id']:<5} {title:<30} {book['author']:<20} {book['year']:<10} {status:<5}')
            else:
                print(f'\nКниги по запросу "{search}" не найдены.')
        case '3':
            print('\nДОБАВЛЕНИЕ НОВОЙ КНИГИ')
            
            title = input('Введите название книги: ').strip()
            if not title:
                print('Ошибка: Название не может быть пустым.')
                continue
            
            author = input('Введите автора: ').strip()
            if not author:
                print('Ошибка: Автор не может быть пустым.')
                continue
            
            try:
                year = int(input('Введите год издания: '))
                if year <= 0 or year > 2025:
                    print('Ошибка: Некорректный год.')
                    continue
            except ValueError:
                print('Ошибка: Введите корректный год.')
                continue
            
            new_id = 1
            if books:
                new_id = max(book['id'] for book in books) + 1
            
            available = input('Книга доступна? (да/нет): ').strip().lower()
            available_status = available == 'да'
            
            new_book = {'id':new_id,
                        'title':title,
                        'author':author,
                        'year':year,
                        'available':available_status}
            
            books.append(new_book)
            
            try:
                with open('resource/library.json', 'w', encoding='utf-8') as f:
                    json.dump(books, f, ensure_ascii=False, indent=2)
                print(f'Книга "{title}" добавлена. ID: {new_id}')
            except Exception as e:
                print(f'Ошибка при сохранении: {e}')
        case '4':
            if not books:
                print('\nБиблиотека пуста.')
                continue
            
            try:
                book_id = int(input('\nВведите ID книги: '))
            except ValueError:
                print('Ошибка: Введите корректный ID.')
                continue
            
            found_book = None
            for book in books:
                if book['id'] == book_id:
                    found_book = book
                    break
            
            if found_book:
                current_status = 'доступна' if found_book['available'] else 'недоступна'
                print(f'\nТекущий статус: {current_status}')
                
                new_status = input('Изменить статус на "доступна"? (да/нет): ').strip().lower()
                new_available = new_status == 'да'
                
                found_book['available'] = new_available
                
                try:
                    with open('resource/library.json', 'w', encoding='utf-8') as f:
                        json.dump(books, f, ensure_ascii=False, indent=2)
                    
                    new_status_text = 'доступна' if new_available else 'недоступна'
                    print(f'Статус книги "{found_book['title']}" изменён на "{new_status_text}".')
                except Exception as e:
                    print(f'\nОшибка при сохранении: {e}')
            else:
                print(f'\nКнига с ID {book_id} не найдена.')
        case '5':
            if not books:
                print('\nБиблиотека пуста.')
                continue
            
            try:
                book_id = int(input('\nВведите ID книги для удаления: '))
            except ValueError:
                print('Ошибка: Введите корректный ID.')
                continue
            
            found_book = None
            for book in books:
                if book['id'] == book_id:
                    found_book = book
                    break
            
            if found_book:
                confirm = input(f'Удалить книгу "{found_book['title']}"? (да/нет): ').strip().lower()
                if confirm == 'да':
                    books.remove(found_book)
                    
                    try:
                        with open('resource/library.json', 'w', encoding='utf-8') as f:
                            json.dump(books, f, ensure_ascii=False, indent=2)
                        print(f'Книга "{found_book['title']}" удалена.')
                    except Exception as e:
                        print(f'Ошибка при сохранении: {e}')
                else:
                    print('Удаление отменено.')
            else:
                print(f'\nКнига с ID {book_id} не найдена.')
        case '6':
            available_books = [book for book in books if book['available']]
            
            if not available_books:
                print('\nНет доступных книг для экспорта.')
            else:
                try:
                    with open('resource/available_books.txt', 'w', encoding='utf-8') as f:
                        f.write('СПИСОК ДОСТУПНЫХ КНИГ\n')
                        for book in available_books:
                            f.write(f'ID: {book['id']}\n')
                            f.write(f'Название: {book['title']}\n')
                            f.write(f'Автор: {book['author']}\n')
                            f.write(f'Год: {book['year']}\n\n')
                    
                    print(f'\nЭкспортировано {len(available_books)} книг в файл "available_books.txt".')
                except Exception as e:
                    print(f'Ошибка при экспорте: {e}')
        case '0':
            print('\nРабота программы завершена.')
            break
        case _:
            print('\nОшибка: Неверный выбор. Попробуйте снова.')