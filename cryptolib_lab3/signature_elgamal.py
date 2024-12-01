import hashlib
import secrets
import math
from cryptolib_lab2.cipher_elgamal import *

# Вычисление хэша файла
def compute_hash(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return int(sha256.hexdigest(), 16)

# Генерация подписи
def generate_signature(file_path, private_key_path):
    private_key = load_private_elgamal_key(private_key_path)
    p, g, x = private_key["p"], private_key["g"], private_key["x"]

    h = compute_hash(file_path) % p
    if h <= 1:
        raise ValueError("Значение хэша слишком мало. Выберите другой файл.")

    while True:
        k = secrets.randbelow(p - 1) + 1
        if math.gcd(k, p - 1) == 1:
            break

    r = pow(g, k, p)
    u = (h - x * r) % (p - 1)
    k_inv = pow(k, -1, p - 1)
    s = (k_inv * u) % (p - 1)

    return r, s

# Проверка подписи
def verify_signature(file_path, signature, public_key_path):
    public_key = load_public_elgamal_key(public_key_path)
    p, g, y = public_key["p"], public_key["g"], public_key["y"]

    r, s = signature
    if not (1 < r < p):
        return False

    h = compute_hash(file_path) % p
    if h <= 1:
        raise ValueError("Значение хэша слишком мало. Выберите другой файл.")

    lhs = (pow(y, r, p) * pow(r, s, p)) % p
    rhs = pow(g, h, p)
    return lhs == rhs

# Подписание файла
def sign_file(file_path, private_key_path, signature_path):
    r, s = generate_signature(file_path, private_key_path)
    with open(signature_path, "w") as sig_file:
        sig_file.write(f"{r}\n{s}")
    print(f"Подпись, сохраненная в {signature_path}")

# Проверка подписи файла
def check_file_signature(file_path, signature_path, public_key_path):
    with open(signature_path, "r") as sig_file:
        lines = sig_file.read().splitlines()
        r, s = int(lines[0]), int(lines[1])

    if verify_signature(file_path, (r, s), public_key_path):
        print("Подпись действительна.")
    else:
        print("Подпись недействительна.")

