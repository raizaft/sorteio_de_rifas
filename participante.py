from sorteio import Sorteio
from AVL import Tree

class Participante:
    def __init__(self, cpf, senha):
        self.__cpf = cpf
        self.__senha = senha
        self.__participando = []
        self.__criados = []
    
    @property
    def cpf(self):
        return self.__cpf

    @property
    def senha(self):
        return self.__senha
    
    @property
    def participando(self):
        return self.__participando
    
    @property
    def criados(self):
        return self.__criados
    
    def addParticipando(self, sorteio):
        self.__participando.append(sorteio)

    def addCriados(self, sorteio):
        self.__criados.append(sorteio)

    def verificarCriados(self, nome):
        v = []
        for i in range(len(self.criados)):
            v.append(self.criados[i].nome)
        if nome in v:
            return True
        else:
            return False
        
    def estaParticipando(self, nome):
        count = 0
        for i in range(len(self.participando)):
            if self.participando[i].nome == nome:
                count += 1
        if count > 0:
            return True

    def imprimeInfos(self):
        criados = ''
        for i in range(len(self.criados)):
            if i < (len(self.criados)-1):
                criados += self.criados[i].nome + ' | '
            else:
                criados += self.criados[i].nome
        part = ''
        for j in range(len(self.participando)):
            if j < (len(self.participando)-1):
                part += self.participando[j].nome + ' | '
            else:
                part += self.participando[j].nome
        s = f'CPF: {self.__cpf}\n\nSorteios Criados: {criados}\n\nParticipando: {part}'
        return s

    def __lt__(self, other):
        return self.__cpf < other
    
    def __gt__(self, other):
        return self.__cpf > other

    def __eq__(self, other):
        return self.__cpf == other

    def __hash__(self):
        return hash(self.__cpf)