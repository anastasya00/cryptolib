from cryptolib_lab2.cipher_shamir import *
from cryptolib_lab2.cipher_elgamal import *
from cryptolib_lab2.cipher_vernam import *
from cryptolib_lab2.cipher_RSA import *

def main():

    # 1) Шифр Шамира
    mod = 251

    generate_shamir_key(mod, 'A')
    generate_shamir_key(mod, 'B')

    private_key_a = load_private_shamir_key('A')
    private_key_b = load_private_shamir_key('B')


    cipher_shamir("files/dataA.txt", "files/shamirA_encode.bin", private_key_a, mod, 'encode')
    cipher_shamir("files/shamirA_encode.bin", "files/shamirB_encode.bin", private_key_b, mod, 'encode')

    cipher_shamir("files/shamirB_encode.bin", "files/shamirA_decode.bin", private_key_a, mod, 'decode')
    cipher_shamir("files/shamirA_decode.bin", "files/shamirB_decode.txt", private_key_b, mod, 'decode')
    

    # 2) Шифр Эль-Гамаля
    generate_elgamal_keys()
    public_key = load_public_elgamal_key("keys/elgamal_public.pub")
    private_key = load_private_elgamal_key("keys/elgamal_private.pem")

    cipher_elgamal("files/dataA.txt", "files/elgamal_encode.bin", public_key, "encode")
    cipher_elgamal("files/elgamal_encode.bin", "files/elgamal_decode.txt", private_key, "decode")

    
    # Шифр Вернама
    key_size = os.path.getsize("files/dataA.txt")

    generate_vernam_key(key_size)
    key = load_vernam_key("keys/vernam_key.bin")

    cipher_vernam("files/dataA.txt", "files/vernam_encode.bin", key, "encode")
    cipher_vernam("files/vernam_encode.bin", "files/vernam_decode.txt", key, "decode")


    # Шифр RSA
    generate_rsa_keys()
    public_key = load_public_rsa_key("keys/rsa_public.pem")
    private_key = load_private_rsa_key("keys/rsa_private.pem")

    cipher_rsa("files/dataA.txt", "files/rsa_encode.bin", public_key, "encode")
    cipher_rsa("files/rsa_encode.bin", "files/rsa_decode.txt", private_key, "decode")


if __name__=="__main__":
    main()