students = []

try:
    with open('resource/students.txt', 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, 1):
            line = line.strip()
            if not line:
                continue
            if ':' not in line or line.count(':') != 1:
                print(f'Строка {line_num} пропущена (некорректный формат): {line}')
                continue

            name, grades_str = line.split(':', 1)
            name = name.strip()

            if not name:
                print(f'Строка {line_num} пропущена (пустое имя): {line}')
                continue

            valid_grades = {2, 3, 4, 5}
            grades = []
            invalid_grades = []

            for g in grades_str.split(','):
                g = g.strip()
                if g:
                    try:
                        grade = int(g)
                        if grade in valid_grades:
                            grades.append(grade)
                        else:
                            invalid_grades.append(grade)
                    except ValueError:
                        invalid_grades.append(g)

            if invalid_grades:
                print(f'У студента "{name}" пропущены некорректные оценки: {invalid_grades}')

            if grades:
                average = sum(grades) / len(grades)
                students.append({'name':name,
                                 'grades':grades,
                                 'average':average})
            else:
                print(f'Студент "{name}" пропущен (нет корректных оценок).')
except FileNotFoundError:
    print('\nОшибка: Файл "students.txt" не найден.')
    exit()
except Exception as e:
    print(f'\nОшибка при чтении файла: {e}')
    exit()

if not students:
    print('\nНет данных для анализа. Программа завершена.')
    exit()

print('\nФайл "students.txt" успешно прочитан.')

filtered_students = []
for s in students:
    if s['average'] > 4.0:
        filtered_students.append(s)

try:
    with open('resource/result.txt', 'w', encoding='utf-8') as f:
        for s in filtered_students:
            f.write(f'{s['name']}: {s['average']:.2f}\n')
    if filtered_students:
        if len(filtered_students) == 1:
            print('\nСоздан файл "result.txt" с 1 студентом, средний балл которого выше 4.0.')
        else:
            print(f'\nСоздан файл "result.txt" с {len(filtered_students)} студентами, средний балл которых выше 4.0.')
    else:
        print('\nФайл "result.txt" создан, но пустой, так как нет студентов со средним баллом выше 4.0.')
except Exception as e:
    print(f'\nОшибка при сохранении файла: {e}')

best = students[0]
worst = students[0]

for s in students:
    if s['average'] > best['average']:
        best = s
    if s['average'] < worst['average']:
        worst = s    

print(f'\nСтудент с наивысшим средним баллом: {best['name']} - {best['average']:.2f}')
print(f'Оценки: {best['grades']}')
print()
print(f'Студент с наинизшим средним баллом: {worst['name']} - {worst['average']:.2f}')
print(f'Оценки: {worst['grades']}')
