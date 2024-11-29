import random
import os
import tempfile
from cryptolib_lab2.cipher_RSA import *

def generate_cards(num_players):
    cards = ['3', '7', 'A', 'K', 'Q', 'J', '10', '9', '8', '7']
    deck = random.sample(cards, len(cards))
    hands = {f"Player {i+1}": deck[i*2:(i+1)*2] for i in range(num_players)}
    table_cards = deck[num_players*2:]
    return hands, table_cards

def play_game(num_players=2):
    key_path = 'keys'
    cards_path = 'cards'
    
    os.makedirs(key_path, exist_ok=True)
    os.makedirs(cards_path, exist_ok=True)
    
    generate_rsa_keys(key_size=2048, key_path=key_path)
    
    e, n = load_public_rsa_key(f"{key_path}/rsa_public.pem")
    d, _ = load_private_rsa_key(f"{key_path}/rsa_private.pem")
    public_key = (e, n)
    private_key = (d, n)
    
    hands, table_cards = generate_cards(num_players)
    
    with open(os.path.join(cards_path, 'encrypted_cards.txt'), 'wb') as f:
        # Шифруем карты игроков
        encrypted_hands = {}
        for player, hand in hands.items():
            encrypted_hands[player] = []
            for card in hand:
                card_bytes = card.encode()  # Кодируем карту в байты
                with tempfile.NamedTemporaryFile(delete=False) as input_file:
                    input_file.write(card_bytes)  # Записываем карту в файл
                    input_file_name = input_file.name
                
                # Шифруем карту
                with tempfile.NamedTemporaryFile(delete=False) as output_file:
                    output_file_name = output_file.name
                    cipher_rsa(input_file_name, output_file_name, public_key, "encode")
                    
                    # Читаем зашифрованные данные
                    with open(output_file_name, "rb") as enc_file:
                        encrypted_data = enc_file.read()
                    
                    encrypted_hands[player].append(encrypted_data)
        
        # Записываем зашифрованные карты игроков в файл
        f.write(b'Encrypted Hands:\n')
        for player, hand in encrypted_hands.items():
            f.write(f"{player}: {hand}\n".encode())
        
        # Шифруем карты на столе
        f.write(b'\nEncrypted Table Cards:\n')
        encrypted_table_cards = []
        for card in table_cards:
            card_bytes = card.encode()
            with tempfile.NamedTemporaryFile(delete=False) as input_file:
                input_file.write(card_bytes)  # Записываем карту в файл
                input_file_name = input_file.name
            
            with tempfile.NamedTemporaryFile(delete=False) as output_file:
                output_file_name = output_file.name
                cipher_rsa(input_file_name, output_file_name, public_key, "encode")
                
                with open(output_file_name, "rb") as enc_file:
                    encrypted_data = enc_file.read()
                
                encrypted_table_cards.append(encrypted_data)
        
        # Записываем зашифрованные настольные карты в файл
        f.write(b'Encrypted Table Cards:\n')
        for card in encrypted_table_cards:
            f.write(f"{card}\n".encode())
    
    # Чтение зашифрованных карт из файла и расшифровка
    with open(os.path.join(cards_path, 'encrypted_cards.txt'), 'rb') as f:
        content = f.read().decode().split('\n')
        
        # Расшифровка карт игроков
        decrypted_hands = {}
        for player in encrypted_hands:
            decrypted_hands[player] = []
            for encrypted_card in encrypted_hands[player]:
                with tempfile.NamedTemporaryFile(delete=False) as input_file:
                    input_file.write(encrypted_card)  # Записываем зашифрованные данные в файл
                    input_file_name = input_file.name
                
                with tempfile.NamedTemporaryFile(delete=False) as output_file:
                    output_file_name = output_file.name
                    cipher_rsa(input_file_name, output_file_name, private_key, "decode")
                    
                    with open(output_file_name, "rb") as f:
                        decrypted_data = f.read()
                    
                    decrypted_hands[player].append(decrypted_data.decode())
        
        # Расшифровка настольных карт
        decrypted_table_cards = []
        for encrypted_card in encrypted_table_cards:
            with tempfile.NamedTemporaryFile(delete=False) as input_file:
                input_file.write(encrypted_card)
                input_file_name = input_file.name
            
            with tempfile.NamedTemporaryFile(delete=False) as output_file:
                output_file_name = output_file.name
                cipher_rsa(input_file_name, output_file_name, private_key, "decode")
                
                with open(output_file_name, "rb") as f:
                    decrypted_data = f.read()
                
                decrypted_table_cards.append(decrypted_data.decode())
    
    print(f"Расшифрованные розданные карты: {decrypted_hands}")
    print(f"Расшифрованные настольные карты: {decrypted_table_cards}")
