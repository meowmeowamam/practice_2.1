key = 0x5A

try:
    with open('resource/data.bin', 'rb') as f:
        data = f.read()
except FileNotFoundError:
    print('Ошибка: Файл "data.bin" не найден.')
    exit()
except Exception as e:
    print(f'Ошибка при чтении: {e}')
    exit()

encoded_data = bytearray()

for byte in data:
    shiftl = ((byte << 2) | (byte >> 6)) & 0xFF
    result = shiftl ^ key
    encoded_data.append(result)

try:
    with open('resource/data_encoded.bin', 'wb') as f:
        f.write(encoded_data)
except Exception as e:
    print(f'Ошибка при сохранении: {e}')
    exit()

print('Файл зашифрован: data_encoded.bin')

with open('resource/data_encoded.bin', 'rb') as f:
    encd_data = f.read()

decoded_data = bytearray()

for byte in encd_data:
    after_xor = byte ^ key
    shiftr = ((after_xor >> 2) | (after_xor << 6)) & 0xFF
    decoded_data.append(shiftr)

try:
    with open('resource/data_decoded.bin', 'wb') as f:
        f.write(decoded_data)
except Exception as e:
    print(f'Ошибка при сохранении: {e}')
    exit()

print('Файл расшифрован: data_decoded.bin')

print('\nПРОВЕРКА:')
if data == decoded_data:
    print('Исходный и расшифрованный файлы совпадают.')
else:
    print('ОШИБКА: Файлы не совпадают.')