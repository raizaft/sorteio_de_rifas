import socket
import threading
from AVL import Tree
from sorteio import Sorteio
from participante import Participante

class Server:
    def __init__(self, host, port, message_size):
        self.__host = host
        self.__port = port
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__max_message_size = message_size
        self.__lock_clientes = threading.Lock()
        self.__lock_rifas = threading.Lock()
        self.__tree_clientes = Tree()
        self.__tree_sorteios = Tree()
    
    def start(self):
        self.__server_socket.bind((self.__host, self.__port))
        self.__server_socket.listen(1)
        print(f"Servidor aguardando conexões em {self.__host}:{self.__port}")
        
        try:
            self.accept_connections()
        except KeyboardInterrupt:
            self.__server_socket.close()
    
    def accept_connections(self):
        while True:
            client_socket, address = self.__server_socket.accept()
            print("Cliente conectado:", address)

            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()
    
    def handle_client(self, client_socket):
        client_socket.send("Conectado ao servidor!".encode())

        while True:
            try:
                msg_client = client_socket.recv(self.__max_message_size).decode()
            except ConnectionResetError:
                print("Cliente", client_socket.getpeername(), "desconectou!")
                break
        
            if msg_client.startswith("REGISTRAR"):
                self.registrar(client_socket, msg_client)

            if msg_client.startswith("LOGAR"):
                self.login(client_socket, msg_client)

            if msg_client.startswith("CRIAR"):
                self.criarSorteio(client_socket, msg_client)

            if msg_client == "VER":
                self.disponiveis(client_socket)

            if msg_client.startswith("DISPONIVEIS"):
                self.numerosDisponiveis(client_socket, msg_client)
            
            if msg_client.startswith("PARTICIPAR"):
                self.participar(client_socket, msg_client)

            if msg_client.startswith("PARTICIPANDO"):
                self.meusSorteios(client_socket, msg_client)

            if msg_client == "SAIR":
                resposta = 'OK'
                client_socket.send(resposta.encode())
                print("Cliente", client_socket.getpeername(), "desconectou!")

            if msg_client.startswith("SORTEIO"):
                self.imprimeSorteio(client_socket, msg_client)
            
            if msg_client.startswith("SORTEAR"):
                self.realizarSorteio(client_socket, msg_client)

                
    def registrar(self, client_socket, msg_cliente):
        with self.__lock_clientes:
            _, cpf, senha = msg_cliente.split()
            if not self.loginExiste(cpf):
                user = Participante(cpf, senha)
                self.__tree_clientes.insert(user)
                resposta = '200'
            else:
                resposta = '400'
            client_socket.send(resposta.encode())

    def login(self, client_socket, msg_cliente):
        _, cpf, senha = msg_cliente.split()
        if not self.loginExiste(cpf):
            resposta = '401'
        else:
            user = self.__tree_clientes.search(cpf)
            if user.value.senha == senha:
                resposta = cpf
            else:
                resposta = '402'
        client_socket.send(resposta.encode())
                    
    def loginExiste(self, cpf):
        if self.__tree_clientes.search(cpf) != None:
            return True
        
    def criarSorteio(self, client_socket, msg_cliente):
        _, nome, tamanho, cpf = msg_cliente.split()
        tamanho = int(tamanho)
        if self.__tree_sorteios.search(nome) == None:
            user = self.__tree_clientes.search(cpf)
            sorteio = Sorteio(nome, tamanho, user)
            self.__tree_sorteios.insert(sorteio)
            user.value.addCriados(sorteio)
            resposta = '201'
        else:
            resposta = '403'
        client_socket.send(resposta.encode())

    def disponiveis(self, client_socket):
        if self.__tree_sorteios.isEmpty():
            resposta = '404'
        else:
            resposta = self.__tree_sorteios.inOrder()
        client_socket.send(resposta.encode())

    def validaSorteio(self, nome):
        if self.__tree_sorteios.search(nome) != None:
            return True

    def numerosDisponiveis(self, client_socket, msg_cliente):
        _, nome = msg_cliente.split()
        if self.validaSorteio(nome):
            sorteio = self.__tree_sorteios.search(nome)
            resposta = sorteio.value.numeros_disponiveis()
            if resposta == -1:
                resposta = '407'
        else:
            resposta = '405'
        client_socket.send(resposta.encode())

    def participar(self, client_socket, msg_cliente):
        with self.__lock_clientes:
            _, nome, numero, cpf = msg_cliente.split()
            sorteio = self.__tree_sorteios.search(nome)
            user = self.__tree_clientes.search(cpf)
            sorteio.value.comprar(numero, user)
            if not user.value.estaParticipando(nome):
                user.value.addParticipando(sorteio.value)
            resposta = '202'
            client_socket.send(resposta.encode())

    def meusSorteios(self, client_socket, msg_cliente):
        _, cpf = msg_cliente.split()
        user = self.__tree_clientes.search(cpf)
        resposta = user.value.imprimeInfos()
        client_socket.send(resposta.encode())

    def imprimeSorteio(self, client_socket, msg_cliente):
        _, nome = msg_cliente.split()
        sorteio = self.__tree_sorteios.search(nome)
        nome = sorteio.value.nome
        tamanho = sorteio.value.tamanho
        resposta = f'{nome} | {tamanho}'
        client_socket.send(resposta.encode())

    def realizarSorteio(self, client_socket, msg_cliente):
        _, nome, cpf = msg_cliente.split()
        sorteio = self.__tree_sorteios.search(nome)
        criador = sorteio.value.adm
        if cpf == criador.value.cpf:
            sorteado, numero = sorteio.value.sortear().split()
            resposta = f'Número sorteado: {numero}\nVencedor: {sorteado}'
        else:
            resposta = '406'
        client_socket.send(resposta.encode())
