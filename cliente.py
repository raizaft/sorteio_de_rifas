import socket
import os
import sys

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

MAX_MESSAGE_SIZE = 1024
HOST = 'localhost'
PORT = 8888

if len(sys.argv) == 2:
    HOST = sys.argv[1]
elif len(sys.argv) == 3:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

CODIGOS_SERVIDOR = {
    '200': 'Usuário cadastrado com sucesso!',
    '201': 'Sorteio criado com sucesso.',
    '202': 'Compra realizada.',
    '400': 'Usuário já cadastrado!',
    '401': 'Usuário não encontrado.',
    '402': 'Senha incorreta!',
    '403': 'Sorteio já existe.',
    '404': 'Nenhum sorteio disponível',
    '405': 'Sorteio não existe!',
    '406': 'Você não tem permissão para realizar esse sorteio.',
    '407': 'Números esgotados.'
}

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    mensagem_servidor = client_socket.recv(MAX_MESSAGE_SIZE).decode()
    print(mensagem_servidor)

    def enviar_mensagem(mensagem):
        client_socket.send(mensagem.encode())
        return client_socket.recv(MAX_MESSAGE_SIZE).decode()
    
    while True:
        op = mostrar_menu_inicial()
        if op == '1':
            cls()
            registro = registrar()
            if registro != -1:
                codigo = enviar_mensagem(f'REGISTRAR {registro}')
                cls()
                if codigo == "200":
                    print(CODIGOS_SERVIDOR['200'])
                elif codigo == '400':
                    print(CODIGOS_SERVIDOR['400'])
        elif op == '2':
            cls()
            logar = login()
            if logar != -1:
                codigo = enviar_mensagem(f'LOGAR {logar}')
                cls()
                if codigo == '401':
                    print(CODIGOS_SERVIDOR['401'])
                elif codigo == '402':
                    print(CODIGOS_SERVIDOR['402'])
                else:
                    cls()
                    print(f"Logado como: {codigo}")
                    while True:
                        choice = menu_principal()
                        if choice == '1':
                            cls()
                            sorteio = criarSorteio()
                            resposta = enviar_mensagem(f'CRIAR {sorteio} {codigo}')
                            cls()
                            if resposta == '403':
                                print(CODIGOS_SERVIDOR['403'])
                            else:
                                print(CODIGOS_SERVIDOR['201'])
                        elif choice == '2':
                            cls()
                            print('SORTEIOS DISPONÍVEIS\n')
                            resposta = enviar_mensagem('VER')
                            if resposta == '404':
                                print(CODIGOS_SERVIDOR['404'])
                            else:
                                print(resposta)
                        elif choice == '3':
                            cls()
                            print('SORTEIOS DISPONÍVEIS\n')
                            resposta = enviar_mensagem('VER')
                            if resposta == '404':
                                print(CODIGOS_SERVIDOR['404'])
                            else:
                                print(resposta)
                                nome = input('Nome do sorteio que deseja participar: ')
                                cls()
                                resposta = enviar_mensagem(f'DISPONIVEIS {nome}')
                                if resposta == '405':
                                    cls()
                                    print(CODIGOS_SERVIDOR['405'])
                                elif resposta == '407':
                                    cls()
                                    print(CODIGOS_SERVIDOR['407'])
                                else:
                                    print(f'Sorteio - {nome}')
                                    print('Números disponíveis:')
                                    print('')
                                    print(resposta)
                                    while True:
                                        numero = int(input('\nNúmero que deseja comprar: '))
                                        if intNaString(resposta, numero):
                                            break
                                        else:
                                            cls()
                                            print('Insira um número válido.')
                                    resposta = enviar_mensagem(f'PARTICIPAR {nome} {numero} {codigo}')
                                    if resposta == '202':
                                        cls()
                                        print(CODIGOS_SERVIDOR['202'])
                        elif choice == '4':
                            cls()
                            resposta = enviar_mensagem(f'PARTICIPANDO {codigo}')
                            print(resposta)
                            escolha = input('\nDeseja realizar um sorteio (s/n): ').lower()
                            cls()
                            if escolha == 's':
                                nome = input('Nome do sorteio que deseja realizar: ')
                                cls()
                                resposta = enviar_mensagem(f'DISPONIVEIS {nome}')
                                if resposta == '405':
                                    cls()
                                    print('Sorteio não existe.')
                                else:
                                    sortear = enviar_mensagem(f'SORTEIO {nome}')
                                    print(sortear)
                                    resultado = enviar_mensagem(f'SORTEAR {nome} {codigo}')
                                    if resultado == '406':
                                        print('Você não tem permissão para realizar esse sorteio.')
                                    else:
                                        print(resultado)
                        elif choice == '5':
                            resposta = enviar_mensagem(f'RESULTADOS')
                        elif choice == '6':
                            cls()
                            break
        elif op == '3':
            cls()
            resposta = enviar_mensagem('SAIR')
            if resposta == 'OK':
                break

def input_cpf():
    while True:
        cpf = input('CPF: ')
        if cpf == 'exit':
            return -1
        if validarCPF(cpf):
            return cpf
        else:
            cls()
            print('CPF inválido! Tente Novamente.')

def login():
    cpf = input_cpf()
    if cpf == -1:
        return -1
    senha = input('Senha: ')
    login = f'{cpf} {senha}'
    return login

def registrar():
    cpf = input_cpf()
    if cpf == -1:
        return -1
    senha = input('Senha: ')
    registro = f'{cpf} {senha}'
    return registro

def intNaString(s, num):
    if str(num) in s:
        return True

def validarCPF(cpf):
        cpf = ''.join(filter(str.isdigit, cpf))
        if len(cpf) != 11:
            return False
        if cpf == cpf[0] * 11:
            return False
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        resto = soma % 11
        if resto < 2:
            digito1 = 0
        else:
            digito1 = 11 - resto
        if digito1 != int(cpf[9]):
            return False
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        resto = soma % 11
        if resto < 2:
            digito2 = 0
        else:
            digito2 = 11 - resto
        if digito2 != int(cpf[10]):
            return False
        return True

def criarSorteio():
    print('CRIAR SORTEIO\n')
    while True:
        nome = input('Nome do sorteio (sem espaços): ')
        cls()
        if ' ' not in nome:
            break
        print('Nome inválido!')
    while True:
        try:
            tamanho = int(input('Quantidade de números do sorteio: '))
            if tamanho > 0:
                break
            else:
                cls()
                print('Insira um número maior que 0!')
        except ValueError:
            cls()
            print("Por favor, digite um número inteiro válido.")
    return f'{nome} {tamanho}'

def menu_principal():
    while True:
            print('''
MENU PRINCIPAL              

1. Criar Sorteio
2. Ver Sorteios
3. Participar de Sorteio
4. Meus Sorteios
5. Resultados
6. Sair
                ''')
            op = input("Digite a opção desejada: ")

            if op not in ('1','2','3','4','5','6'):
                cls()
                print('Digite uma opção válida!')
            return op
                

def mostrar_menu_inicial():
    while True:
        print('''
1. Registrar
2. Login
3. Sair       
    ''')
        op = input('Digite a opção desejada: ')
        if op not in ('1','2','3'):
            cls()
            print('Digite uma opção válida!')
        return op
    
main()