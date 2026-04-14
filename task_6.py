import struct
from datetime import datetime

with open('resource/data.bin', 'rb') as f:
    signature = f.read(4)
    version = struct.unpack('<H', f.read(2))[0]
    num_records = struct.unpack('<I', f.read(4))[0]
    
    print('РАЗБОР БИНАРНОГО ФАЙЛА "data.bin"')
    print(f'Сигнатура: {signature.decode('ascii')}')
    print(f'Версия: {version}\n')
    print(f'Количество записей: {num_records}')
    
    temperatures = []
    active_flags_count = 0
    
    for i in range(num_records):
        timestamp_raw = struct.unpack('<Q', f.read(8))[0]
        record_id = struct.unpack('<I', f.read(4))[0]
        temp_raw = struct.unpack('<h', f.read(2))[0]
        flags = struct.unpack('<B', f.read(1))[0]
        
        timestamp = datetime.fromtimestamp(timestamp_raw / 1000)
        temperature = temp_raw / 100.0
        temperatures.append(temperature)
        
        if flags != 0:
            active_flags_count += 1
        
        print(f'Запись {i+1}: {timestamp.strftime('%Y-%m-%d %H:%M:%S')} '
              f'ID={record_id} Температура={temperature:+.2f}°C '
              f'Флаги=0x{flags:02X} ({flags})')
    
    avg_temperature = sum(temperatures) / len(temperatures)
    
    print('\nСТАТИСТИКА:')
    print(f'Средняя температура: {avg_temperature:.2f}°C')
    print(f'Количество записей с активными флагами: {active_flags_count} из {num_records}')