## Adrian Antônio de Souza Gomes
## Matheus Henrique Heinzen

import hashlib
import os
import random
import string

pARQUIVO_USUARIOS = "usuarios.txt"
pITERACOES = 200000  # aumento grande para dificultar força bruta

def phash_senha_forte(senha, iteracoes=pITERACOES):
    hash_valor = senha.encode()
    for _ in range(iteracoes):
        hash_valor = hashlib.sha256(hash_valor).digest()
    return hash_valor.hex()

def pcarregar_usuarios():
    usuarios = {}
    if os.path.exists(pARQUIVO_USUARIOS):
        with open(pARQUIVO_USUARIOS, "r") as f:
            for linha in f:
                partes = linha.strip().split(",")
                if len(partes) == 2:
                    nome, senha_hash = partes
                    usuarios[nome] = senha_hash
                else:
                    print(f"Linha inválida ignorada: {linha.strip()}")
    return usuarios

def psalvar_usuarios(usuarios):
    with open(pARQUIVO_USUARIOS, "w") as f:
        for nome, senha_hash in usuarios.items():
            f.write(f"{nome},{senha_hash}\n")

def pobter_entrada_usuario():
    nome = input("Nome (4 caracteres): ").strip()
    senha = input("Senha (4 caracteres): ").strip()
    if len(nome) != 4 or len(senha) != 4:
        print("Nome e senha devem ter exatamente 4 caracteres.")
        return None, None
    return nome, senha

def pprocessar_usuario():
    usuarios = pcarregar_usuarios()
    print("1 - Cadastrar\n2 - Autenticar")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        nome, senha = pobter_entrada_usuario()
        if not nome or nome in usuarios:
            print("Usuário inválido ou já existe.")
            return
        senha_hash = phash_senha_forte(senha)
        usuarios[nome] = senha_hash
        psalvar_usuarios(usuarios)
        print("Usuário cadastrado com sucesso.")

    elif opcao == "2":
        nome, senha = pobter_entrada_usuario()
        if nome in usuarios:
            senha_hash_armazenado = usuarios[nome]
            senha_hash_digitada = phash_senha_forte(senha)
            if senha_hash_digitada == senha_hash_armazenado:
                print("Autenticação bem-sucedida.")
                return
        print("Falha na autenticação.")
    else:
        print("Opção inválida.")

while True:
    pprocessar_usuario()
