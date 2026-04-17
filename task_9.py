class JSONDeserialize:

    def __init__(self, json_str):
        self.json_str = json_str
        self.position = 0
        self.line = 1
        self.column = 1
        self.error_line = None

    def error(self, message):
        self.error_line = self.line
        raise ValueError(f'Ошибка на строке {self.line}, позиция {self.column}: {message}.')
    
    def peek(self):
        if self.position >= len(self.json_str):
            return None
        return self.json_str[self.position]
    
    def advance(self):
        if not self.peek():
            return
        if self.json_str[self.position] == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.position += 1

    def skip_spaces(self):
        while self.peek() and self.peek() in ' \t\n\r':
            self.advance()

    def parse(self):
        self.skip_spaces()
        result = self.parse_value()
        self.skip_spaces()
        if self.peek():
            self.error('Лишние символы после конца JSON значения')
        return result
    
    def parse_value(self):
        self.skip_spaces()
        sym = self.peek()

        if not sym:
            self.error('Неожиданный конец строки')

        match sym:
            case '"': return self.parse_str()
            case '{': return self.parse_obj()
            case '[': return self.parse_arr()
            case 't' | 'f' | 'n': return self.parse_keyword()
            case '-' | _ if sym.isdigit(): return self.parse_num()
            case _: self.error(f'Неожиданный символ: "{sym}"')

    def parse_esc(self):
        self.advance()
        sym = self.peek()
        if not sym:
            self.error('Неожиданный конец строки в экранировании')

        match sym:
            case '"': return '"'
            case '\\': return '\\'
            case '/': return '/'
            case 'n': return '\n'
            case 't': return '\t'
            case 'r': return '\r'
            case 'b': return '\b'
            case 'f': return '\f'
            case _: self.error(f'Неизвестная escape-последовательность: \\{sym}')

    def parse_str(self):
        self.advance()
        result = ''

        while True:
            sym = self.peek()
            if not sym:
                self.error('Незакрытая строка')

            match sym:
                case '"':
                    self.advance()
                    return result
                case '\\':
                    result += self.parse_esc()
                    self.advance()
                case _:
                    result += sym
                    self.advance()

    def parse_dig(self, message=None):
        sym = self.peek()
        if not sym or not sym.isdigit():
            if message:
                self.error(message)
            return False
        while sym and sym.isdigit():
            self.advance()
            sym = self.peek()
        return True
    
    def parse_num(self):
        start = self.position

        if self.peek() == '-':
            self.advance()

        self.parse_dig('Ожидалась цифра')

        if self.peek() == '.':
            self.advance()
            self.parse_dig('Ожидалась цифра после точки')

        if self.peek() in 'eE':
            self.advance()
            if self.peek() in '+-':
                self.advance()
            self.parse_dig('Ожидалась цифра в экспоненте')

        num_str = self.json_str[start:self.position]

        if '.' in num_str or 'e' in num_str or 'E' in num_str:
            return float(num_str)
        return int(num_str)
    
    def parse_keyword(self):
        sym = self.peek()

        match sym:
            case 't':
                if self.json_str[self.position:self.position+4] == 'true':
                    for _ in range(4):
                        self.advance()
                    return True
                self.error('Ожидалось "true"')
            case 'f':
                if self.json_str[self.position:self.position+5] == 'false':
                    for _ in range(5):
                        self.advance()
                    return False
                self.error('Ожидалось "false"')
            case 'n':
                if self.json_str[self.position:self.position+4] == 'null':
                    for _ in range(4):
                        self.advance()
                    return None
                self.error('Ожидалось "null"')
            case _:
                self.error(f'Неожиданный символ: "{sym}"')

    def parse_arr(self):
        self.advance()
        result = []

        self.skip_spaces()

        if self.peek() == ']':
            self.advance()
            return result
        
        while True:
            result.append(self.parse_value())
            self.skip_spaces()

            if self.peek() == ']':
                self.advance()
                break
            elif self.peek() == ',':
                self.advance()
                self.skip_spaces()
            else:
                self.error('Ожидалась "," или "]"')
        
        return result
    
    def parse_obj(self):
        self.advance()
        result = {}

        self.skip_spaces()

        if self.peek() == '}':
            self.advance()
            return result
        
        while True:
            self.skip_spaces()
            if self.peek() != '"':
                self.error('Ожидалось имя ключа (строка в кавычках)')
            key = self.parse_str()

            self.skip_spaces()
            if self.peek() != ':':
                self.error('Ожидалось ":"')
            
            self.advance()
            value = self.parse_value()
            result[key] = value

            self.skip_spaces()
            if self.peek() == '}':
                self.advance()
                break
            elif self.peek() == ',':
                self.advance()
            else:
                self.error('Ожидалась "," или "}"')

        return result

replacements = [('\\', '\\\\'), ('"', '\\"'), ('\n', '\\n'),
                ('\r', '\\r'), ('\t', '\\t'), ('\b', '\\b'), ('\f', '\\f')]

def serialization(obj, indent=0, level=0):
    space = ' ' * (indent * level) if indent else ''
    next_space = ' ' * (indent * (level + 1)) if indent else ''

    if obj is None:
        return 'null'
    
    if isinstance(obj, bool):
        return 'true' if obj else 'false'
    
    if isinstance(obj, (float, int)):
        if isinstance(obj, float) and obj.is_integer():
            return str(int(obj))
        return str(obj)
    
    if isinstance(obj, str):
        for old, new in replacements:
            obj = obj.replace(old, new)
        return f'"{obj}"'
    
    if isinstance(obj, list):
        if not obj:
            return '[]'
        items = [serialization(item, indent, level + 1) for item in obj]
        if indent:
            return '[\n' + next_space + ',\n'.join(items) + '\n' + space + ']'
        return '[' + ','.join(items) + ']'
    
    if isinstance(obj, dict):
        if not obj:
            return '{}'
        items = []
        for key, value in obj.items():
            key_str = f'"{key}"'
            value_str = serialization(value, indent, level + 1)
            items.append(f'{key_str}: {value_str}')
        if indent:
            return '{\n' + next_space + ',\n'.join(items) + '\n' + space + '}'
        return '{' + ','.join(items) + '}'
    
    raise TypeError(f'Не сериализуемый тип: {type(obj)}.')

def to_json(obj, indent=2):
    return serialization(obj, indent)

def from_json(obj):
    parser = JSONDeserialize(obj)
    return parser.parse()

def validation(obj):
    parser = JSONDeserialize(obj)
    try:
        parser.parse()
        return True, None
    except ValueError:
        return False, parser.error_line if parser.error_line is not None else 1
    
#test

files = ['test_1', 'test_2', 'test_3', 'test_4', 'test_5',
         'test_6', 'test_7', 'test_8', 'test_9', 'json_10']

for i, filename in enumerate(files, 1):
    filename += '.json'
    print(f'ФАЙЛ {i}: {filename}')

    try:
        with open(f'resource/test_objects_json/{filename}', 'r', encoding='utf-8') as f:
            content = f.read()

        valid, error = validation(content)

        if valid:
            print('JSON валидный')
            obj = from_json(content)
            print(f'Результат: {obj}')
        else:
            print('JSON невалидный')
            print(f'Ошибка на строке: {error}')
    except FileNotFoundError:
        print(f'Файл не найден: {filename}')
    except Exception as e:
        print(f'Ошибка: {e}')
    print('\n')