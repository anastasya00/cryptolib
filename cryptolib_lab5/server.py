import random
from sympy import isprime, mod_inverse

def generate_keys():
    def generate_prime(bits):
        while True:
            num = random.getrandbits(bits)
            if isprime(num):
                return num

    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    # Генерация простых чисел и вычисление ключей
    p, q = generate_prime(1024), generate_prime(1024)
    n = p * q
    phi_n = (p - 1) * (q - 1)

    d = random.randint(2, phi_n - 1)
    while gcd(d, phi_n) != 1:
        d = random.randint(2, phi_n - 1)

    c = mod_inverse(d, phi_n)
    return n, d, c

def sign_ballot(blinded_hash, n, c):
    # Подпись бюллетеня
    return pow(blinded_hash, c, n)

def verify_vote(ballot, signature, n, d):
    from hashlib import sha3_256

    # Проверка подписи
    original_hash = pow(signature, d, n)
    expected_hash = int(sha3_256(ballot.encode()).hexdigest(), 16)
    return original_hash == expected_hash
