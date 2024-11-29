import os
import random
from cryptolib_lab2.cipher_vernam import *

# Карты стандартной колоды
DECK = [f"{rank}{suit}" for rank in '23456789TJQKA' for suit in '♠♥♦♣']

def generate_keys(player_count, key_folder="keys"):
    os.makedirs(key_folder, exist_ok=True)
    for i in range(player_count):
        key_path = os.path.join(key_folder, f"{i + 1}_privatekey.pem")
        generate_vernam_key(512, key_path)

def shuffle_and_encrypt(deck, player_count, key_folder="keys"):
    cards_folder = "cards"
    os.makedirs(cards_folder, exist_ok=True)
    encrypted_deck = []

    random.shuffle(deck)
    for i, card in enumerate(deck):
        card_file = os.path.join(cards_folder, f"card_{i}.bin")
        encrypted_file = os.path.join(cards_folder, f"encrypted_card_{i}.bin")
        key = load_vernam_key(os.path.join(key_folder, f"{(i % player_count) + 1}_privatekey.pem"))

        with open(card_file, "w") as f:
            f.write(card)

        cipher_vernam(card_file, encrypted_file, key, mode="encode")
        encrypted_deck.append(encrypted_file)

    return encrypted_deck

def distribute_cards(encrypted_deck, player_count):
    if len(encrypted_deck) < player_count * 2 + 5:
        raise ValueError("Недостаточно карт в колоде для раздачи игрокам и на стол.")

    players = {f"Player {i + 1}": [] for i in range(player_count)}
    table = []

    for i in range(player_count * 2):
        players[f"Player {(i % player_count) + 1}"].append(encrypted_deck[i])

    table = encrypted_deck[player_count * 2:player_count * 2 + 5]

    return players, table

def decrypt_card(card_file, player_key):
    cards_folder = "cards"
    os.makedirs(cards_folder, exist_ok=True)

    output_file = card_file.replace("encrypted_", "decrypted_")
    key = load_vernam_key(player_key)

    cipher_vernam(card_file, output_file, key, mode="decode")

    with open(output_file, "rb") as f:
        decrypted_card = f.read()
        return decrypted_card.decode("utf-8", errors="ignore")

