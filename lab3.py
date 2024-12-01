from cryptolib_lab3.signature_elgamal import *
from cryptolib_lab3.signature_RSA import *
from cryptolib_lab3.signature_GOST import *

def main():
    # Подпись на базе шифра Эль-Гамаль
    generate_elgamal_keys(key_size=512)

    sign_file("files/dataA.txt", "keys/elgamal_private.pem", "files/dataA_elgamal.sig")
    check_file_signature("files/dataA.txt", "files/dataA_elgamal.sig", "keys/elgamal_public.pub")


    # Подпись на базе шифра RSA
    generate_rsa_keys(key_size=2048, key_path="keys")
    sign_file("files/dataA.txt", "keys/rsa_private.pem", "files/dataA_rsa.sig")
    check_file_signature("files/dataA.txt", "files/dataA_rsa.sig", "keys/rsa_public.pem")
    

    # Подпись по ГОСТУ
    p, q, a = generate_gost_parameters()

    x = 6  # Закрытый ключа
    y = pow(a, x, p)  # Открытый ключ

    # Сообщение для подписи
    message = "Hello, this is a test message."

    # Подпись
    r, s = sign_message(message, p, q, a, x)
    print(f"Подпись: r = {r}, s = {s}")

    # Проверка подписи
    is_valid = verify_signature(message, r, s, p, q, a, y)
    print(f"Подпись действительна: {is_valid}")
    

if __name__ == "__main__":
    main()