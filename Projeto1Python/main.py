# Matheus Henrique Heinzen e Vinicius Lima Teider

import json
import os
import getpass

USUARIOS_JSON = "usuarios.json"
PERMISSOES_JSON = "permissoes.json"

def inicializar_dados():
    if not os.path.exists(USUARIOS_JSON):
        usuarios = {
            "adm": "admin123",
            "Matheus": "senha123",
            "Maysa": "pass456",
            "Vinicius": "segredo",
            "Manuel Gomes": "qwerty"
        }
        with open(USUARIOS_JSON, "w") as arquivo:
            json.dump(usuarios, arquivo, indent=4)
    if not os.path.exists(PERMISSOES_JSON):
        permissoes = [
            {"nome": "adm", "permissoes": {"leitura": ["config.json"], "escrita": ["config.json"], "apagar": ["config.json"]}},
            {"nome": "Matheus", "permissoes": {"leitura": ["dados.csv"], "escrita": [], "apagar": []}},
            {"nome": "Maysa", "permissoes": {"leitura": ["relatorio.pdf"], "escrita": ["relatorio.pdf"], "apagar": []}},
            {"nome": "Vinicius", "permissoes": {"leitura": [], "escrita": ["anotacoes.txt"], "apagar": []}},
            {"nome": "Manuel Gomes", "permissoes": {"leitura": ["manual.pdf"], "escrita": [], "apagar": ["manual.pdf"]}}
        ]
        with open(PERMISSOES_JSON, "w") as arquivo:
            json.dump(permissoes, arquivo, indent=4)

def carregar_usuarios():
    with open(USUARIOS_JSON, "r") as arquivo:
        return json.load(arquivo)

def salvar_usuarios(usuarios):
    with open(USUARIOS_JSON, "w") as arquivo:
        json.dump(usuarios, arquivo, indent=4)

def carregar_permissoes():
    with open(PERMISSOES_JSON, "r") as arquivo:
        return json.load(arquivo)

def salvar_permissoes(permissoes):
    with open(PERMISSOES_JSON, "w") as arquivo:
        json.dump(permissoes, arquivo, indent=4)

def autenticar(login, senha):
    usuarios = carregar_usuarios()
    return usuarios.get(login) == senha

def cadastrar_usuario():
    usuarios = carregar_usuarios()
    login = input("Digite o novo login: ")
    if login in usuarios:
        print("Usuário já existe!")
        return
    senha = getpass.getpass("Digite a senha: ")
    usuarios[login] = senha
    salvar_usuarios(usuarios)
    permissoes = carregar_permissoes()
    permissoes.append({"nome": login, "permissoes": {"leitura": [], "escrita": [], "apagar": []}})
    salvar_permissoes(permissoes)
    print("Usuário cadastrado com sucesso!")

def verificar_permissao(usuario, recurso, acao):
    permissoes = carregar_permissoes()
    for perm in permissoes:
        if perm["nome"] == usuario:
            return recurso in perm["permissoes"].get(acao, [])
    return False

def editar_permissoes():
    login = input("Digite o login do administrador: ")
    senha = getpass.getpass("Digite a senha do administrador: ")
    if login != "adm" or not autenticar(login, senha):
        print("Apenas o administrador pode editar permissões!")
        return
    permissoes = carregar_permissoes()
    usuario = input("Digite o login do usuário para editar permissões: ")
    for perm in permissoes:
        if perm["nome"] == usuario:
            print("Permissões atuais:", perm["permissoes"])
            recurso = input("Digite o nome do arquivo que deseja modificar: ")
            acao = input("Escolha a ação (leitura, escrita, apagar): ")
            if recurso in perm["permissoes"].get(acao, []):
                perm["permissoes"][acao].remove(recurso)
                print("Permissão removida com sucesso!")
            else:
                perm["permissoes"].setdefault(acao, []).append(recurso)
                print("Permissão adicionada com sucesso!")
            salvar_permissoes(permissoes)
            return
    print("Usuário não encontrado!")

def solicitar_permissao(usuario):
    while True:
        recurso = input("Digite o nome do arquivo (ou 'sair' para voltar ao menu): ")
        if recurso.lower() == "sair":
            break
        acao = input("Escolha a ação (leitura, escrita, apagar): ")
        if verificar_permissao(usuario, recurso, acao):
            print("Acesso permitido")
        else:
            print("Acesso negado")

def menu():
    inicializar_dados()
    while True:
        escolha = input("Escolha uma opção:\n1 - Login\n2 - Cadastrar usuário\n3 - Editar permissões\n4 - Sair\nOpção: ")
        if escolha == "1":
            login = input("Digite seu login: ")
            senha = getpass.getpass("Digite sua senha: ")
            if autenticar(login, senha):
                print(f"Seja bem-vindo, {login}!")
                solicitar_permissao(login)
            else:
                print("Usuário ou senha inválidos")
        elif escolha == "2":
            cadastrar_usuario()
        elif escolha == "3":
            editar_permissoes()
        elif escolha == "4":
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu()