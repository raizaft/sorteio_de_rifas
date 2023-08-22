class Entry:
    __slots__ = ("__chave", "__valor")

    def __init__(self, chave, valor):
        self.__chave = chave 
        self.__valor = valor

    @property
    def chave(self):
        return self.__chave

    @property
    def valor(self):
        return self.__valor

class HashTable:
    def __init__(self, max):
        self.__table = [[] for i in range(max)]
        self.__capacidade = max
        self.__ocupados = 0
    
    def __len__(self):
        return self.__ocupados

    def put(self, chave, valor):
        return self.__put(chave, valor)

    def __put(self, chave, valor):
        indice = int(chave)

        for entry in self.__table[indice]:
            if entry.chave == indice:
                return -1

        self.__table[indice].append(Entry(chave, valor))
        return indice
    
    def search(self, key):
        slot = self.__hash(key)
        if not self.__table[slot]:
            return False
        else:
            return True

    def __hash(self, key:any):
        return hash(key) % self.__capacidade
    
    def get(self, chave):
        return self.__get(chave)

    def __get(self, chave):
        indice = chave
        chave = str(chave)

        for entry in self.__table[indice]:
            if entry.chave == chave:
                node = entry.valor

        return node
    
    def __str__(self):
        s = ''
        for i in range(self.__capacidade):
            if not self.__table[i]:
                s += f'{i}:\n'
            else:
                s += f'{i}: {self.__table[i]}\n'
        return s
    
if __name__ == '__main__':
    t = HashTable(4)
    t.put(1, 'comprei 1')
    t.put(2, 'comprei 2')
    t.put(3, 'comprei 3')
    t.put(0, 'comprei 0')
    print(t)