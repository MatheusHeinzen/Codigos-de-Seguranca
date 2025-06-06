## Adrian Antônio de Souza Gomes
## Matheus Henrique Heinzen

import hashlib
import os
import random
import string

ARQUIVO_USUARIOS = "usuarios.txt"
ITERACOES = 20

def hash_senha_forte(senha, iteracoes=ITERACOES):
    hash_valor = senha.encode()
    for _ in range(iteracoes):
        hash_valor = hashlib.sha256(hash_valor).digest()
    return hash_valor.hex()

def carregar_usuarios():
    usuarios = {}
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, "r") as f:
            for linha in f:
                partes = linha.strip().split(",")
                if len(partes) == 2:
                    nome, senha_hash = partes
                    usuarios[nome] = senha_hash
                else:
                    print(f"Linha inválida ignorada: {linha.strip()}")
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
        senha_hash = hash_senha_forte(senha)
        usuarios[nome] = senha_hash
        salvar_usuarios(usuarios)
        print("Usuário cadastrado com sucesso.")

    elif opcao == "2":
        nome, senha = obter_entrada_usuario()
        if nome in usuarios:
            senha_hash_armazenado = usuarios[nome]
            senha_hash_digitada = hash_senha_forte(senha)
            if senha_hash_digitada == senha_hash_armazenado:
                print("Autenticação bem-sucedida.")
                return
        print("Falha na autenticação.")
    else:
        print("Opção inválida.")

processar_usuario()