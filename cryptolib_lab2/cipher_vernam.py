import os

# Генерация ключа
def generate_vernam_key(key_size, key_path='keys/vernam_key.bin'):
    with open(key_path, 'wb') as key_out:
        key_out.write(os.urandom(key_size))

# Загрузка ключа
def load_vernam_key(key_path):
    try:
        with open(key_path, 'rb') as key_in:
            return key_in.read()
    except IOError as e:
        print(f"Ошибка загрузки ключа: {e}")
        return None

# Шифр Вернама
def cipher_vernam(input_file_name, output_file_name, key, mode):
    try:
        with open(input_file_name, 'rb') as input_file, open(output_file_name, 'wb') as output_file:
            input_size = os.path.getsize(input_file_name)
            key_size = len(key)

            if key_size < input_size:
                print("Ошибка: размер ключа меньше размера входного файла.")
                return False

            count = 0
            while chunk := input_file.read(1024):
                key_chunk = key[count:count + len(chunk)]
                result = bytes([b ^ k for b, k in zip(chunk, key_chunk)])
                output_file.write(result)
                count += len(chunk)

            print(f"{'Зашифровано' if mode == 'encode' else 'Расшифровано'} {input_size} байтов в файл {output_file_name}.")
            return True

    except IOError as e:
        print(f"Ошибка работы с файлами: {e}")
        return False