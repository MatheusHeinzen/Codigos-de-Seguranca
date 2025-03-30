# Matheus Henrique Heinzen
import json
import os
import getpass
ARQUIVO_JSON = "usuariosLogin1.json"
BLOQUEADOS_JSON = "bloqueadosLogin1.json"
TENTATIVAS_PERMITIDAS = 5
def inicializarDados():
    if not os.path.exists(ARQUIVO_JSON):
        usuarios = [
            {"nome": "Matheus", "senha": "passw0rd"},
            {"nome": "Bruna", "senha": "passw0rd1"},
            {"nome": "Vini", "senha": "1011"}
        ]
        with open(ARQUIVO_JSON, "w") as arquivo:
            json.dump(usuarios, arquivo, indent=4)
    if not os.path.exists(BLOQUEADOS_JSON):
        with open(BLOQUEADOS_JSON, "w") as arquivo:
            json.dump({}, arquivo, indent=4)
def carregarUsuarios():
    with open(ARQUIVO_JSON, "r") as arquivo:
        return json.load(arquivo)
def carregarBloqueados():
    with open(BLOQUEADOS_JSON, "r") as arquivo:
        return json.load(arquivo)
def salvarBloqueados(bloqueados):
    with open(BLOQUEADOS_JSON, "w") as arquivo:
        json.dump(bloqueados, arquivo, indent=4)
def autenticar(login, senha):
    usuarios = carregarUsuarios()
    for usuario in usuarios:
        if usuario["nome"] == login and usuario["senha"] == senha:
            return True
    return False
inicializarDados()
bloqueados = carregarBloqueados()
login = input("Digite seu login: ")
if login in bloqueados and bloqueados[login] >= TENTATIVAS_PERMITIDAS:
    print("Usuário bloqueado. Contate o suporte.")
else:
    tentativas = bloqueados.get(login, 0)
while tentativas < TENTATIVAS_PERMITIDAS:
    senha = getpass.getpass("Digite sua senha: ")
    if autenticar(login, senha):
        print(f"Seja bem-vindo, {login}!")
        if login in bloqueados:
            del bloqueados[login]
            salvarBloqueados(bloqueados)
        break
    else:
        tentativas += 1
        print(f"Login ou senha incorretos. Tentativa {tentativas}/{TENTATIVAS_PERMITIDAS}.")
        if tentativas >= TENTATIVAS_PERMITIDAS:
            print("Usuário bloqueado devido a múltiplas tentativas erradas.")
            bloqueados[login] = tentativas
            salvarBloqueados(bloqueados)
        else:
            bloqueados[login] = tentativas
            salvarBloqueados(bloqueados)