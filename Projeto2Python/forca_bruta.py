## Adrian Antônio de Souza Gomes
## Matheus Henrique Heinzen

import hashlib
import itertools
import string
import time

ARQUIVO_USUARIOS = "usuarios.txt"

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def carregar_hashes():
    hashes = {}
    with open(ARQUIVO_USUARIOS, "r") as f:
        for linha in f:
            nome, senha_hash = linha.strip().split(",")
            hashes[nome] = senha_hash
    return hashes

def força_bruta_sha256(hash_alvo):
    caracteres = string.ascii_letters + string.digits  # letras e números
    for tentativa in itertools.product(caracteres, repeat=4):
        tentativa_str = ''.join(tentativa)
        if hash_senha(tentativa_str) == hash_alvo:
            return tentativa_str
    return None

def quebrar_todas_as_senhas():
    hashes = carregar_hashes()
    tempos = []
    resultados = {}

    print("Iniciando quebra de senhas por força bruta...\n")
    tempo_total_inicio = time.time()

    for nome, senha_hash in list(hashes.items())[:4]:  # apenas os 4 primeiros usuários
        print(f"Quebrando senha de: {nome}")
        inicio = time.time()
        senha_encontrada = força_bruta_sha256(senha_hash)
        fim = time.time()
        tempo = fim - inicio
        tempos.append(tempo)
        resultados[nome] = (senha_encontrada, tempo)
        print(f"Senha encontrada: {senha_encontrada} | Tempo: {tempo:.2f} segundos\n")

    tempo_total_fim = time.time()
    tempo_total = tempo_total_fim - tempo_total_inicio

    print(f"\nTempo total: {tempo_total:.2f} segundos")
    print("Tempo médio por senha:", f"{(sum(tempos)/len(tempos)):.2f} segundos")
    return resultados

quebrar_todas_as_senhas()
