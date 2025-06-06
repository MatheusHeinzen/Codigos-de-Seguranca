## Adrian Antônio de Souza Gomes
## Matheus Henrique Heinzen

import hashlib
import os

ARQUIVO_USUARIOS = "usuarios.txt"

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def carregar_usuarios():
    usuarios = {}
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, "r") as f:
            for linha in f:
                nome, senha_hash = linha.strip().split(",")
                usuarios[nome] = senha_hash
    return usuarios

def salvar_usuarios(usuarios):
    with open(ARQUIVO_USUARIOS, "w") as f:
        for nome, senha_hash in usuarios.items():
            f.write(f"{nome},{senha_hash}\n")

def obter_entrada_usuario():
    nome = input("Nome: ").strip()
    senha = input("Senha: ").strip()
    if len(nome) != 4 or len(senha) != 4:
        print("Nome e senha devem ter exatamente 4 caracteres.")
        return None, None
    return nome, senha

def processar_usuario():
    usuarios = carregar_usuarios()
    print("1 - Cadastrar\n2 - Autenticar")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        nome, senha = obter_entrada_usuario()
        if not nome or nome in usuarios:
            print("Usuário inválido ou já existe.")
            return
        usuarios[nome] = hash_senha(senha)
        salvar_usuarios(usuarios)
        print("Usuário cadastrado com sucesso.")

    elif opcao == "2":
        nome, senha = obter_entrada_usuario()
        if nome in usuarios and usuarios[nome] == hash_senha(senha):
            print("Autenticação bem-sucedida.")
        else:
            print("Falha na autenticação.")
    else:
        print("Opção inválida.")


processar_usuario()
