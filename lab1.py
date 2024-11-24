import random
from cryptolib_lab1.crypto_utils import *

def main():
    # 1)
    num, deg = map(int, input("Введите num, deg: ").split())
    mod = generate_prime()    

    result = exponentiation_fast(num, deg, mod)
    print(f"{num}^{deg} mod {mod} = {result}\n\n")


    # 2)
    a, b = map(int, input("Введите два целых числа a, b: ").split())

    gcd, x, y = extended_gcd(a, b)

    print(f"НОД({a}, {b}) = {gcd}")
    print(f"x = {x}, y = {y}\n")

    if (a * x + b * y != gcd):
        print("Неккоректное решение уравнения.\n")


    # 3)
    mod = generate_prime()    

    base = random.randint(2, mod - 2)
    private_key_a = random.randint(1, mod - 1)
    private_key_b = random.randint(1, mod - 1)

    print(f"Основание base: {base}")
    print(f"Закрытый ключ A: {private_key_a}")
    print(f"Закрытый ключ B: {private_key_b}")
    print(f"Модуль: {mod}\n")

    shared_key_a = compute_shared_key(base, private_key_a, mod)
    shared_key_b = compute_shared_key(base, private_key_b, mod)

    print(f"Общий ключ для абонента A: {shared_key_a}")
    print(f"Общий ключ для абонента B: {shared_key_b}\n")

    final_key_a = compute_shared_key(shared_key_b, private_key_a, mod)
    final_key_b = compute_shared_key(shared_key_a, private_key_b, mod)

    print(f"Итоговый общий ключ для A: {final_key_a}")
    print(f"Итоговый общий ключ для B: {final_key_b}\n")

    if final_key_a != final_key_b:
        print("Ошибка: ключи не совпадают :с")


    # 4)
    base, result, mod = map(int, input("Введите base, result, mod: ").split())

    log_result = baby_step_giant_step(base, result, mod)
    if log_result != -1:
        print(f"{base}^x = {result} mod {mod}, x = {log_result}")
    else:
        print("Решение не найдено.")


if __name__=="__main__":
    main()