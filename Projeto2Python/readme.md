# Desempenho de Hash Criptográfico

## Desenvolvido por
- **Desenvolvedor Principal**: Adrian Antônio de Souza Gomes
- **Desenvolvedor Auxiliar e Tester**: Matheus Henrique Heinzen
## 1. Autenticação
Arquivo 1 `cadastro_normal.py` que implementa uma aplicação que possui a funcionalidade de cadastrar e autenticar usuário.

Um usuário possui:
- Nome (String de 4 caracteres)
- Senha (String de 4 caracteres)

Além disso, o cadastro dos usuários é armazenado em um arquivo txt, a aplicação utiliza SHA-256 da biblioteca hashlib para realizar o hash para o armazenamento da senha.

## 2. Quebra de Hash Criptográfico

Algoritmo/código `forca_bruta.py` de força bruta para SHA-256 e processe o arquivo que contém as
senhas armazenadas conforme implementado na Seção 1. Computa o tempo necessário para realizar
a quebra de hash de 4 usuários (tempo total e tempo por senha). Código feito com a ajuda do ChatGPT


## 3. Solução para redução de Força Bruta

Keystretching foi a solução no arquivo `cadastro_reforcado.py` , ele aplica o hash na senha milhares de vezes (como definido no código python na var `iteracoes`) fazendo com que a senha fique praticamente inquebrável para o brute force criado antes de aplicar a solução. Também deixa cada tentativa de quebrar a senha muito mais lenta do que o normal, pois demoraria horas e até dias para quebrar uma senha ou nem conseguiria quebrar.