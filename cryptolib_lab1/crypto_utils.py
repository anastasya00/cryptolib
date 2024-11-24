import math
import random

# 1) Функция быстрого возведения числа в степень по модулю
def exponentiation_fast(num, deg, mod):
    if mod <= 1:
        raise ValueError("Модуль должен быть больше 1.")
    result = 1
    num %= mod
    if deg < 0:
        num = mod_inverse(num, mod)
        deg = -deg
    while deg > 0:
        if deg % 2 == 1:
            result = (result * num) % mod
        num = (num * num) % mod
        deg //= 2
    return result

# 2) Функция, реализующая обобщённый алгоритм Евклида
def extended_gcd(a, b):
    if b == 0:
        return abs(a), 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y

# 3) Функция построения общего ключа для двух абонентов по схеме Диффи-Хеллмана
def compute_shared_key(base, private_key, mod):
    return exponentiation_fast(base, private_key, mod)

# Вспомогательная функция для нахождения обратного по модулю
def mod_inverse(num, mod):
    gcd, x, _ = extended_gcd(num, mod)
    if gcd != 1:
        raise ValueError(f"Обратный элемент не существует, так как НОД({num}, {mod}) != 1.")
    return (x % mod + mod) % mod

# 4) Функция для решения задачи нахождения дискретного логарифма с использованием алгоритма «Шаг младенца, шаг великана» O(√P*log_2(P)).
def baby_step_giant_step(base, result, mod):
    if mod <= 1:
        raise ValueError("Модуль должен быть больше 1.")

    m = math.isqrt(mod) + 1
    baby_step = {exponentiation_fast(base, j, mod): j for j in range(m)}

    base_inv_m = exponentiation_fast(base, m, mod)
    base_inv_m = mod_inverse(base_inv_m, mod)

    giant_step = result
    for i in range(m):
        if giant_step in baby_step:
            return i * m + baby_step[giant_step]
        giant_step = (giant_step * base_inv_m) % mod

    return -1

# Функция проверки числа на простоту
def is_prime(p):
    if p <= 1:
        return False
    b = int(math.sqrt(p))
    for i in range(2, b + 1):
        if p % i == 0:
            return False
    return True

# Функция генерации случайного простого числа
def generate_prime(range_limit=100):
    while True:
        x = random.randint(2, range_limit)
        if is_prime(x):
            return x