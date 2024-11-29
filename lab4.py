from cryptolib_lab4.mental_poker_vernam import *
from cryptolib_lab4.mental_poker_rsa import *

def main():
    # num_players = int(input("Введите количество игроков (2-10): ")) # для справедливого распределения карт из стандартной колоды
    # if num_players < 2 or num_players > 10:
    #     print("Количество игроков должно быть от 2 до 10!")
    #     return

    # generate_keys(num_players)
    # encrypted_deck = shuffle_and_encrypt(DECK, num_players)
    # players, table = distribute_cards(encrypted_deck, num_players)

    # for player, cards in players.items():
    #     print(f"{player}:")
    #     for card in cards:
    #         decrypted_card = decrypt_card(card, f"keys/{player.split()[1]}_privatekey.pem")
    #         print(f"  {decrypted_card}")

    # print("\nКарты на столе:")
    # for i, card in enumerate(table):
    #     player_index = i % num_players
    #     player_key = f"keys/{player_index + 1}_privatekey.pem"
    #     decrypted_card = decrypt_card(card, player_key)
    #     print(f"  {decrypted_card}")

    play_game(num_players=3)

if __name__ == "__main__":
    main()