import hashlib
import os
from cryptolib_lab2.cipher_RSA import *

def compute_hash(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as file:
        while chunk := file.read(4096):
            sha256.update(chunk)
    return int.from_bytes(sha256.digest(), byteorder="big")

def sign_file(file_path, private_key_path, signature_output_path):
    # Вычисляем хэш
    hash_value = compute_hash(file_path)
    
    # Загружаем приватный ключ
    private_key = load_private_rsa_key(private_key_path)
    
    # Подписываем хэш
    signature = pow(hash_value, private_key[0], private_key[1])
    
    # Сохраняем подпись
    with open(signature_output_path, "w") as signature_file:
        signature_file.write(str(signature))  # Сохраняем подпись как строку числа

def verify_signature(file_path, public_key_path, signature_path):
    # Вычисляем хэш файла
    hash_value = compute_hash(file_path)
    
    # Загружаем публичный ключ
    public_key = load_public_rsa_key(public_key_path)
    
    # Загружаем подпись
    with open(signature_path, "r") as signature_file:
        signature = int(signature_file.read())
    
    # Проверяем подпись
    verified_hash = pow(signature, public_key[0], public_key[1])
    return verified_hash == hash_value

def check_file_signature(file_path, signature_path, public_key_path):
    # Проверяем подпись
    if verify_signature(file_path, public_key_path, signature_path):
        print("Подпись действительна.")
    else:
        print("Подпись действительна.")
