import hashlib
import random
from sympy import mod_inverse

# Генерация параметров для ГОСТ
def generate_gost_parameters():
    q = 0x11  # Примерное значение для q (256 бит)
    p = 6 * q + 1  # p = 6q + 1
    a = 10  # Примерное значение для a
    return p, q, a

# Вычисление хеша с использованием ГОСТ
def calculate_hash(message):
    # Для примера используем SHA256 как хеш-функцию
    return int(hashlib.sha256(message.encode('utf-8')).hexdigest(), 16)

# Генерация подписи
def sign_message(message, p, q, a, x):
    h = calculate_hash(message) % q
    k = random.randint(1, q-1)
    
    while True:
        r = pow(a, k, p) % q
        if r == 0:
            k = random.randint(1, q-1)
            continue
        
        s = (mod_inverse(k, q) * (h + x * r)) % q
        if s != 0:
            return r, s
        k = random.randint(1, q-1)

# Проверка подписи
def verify_signature(message, r, s, p, q, a, y):
    h = calculate_hash(message) % q
    if not (0 < r < q and 0 < s < q):
        return False

    h_inv = mod_inverse(h, q)
    u1 = (s * h_inv) % q
    u2 = (-r * h_inv) % q

    v = (pow(a, u1, p) * pow(y, u2, p)) % p % q
    return v == r

