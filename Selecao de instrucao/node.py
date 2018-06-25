class Node():
    
    def __init__(self,instrucao,left,right):
        self.instrucao = instrucao
        self.left = left
        self.right = right
        
    def __str__(self):
        return self.to_print(self)

    def to_print(self,tree, level=0) :
        if tree == None :return '' #'\t'*level + '|- NULL' + '\n'
        return ( self.to_print(tree.right, level+1) + '\n' +
                ('\t'*level + '|--' + str(tree.instrucao)) + '\n' + 
                self.to_print(tree.left, level+1))