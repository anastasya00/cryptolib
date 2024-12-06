import random
from hashlib import sha3_256
from sympy import mod_inverse
from cryptolib_lab5.server import *

def prepare_ballot(vote, n, d):
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    # Генерация случайного числа и бюллетеня
    r = random.randint(2, n - 1)
    while gcd(r, n) != 1:
        r = random.randint(2, n - 1)

    ballot = f"vote:{vote}"
    ballot_hash = int(sha3_256(ballot.encode()).hexdigest(), 16)

    # Ослепление
    blinded_hash = (ballot_hash * pow(r, d, n)) % n
    return blinded_hash, ballot, r

def send_ballot_for_signature(blinded_hash, n, c):
    # Симуляция отправки на сервер для подписи
    return sign_ballot(blinded_hash, n, c)

def cast_vote(signed_blinded_hash, ballot, r, n, d, c):
    # Снятие ослепления
    signature = (signed_blinded_hash * mod_inverse(r, n)) % n

    # Проверка голоса
    valid = verify_vote(ballot, signature, n, d)
    if valid:
        print("Ваш голос успешно учтен!")
    else:
        print("Ошибка проверки голоса!")
