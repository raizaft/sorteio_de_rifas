from HashTable import HashTable
import random

class Sorteio:
    def __init__(self, nome, tamanho, adm):
        self.__nome = nome
        self.tamanho = tamanho
        self.numeros = HashTable(tamanho)
        self.__adm = adm

    @property
    def nome(self):
        return self.__nome
    
    @property
    def adm(self):
        return self.__adm
    
    def comprar(self, numero, participante:object):
        self.numeros.put(numero, participante)

    def numeros_disponiveis(self):
        s = ''
        for i in range(self.tamanho):
            if not self.numeros.search(i) and i != self.tamanho-1:
                s += str(i) + ' | '
            elif not self.numeros.search(i) and i == self.tamanho-1:
                s += str(i)
        if s == '':
            return -1
        else:
            return s
    
    def comprados(self):
        s = []
        for i in range(self.tamanho):
            if self.numeros.search(i):
                s.append(i)
        return s
    
    def sortear(self):
        s = self.comprados()
        slot = random.choice(s)
        return slot
    
    def vencedor(self, slot):
        sorteado = self.numeros.get(slot)
        return sorteado
    
    def imprime(self):
        s = f'{self.__nome} | {self.tamanho}\n'
        return s

    def __str__(self):
        s = f'{self.__nome} | {self.tamanho}\n'
        return s
    
    def __lt__(self, other):
        return self.__nome < other

    def __gt__(self, other):
        return self.__nome > other

    def __eq__(self, other):
        return self.__nome == other
    
if __name__ == '__main__':
    s = Sorteio('amora', 4, 'raiza')
    s.comprar(0, 'lucas')
    #s.comprar(1, 'lucas')
    #s.comprar(2, 'lucas')
    #s.comprar(3, 'lucas')
    print(s.numeros_disponiveis())
    print(s.comprados())