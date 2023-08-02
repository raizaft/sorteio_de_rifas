class Node(object): 
    def __init__(self, value): 
        self.value = value 
        self.left = None
        self.right = None
        self.height = 1

    def __str__(self):
        return f'|{self.value}:h={self.height}|'

class Tree(object): 
    def __init__(self, value:object = None):
        if value is None:
            self.__root = None
        else:
            self.__root = self.insert(value)
    
    def getRoot(self)->any:
        return None if self.__root is None else self.__root.value

    def isEmpty(self)->bool:
        return self.__root == None

    def search(self, key:any )->any:
        if( self.__root != None ):
            value = self.__searchData(key, self.__root)
            return None if value is None else value
        else:
            return None
    
    def __searchData(self, key:any, node:Node)->Node:
        if ( key == node.value):
            return node
        elif ( key < node.value and node.left != None):
            return self.__searchData( key, node.left())
        elif ( key > node.value and node.right != None):
            return self.__searchData( key, node.right)
        else:
            return None
    
    def __len__(self):
        return self.count()
    
    def insert(self, key:object):
        if(self.__root == None):
            self.__root = Node(key)
        else:
            self.__root = self.__insert(self.__root, key)
  
    def __insert(self, root, key):
        if not root: 
            return Node(key) 
        elif key < root.value: 
            root.left = self.__insert(root.left, key) 
        else: 
            root.right = self.__insert(root.right, key) 
        root.height = 1 + max(self.__getHeight(root.left), 
                              self.__getHeight(root.right)) 
        balance = self.__getBalance(root) 
        if balance > 1 and key < root.left.value: 
            return self.__rightRotate(root) 
        if balance < -1 and key > root.right.value: 
            return self.__leftRotate(root) 
        if balance > 1 and key > root.left.value: 
            root.left = self.__leftRotate(root.left) 
            return self.__rightRotate(root) 
        if balance < -1 and key < root.right.value: 
            root.right = self.__rightRotate(root.right) 
            return self.__leftRotate(root) 
        return root 
  
    def __leftRotate(self, p:Node)->Node: 
        u = p.right 
        T2 = u.left 
        u.left = p 
        p.right = T2 
        p.height = 1 + max(self.__getHeight(p.left), 
                         self.__getHeight(p.right)) 
        u.height = 1 + max(self.__getHeight(u.left), 
                         self.__getHeight(u.right)) 
        return u 
  
    def __rightRotate(self, p:Node)->Node: 
        u = p.left 
        T2 = u.right 
        u.right = p 
        p.left = T2 
        p.height = 1 + max(self.__getHeight(p.left), 
                        self.__getHeight(p.right)) 
        u.height = 1 + max(self.__getHeight(u.left), 
                        self.__getHeight(u.right)) 
        return u 
  
    def __getHeight(self, node:Node)->int: 
        if node is None: 
            return 0
  
        return node.height 
  
    def __getBalance(self, node:Node)->int: 
        if not node: 
            return 0
        return self.__getHeight(node.left) - self.__getHeight(node.right)
    
    def inOrder(self):
        values_list = []
        self.__inOrder(self.__root, values_list)
        return "\n".join(str(value) for value in values_list)

    def __inOrder(self, root, values_list): 
        if not root: 
            return
        self.__inOrder(root.left, values_list)
        values_list.append(root.value)
        self.__inOrder(root.right, values_list)
    
if __name__ == '__main__':
    a = Tree()
    a.insert(5)
    a.insert(8)
    a.insert(3)
    a.insert(6)

    print(a.inOrder())
