import os
from Crypto.Util import number
from cryptolib_lab1.crypto_utils import generate_prime, mod_inverse

# Генерация RSA-ключей
def generate_rsa_keys(key_size=2048, key_path='keys'):
    p = number.getPrime(key_size // 2)
    q = number.getPrime(key_size // 2)
    
    n = p * q
    phi_n = (p - 1) * (q - 1)

    e = 65537
    d = mod_inverse(e, phi_n)

    os.makedirs(key_path, exist_ok=True)
    with open(f"{key_path}/rsa_private.pem", "w") as private_file:
        private_file.write(f"{d}\n{n}")

    with open(f"{key_path}/rsa_public.pem", "w") as public_file:
        public_file.write(f"{e}\n{n}")

# Загрузка публичного ключа
def load_public_rsa_key(key_path):
    with open(key_path, "r") as public_file:
        e, n = map(int, public_file.read().splitlines())
    return e, n

# Загрузка приватного ключа
def load_private_rsa_key(key_path):
    with open(key_path, "r") as private_file:
        d, n = map(int, private_file.read().splitlines())
    return d, n

# Шифр RSA
def cipher_rsa(input_file_name, output_file_name, key, mode):
    try:
        if mode == "encode":
            e, n = key
            with open(input_file_name, "rb") as input_file:
                data = input_file.read()
                
                if len(data) > (n.bit_length() // 8) - 11:
                    raise ValueError("Данные слишком велики для шифрования.")

                data_int = int.from_bytes(data, byteorder='big')
                ciphered_int = pow(data_int, e, n)
                encrypted_data = ciphered_int.to_bytes((ciphered_int.bit_length() + 7) // 8, byteorder='big')
                
                with open(output_file_name, "wb") as output_file:
                    output_file.write(encrypted_data)

        elif mode == "decode":
            d, n = key
            with open(input_file_name, "rb") as input_file:
                ciphered_data = input_file.read()
                ciphered_int = int.from_bytes(ciphered_data, byteorder='big')
                decrypted_int = pow(ciphered_int, d, n)
                
                decrypted_data = decrypted_int.to_bytes((decrypted_int.bit_length() + 7) // 8, byteorder='big')

                with open(output_file_name, "wb") as output_file:
                    output_file.write(decrypted_data)

        else:
            print("Неизвестный режим шифрования.")
            return False
    except Exception as e:
        print(f"Ошибка при обработке файла: {e}")
        return False