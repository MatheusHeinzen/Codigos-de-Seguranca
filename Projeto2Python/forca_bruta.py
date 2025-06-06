import hashlib
import itertools
import string
import time

ARQUIVO_USUARIOS = "usuarios.txt"
ITERACOES_REFORCADO = 20

def hash_normal(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def hash_reforcado(senha, iteracoes=ITERACOES_REFORCADO):
    hash_valor = senha.encode()
    for _ in range(iteracoes):
        hash_valor = hashlib.sha256(hash_valor).digest()
    return hash_valor.hex()

def carregar_hashes():
    hashes = {}
    with open(ARQUIVO_USUARIOS, "r") as f:
        for linha in f:
            nome, senha_hash = linha.strip().split(",")
            hashes[nome] = senha_hash
    return hashes

def força_bruta_sha256(hash_alvo):
    caracteres = string.ascii_letters + string.digits  # letras e números
    total_tentativas = 0
    
    print(f"Tentando quebrar hash: {hash_alvo}")

    inicio_normal = time.time()
    for tentativa in itertools.product(caracteres, repeat=4):
        tentativa_str = ''.join(tentativa)
        total_tentativas += 1
        if hash_normal(tentativa_str) == hash_alvo:
            tempo_normal = time.time() - inicio_normal
            print(f"Senha encontrada (normal): {tentativa_str}")
            print(f"Tentativas: {total_tentativas} | Tempo: {tempo_normal:.2f}s")
            return tentativa_str, "normal", tempo_normal
    
    inicio_reforcado = time.time()
    for tentativa in itertools.product(caracteres, repeat=4):
        tentativa_str = ''.join(tentativa)
        total_tentativas += 1
        if hash_reforcado(tentativa_str) == hash_alvo:
            tempo_reforcado = time.time() - inicio_reforcado
            print(f"Senha encontrada (reforçado): {tentativa_str}")
            print(f"Tentativas: {total_tentativas} | Tempo: {tempo_reforcado:.2f}s")
            return tentativa_str, "reforçado", tempo_reforcado
    
    return None, "não encontrada", 0

def quebrar_todas_as_senhas():
    hashes = carregar_hashes()
    tempos = []
    resultados = {}

    print("Iniciando quebra de senhas por força bruta...\n")
    tempo_total_inicio = time.time()

    for nome, senha_hash in list(hashes.items())[:4]:  # apenas os 4 primeiros usuários
        print(f"\nQuebrando senha de: {nome}")
        senha_encontrada, tipo_hash, tempo = força_bruta_sha256(senha_hash)
        tempos.append(tempo)
        resultados[nome] = (senha_encontrada, tipo_hash, tempo)
        if senha_encontrada:
            print(f"Senha encontrada: {senha_encontrada} | Tipo: {tipo_hash} | Tempo: {tempo:.2f}s")
        else:
            print("Senha não encontrada")

    tempo_total_fim = time.time()
    tempo_total = tempo_total_fim - tempo_total_inicio

    print(f"\nResumo:")
    for nome, (senha, tipo, tempo) in resultados.items():
        print(f"{nome}: {senha if senha else 'Não quebrada'} ({tipo}) - {tempo:.2f}s")
    
    print(f"\nTempo total: {tempo_total:.2f} segundos")
    if tempos:
        print(f"Tempo médio por senha: {sum(tempos)/len(tempos):.2f} segundos")
    
    return resultados

quebrar_todas_as_senhas()