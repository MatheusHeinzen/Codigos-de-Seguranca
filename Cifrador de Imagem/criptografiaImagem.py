from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import hashlib
import itertools
import string
import os

# Funções de criptografia adaptadas para imagens
def encrypt_image(file_path, key):
    with open(file_path, 'rb') as f:
        plain_bytes = f.read()
    
    salt = get_random_bytes(AES.block_size)
    private_key = hashlib.scrypt(key.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)
    cipher_config = AES.new(private_key, AES.MODE_GCM)
    cipher_bytes, tag = cipher_config.encrypt_and_digest(plain_bytes)
    
    return {
        'cipher_bytes': cipher_bytes,
        'salt': salt,
        'nonce': cipher_config.nonce,
        'tag': tag
    }

def decrypt_image(enc_dict, key):
    salt = enc_dict['salt']
    cipher_bytes = enc_dict['cipher_bytes']
    nonce = enc_dict['nonce']
    tag = enc_dict['tag']
    
    private_key = hashlib.scrypt(key.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)
    cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)
    decrypted_bytes = cipher.decrypt_and_verify(cipher_bytes, tag)
    
    return decrypted_bytes

# Funções para salvar/carregar do disco
def save_encrypted_image(enc_dict, output_path):
    with open(output_path, 'wb') as f:
        f.write(enc_dict['salt'] + b'::SALT::')
        f.write(enc_dict['nonce'] + b'::NONCE::')
        f.write(enc_dict['tag'] + b'::TAG::')
        f.write(enc_dict['cipher_bytes'])

def load_encrypted_image(input_path):
    with open(input_path, 'rb') as f:
        data = f.read()
    
    parts = data.split(b'::SALT::')
    salt = parts[0]
    remaining = parts[1].split(b'::NONCE::')
    nonce = remaining[0]
    remaining = remaining[1].split(b'::TAG::')
    tag = remaining[0]
    cipher_bytes = remaining[1]
    
    return {
        'salt': salt,
        'nonce': nonce,
        'tag': tag,
        'cipher_bytes': cipher_bytes
    }

# Função para detectar tipo de imagem pelos primeiros bytes
def detect_image_type(decrypted_bytes):
    if decrypted_bytes.startswith(b'\x89PNG'):
        return 'PNG'
    elif decrypted_bytes.startswith(b'\xFF\xD8'):
        return 'JPEG'
    return 'UNKNOWN'

# Ataque de força bruta
def brute_force_attack(encrypted_file_path, max_length=4):
    enc_dict = load_encrypted_image(encrypted_file_path)
    chars = string.ascii_letters + string.digits
    
    for key_length in range(1, max_length + 1):
        for candidate in itertools.product(chars, repeat=key_length):
            key = ''.join(candidate)
            try:
                decrypted = decrypt_image(enc_dict, key)
                img_type = detect_image_type(decrypted)
                if img_type in ['PNG', 'JPEG']:
                    print(f"\nChave encontrada: '{key}'")
                    print(f"Tipo de imagem detectado: {img_type}")
                    
                    # Salvar imagem descriptografada
                    output_path = f"decrypted_with_{key}.{img_type.lower()}"
                    with open(output_path, 'wb') as f:
                        f.write(decrypted)
                    print(f"Imagem salva como: {output_path}")
                    return key
            except:
                continue
    
    print("Nenhuma chave válida encontrada.")
    return None

# Menu principal
def main():
    print("=== Sistema de Criptografia de Imagens ===")
    print("1. Criptografar imagem")
    print("2. Descriptografar imagem")
    print("3. Tentar quebrar criptografia (força bruta)")
    print("4. Sair")
    
    while True:
        choice = input("\nEscolha uma opção (1-4): ")
        
        if choice == '1':
            # Criptografar
            image_path = input("Nome da imagem para criptografar (ex: castor.png): ")
            if not os.path.exists(image_path):
                print("Arquivo não encontrado!")
                continue
                
            key = input("Digite a chave (até 4 caracteres alfanuméricos): ")
            if len(key) > 4 or not key.isalnum():
                print("Chave inválida! Deve ter até 4 caracteres alfanuméricos.")
                continue
                
            encrypted = encrypt_image(image_path, key)
            save_encrypted_image(encrypted, "imagem_criptografada.castor")
            print("Imagem criptografada salva como 'imagem_criptografada.castor'")
            
        elif choice == '2':
            # Descriptografar
            encrypted_path = input("Nome do arquivo criptografado: ")
            if not os.path.exists(encrypted_path):
                print("Arquivo não encontrado!")
                continue
                
            key = input("Digite a chave: ")
            try:
                loaded = load_encrypted_image(encrypted_path)
                decrypted = decrypt_image(loaded, key)
                
                # Detectar tipo de imagem
                img_type = detect_image_type(decrypted)
                if img_type == 'UNKNOWN':
                    print("Aviso: Tipo de imagem não reconhecido. Pode ser chave incorreta.")
                    img_type = 'bin'
                
                output_path = f"imagem_descriptografada.{img_type.lower()}"
                with open(output_path, 'wb') as f:
                    f.write(decrypted)
                print(f"Imagem descriptografada salva como '{output_path}'")
            except Exception as e:
                print(f"Erro: {e}. Chave incorreta ou arquivo corrompido.")
                
        elif choice == '3':
            # Força bruta
            encrypted_path = input("Nome do arquivo criptografado: ")
            if not os.path.exists(encrypted_path):
                print("Arquivo não encontrado!")
                continue
                
            print("\nIniciando ataque de força bruta... (isso pode demorar)")
            found_key = brute_force_attack(encrypted_path)
            if not found_key:
                print("Não foi possível encontrar a chave.")
                
        elif choice == '4':
            break
            
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()