import os
import random
import secrets
from sympy import isprime

# Функция для генерации больших простых чисел
def generate_large_prime(bits=32):
    while True:
        p = random.getrandbits(bits)
        if isprime(p):
            return p

# Генерация ключей для шифра Эль-Гамаля
def generate_elgamal_keys(key_size=8192, key_path='keys'):
    p = generate_large_prime()
    g = random.randint(2, p - 1)  # Генератор g
    x = random.randint(1, p - 2)  # Приватный ключ
    y = pow(g, x, p)  # Публичный ключ y = g^x mod p

    os.makedirs(key_path, exist_ok=True)
    with open(f"{key_path}/elgamal_private.pem", "w") as private_key_file:
        private_key_file.write(f"{p}\n{g}\n{x}")
    with open(f"{key_path}/elgamal_public.pub", "w") as public_key_file:
        public_key_file.write(f"{p}\n{g}\n{y}")

# Загрузка публичного ключа
def load_public_elgamal_key(public_key_path):
    with open(public_key_path, "r") as f:
        lines = f.read().splitlines()
        p = int(lines[0])
        g = int(lines[1])
        y = int(lines[2])
        return {"p": p, "g": g, "y": y}

# Загрузка приватного ключа
def load_private_elgamal_key(private_key_path):
    with open(private_key_path, "r") as f:
        lines = f.read().splitlines()
        p = int(lines[0])
        g = int(lines[1])
        x = int(lines[2])
        return {"p": p, "g": g, "x": x}

# Шифр Эль-Гамаля
def cipher_elgamal(input_file_name, output_file_name, key, mode):
    try:
        if mode == "encode":
            with open(input_file_name, "rb") as input_file:
                data = input_file.read()

            encrypted_blocks = []
            for byte in data:
                m = byte
                k = secrets.randbelow(key["p"] - 2) + 1
                c1 = pow(key["g"], k, key["p"])
                s = pow(key["y"], k, key["p"])
                c2 = (s * m) % key["p"]
                encrypted_blocks.append((c1, c2))

            with open(output_file_name, "wb") as output_file:
                for c1, c2 in encrypted_blocks:
                    output_file.write(c1.to_bytes(4, 'big'))
                    output_file.write(c2.to_bytes(4, 'big'))

            print(f"Данные зашифрованы и записаны в {output_file_name}")

        elif mode == "decode":
            decrypted_data = bytearray()
            with open(input_file_name, "rb") as input_file:
                while True:
                    c1_bytes = input_file.read(4)
                    if not c1_bytes:
                        break
                    c1 = int.from_bytes(c1_bytes, 'big')
                    c2_bytes = input_file.read(4)
                    c2 = int.from_bytes(c2_bytes, 'big')

                    s = pow(c1, key["x"], key["p"])
                    s_inv = pow(s, -1, key["p"])
                    m = (c2 * s_inv) % key["p"]
                    decrypted_data.append(m)

            with open(output_file_name, "wb") as output_file:
                output_file.write(decrypted_data)

            print(f"Данные расшифрованы и записаны в {output_file_name}")

        else:
            print("Неизвестный режим шифрования.")
            return False

    except IOError as e:
        print(f"Ошибка при работе с файлом: {e}")
        return False
    except ValueError as e:
        print(f"Ошибка при вычислении: {e}")
        return False
    
    return True