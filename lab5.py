from cryptolib_lab5.server import generate_keys, sign_ballot, verify_vote
from cryptolib_lab5.client import prepare_ballot, send_ballot_for_signature, cast_vote

def main():
    print("Добро пожаловать в систему анонимного голосования!")
    print("Вопрос: Вы поддерживаете проект X?")
    print("Варианты: 1 - Да, 2 - Нет, 3 - Воздержался")

    # Генерация ключей на сервере
    n, d, c = generate_keys()

    vote = input("Ваш выбор: ")
    while vote not in {"1", "2", "3"}:
        print("Неверный ввод. Попробуйте снова.")
        vote = input("Ваш выбор: ")

    print("\nФормируем бюллетень...")
    blinded_hash, ballot, r = prepare_ballot(vote, n, d)

    print("Передача бюллетеня серверу...")
    signed_blinded_hash = send_ballot_for_signature(blinded_hash, n, c)

    print("\nПередача подписанного бюллетеня серверу для учета...")
    cast_vote(signed_blinded_hash, ballot, r, n, d, c)


if __name__ == "__main__":
    main()