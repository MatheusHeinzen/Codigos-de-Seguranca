import token
import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyCwKhURYwUDjfEDwqIf_pcq2NNqBm3r1IY",
    "authDomain": "seginfo-1.firebaseapp.com",
    "projectId": "seginfo-1",
    "storageBucket": "seginfo-1.firebasestorage.app",
    "messagingSenderId": "128973867679",
    "appId": "1:128973867679:web:0f625fd06c581487a130aa",
    "databaseURL": ""
}

APP = pyrebase.initialize_app(firebaseConfig)
AUTH = APP.auth()

while True:
    loginCadastro = input("Digite 1 para fazer cadastro ou 2 para login: ")
    if loginCadastro == "1":
        emailCadastro = input('Digite seu email que exista, obrigado: ')
        senhaCadastro = input('Senha: ')
        tokenCadastro = AUTH.create_user_with_email_and_password(emailCadastro, senhaCadastro)

        print("Cadastro realizado com sucesso!")
    elif loginCadastro == "2":
        emailLogin = input("Digite seu email: ")
        senhaLogin = input("Digite sua senha: ")
        tokenLogin = AUTH.sign_in_with_email_and_password(emailLogin, senhaLogin)
        logado = True
        user = AUTH.get_account_info(tokenLogin['idToken'])


        AUTH.send_email_verification(tokenLogin['idToken'])
        print("E-mail de verificação enviado!")
        while logado:
            menuLogado = input("1 - Fazer nada\n2 - Nada denovo\n3 - Mudar a senha")
            if menuLogado == "3":
                AUTH.send_password_reset_email(emailLogin)


    else:
        print("Opção inválida")