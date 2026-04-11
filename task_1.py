text = ['Сквозь тучи пробивает лучик света,',
         'Даря земле последнее тепло.',
         'За птицами на юг умчалось лето.',
         'И осень, !в платье золотого цвета,',
         'He sends me greetings, wetting the glass with rain.']

try:
    with open('text.txt', 'w', encoding='utf-8') as file:
        for line in text:
            file.write(line + '\n')
    print('Файл "text.txt" успешно создан и заполнен 5 строками.')
except Exception as e:
    print(f'Ошибка при создании файла: {e}')

with open('text.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

lines = [line.rstrip('\n') for line in lines]

lines_count = len(lines)

words_count = 0
for line in lines:
    clear_line = ''
    for i, l in enumerate(line):
        if l.isalpha() or l == ' ':
            clear_line += l
        elif l == '-':
            if i > 0 and i < len(line) - 1:
                prev_l = line[i-1]
                next_l = line[i+1]
                if prev_l.isalpha() and next_l.isalpha():
                    clear_line += l
                else:
                    clear_line += ' '
            else:
                clear_line += ' '
        else:
            clear_line += ' '

    words = clear_line.split()
    words_count += len(words)

longest_line = max(lines, key=len) if lines else ''

vowels = 'aeiouаеёиоуыэюяAEIOUАЕЁИОУЫЭЮЯ'
consonants = 'bcdfghjklmnpqrstvwxyzбвгджзйклмнпрстфхцчшщBCDFGHJKLMNPQRSTVWXYZБВГДЖЗЙКЛМНПРСТФХЦЧШЩ'

vowels_count = 0
consonants_count = 0

for line in lines:
    for l in line:
        if l in vowels:
            vowels_count += 1
        elif l in consonants:
            consonants_count += 1

print('Результаты анализа файла "text.txt":')
print(f'1) Количество строк в файле: {lines_count}')
print(f'2) Количество слов в файле: {words_count}')
print(f'3) Самая длинная строка: {longest_line}')
print(f'4) Количество гласных и согласных букв: {vowels_count} и {consonants_count}')