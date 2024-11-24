import os
import random
import pickle

# Генерация ключей Шамира
def generate_shamir_key(mod, role, key_path='keys'):
    secret = random.randint(1, mod - 1)  # Секретный ключ
    coefficients = [random.randint(1, mod - 1) for _ in range(2)]  # Генерация случайных коэффициентов

    if not os.path.exists(key_path):
        os.makedirs(key_path)
    with open(os.path.join(key_path, f'shamir_key_{role}.pem'), 'wb') as f:
        pickle.dump((secret, coefficients), f)

# Загрузка приватного ключа
def load_private_shamir_key(role, key_path='keys'):
    with open(os.path.join(key_path, f'shamir_key_{role}.pem'), 'rb') as f:
        secret, coefficients = pickle.load(f)
    return secret, coefficients

# Шифр Шамира
def cipher_shamir(input_file_name, output_file_name, private_key, mod, mode):
    secret, coefficients = private_key

    with open(input_file_name, 'rb') as f:
        data = f.read()
    modified_data = bytearray()

    if mode == 'encode':
        for byte in data:
            x = byte
            encrypted_byte = (x + coefficients[0] * secret + coefficients[1] * (secret ** 2)) % 256
            modified_data.append(encrypted_byte)

    elif mode == 'decode':
        for byte in data:
            decrypted_byte = (byte - (coefficients[0] * secret + coefficients[1] * (secret ** 2))) % 256
            modified_data.append(decrypted_byte)

    with open(output_file_name, 'wb') as f:
        f.write(modified_data)