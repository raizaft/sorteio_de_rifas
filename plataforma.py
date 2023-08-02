import os

from AVL import Tree

from sorteio import Sorteio
from participante import Participante

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

class Plataforma:
    def __init__(self, tree_sorteios, tree_clientes):
        self.__tree_sorteios = tree_sorteios
        self.__tree_clientes = tree_clientes       

    def criarSorteio(self, nome, tamanho, user):
        if self.__tree_sorteios.search(nome) == None:
            sorteio = Sorteio(nome, tamanho, user)
            self.__tree_sorteios.insert(sorteio)
            user.value.addCriados(sorteio)
            print('Sorteio criado com sucesso!')

    def verificarSorteio(self, user, nome):
        if user.value.verificarCriados(nome):
            return True
        
    def validaSorteio(self, nome):
        if self.__tree_sorteios.search(nome) != None:
            return True
        
    def realizarSorteio(self, nome):
        sorteio = self.__tree_sorteios.search(nome)
        sorteado = sorteio.value.sortear()
        return sorteado

    def participar(self, nome, numero, user):
        sorteio = self.__tree_sorteios.search(nome)
        sorteio.value.comprar(numero, user)
        user.value.addParticipando(nome)

    def disponiveis(self, nome):
        sorteio = self.__tree_sorteios.search(nome)
        return sorteio.value.disponiveis()

    def menu_principal(self, user):
        while True:
            print('''
    MENU PRINCIPAL              

    1. Criar Sorteio
    2. Ver Sorteios
    3. Participar de Sorteio
    4. Meus Sorteios
    5. Sair
                ''')
            op = input("Digite a opção desejada: ")

            if op not in ('1','2','3','4','5'):
                cls()
                print('Digite uma opção válida!')
            elif op == '1':
                cls()
                print('CRIAR SORTEIOS\n')
                nome = input('Nome do sorteio: ')
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
                cls()
                self.criarSorteio(nome, tamanho, user)
            elif op == '2':
                cls()
                print('SORTEIOS DISPONÍVEIS\n')
                self.__tree_sorteios.inOrder()
            elif op == '3':
                cls()
                print('SORTEIOS DISPONÍVEIS\n')
                self.__tree_sorteios.inOrder()
                nome = input('Nome do sorteio que deseja participar: ')
                if self.validaSorteio(nome):
                    print(self.disponiveis(nome))
                    numero = int(input("Digite o número que deseja comprar: "))
                    self.participar(nome, numero, user)
            elif op == '4':
                cls()
                print('MEUS SORTEIOS\n')
                user.value.imprimeInfos()
                choice = input('Deseja realizar um sorteio (s/n)? ').lower()
                if choice == 's':
                    cls()
                    nome = input('Nome do sorteio que deseja realizar: ')
                    if self.verificarSorteio(user, nome):
                        resultado = self.realizarSorteio(nome)
                        print(f'Sorteio: {nome}\nResultado: {resultado}')
            elif op == '5':
                cls()
                break

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

    def loginExiste(self, cpf):
        if self.__tree_clientes.search(cpf) != None:
            return False
        else:
            return True

    def login(self, cpf, senha):
        user = self.__tree_clientes.search(cpf)
        if user.value.senha == senha:
            return user
        else:
            return -1

    def registrar(self, cpf, senha):
        user = Participante(cpf, senha)
        self.__tree_clientes.insert(user)

    def menu_inicial(self):
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
            elif op == '1':
                cls()
                while True:
                    cpf = input('CPF: ')
                    if self.validarCPF(cpf):
                        break
                    else:
                        cls()
                        print('CPF inválido! Tente Novamente.')
                senha = input('Senha: ')
                cls()
                if self.loginExiste(cpf):
                    self.registrar(cpf, senha)
                    print('Usuário cadastrado com sucesso')
                else:
                    print('Usuário já cadastrado.')
            elif op == '2':
                cls()
                while True:
                    cpf = input('CPF: ')
                    if self.validarCPF(cpf):
                        break
                    else:
                        cls()
                        print('CPF inválido! Tente Novamente.')
                senha = input('Senha: ')
                cls()
                if self.loginExiste(cpf) == True:
                    print('Usuário não cadastrado.')
                else:
                    user = self.login(cpf, senha)
                    if user == -1:
                        print('Senha incorreta!')
                    else:
                        self.menu_principal(user)
            elif op == '3':
                cls()
                break