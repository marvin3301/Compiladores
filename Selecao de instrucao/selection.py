from node import Node

class selection():
    din = [] 

    jouette_exp = {
        'ADD' : 'ri <- rj + rk','MUL' : 'ri <- rj x rK','SUB' : 'ri <- rj - rK',
        'DIV' : 'ri <- rj / rK','ADDI': 'ri <- rj + c','SUBI': 'ri <- rj - c',
        'LOAD': 'ri <- M[rj + c]','STORE': 'M[rj + c] <- ri',
        'MOVEM': 'M[rj] <- M[ri]','Temp' : 'ri'
    }
    jouette_exp['ADDI:1'] = jouette_exp['ADDI:2'] = jouette_exp['ADDI:3'] = jouette_exp['ADDI']
    jouette_exp['LOAD:1'] = jouette_exp['LOAD:2'] = jouette_exp['LOAD:3'] = jouette_exp['LOAD:4'] = jouette_exp['LOAD']
    jouette_exp['STORE:1'] = jouette_exp['STORE:2'] = jouette_exp['STORE:3'] = jouette_exp['STORE:4'] = jouette_exp['STORE']
   
    jouette_peso = {
        'ADD':1,'MUL':1,'SUB':1,'DIV':1,'ADDI':1,'SUBI':2,'LOAD':3,
        'STORE':4,'MOVEM':3,'Temp':0
    }
    jouette_peso['ADDI:1'] = jouette_peso['ADDI:2'] = jouette_peso['ADDI:3'] = jouette_peso['ADDI']
    jouette_peso['LOAD:1'] = jouette_peso['LOAD:2'] = jouette_peso['LOAD:3'] = jouette_peso['LOAD:4'] = jouette_peso['LOAD']
    jouette_peso['STORE:1'] = jouette_peso['STORE:2'] = jouette_peso['STORE:3'] = jouette_peso['STORE:4'] = jouette_peso['STORE']   

    def tratar(self,st1):
        st = st1[:]
        result = []
        inicio = 0
        for i in range(0,len(st)):
            if st[i] != '':
                break
            if st[i] == '':
                inicio += 1
                st[i] = '#'
        for i in range(0,len(st)):
            if st[len(st) - i - 1] != '':
                break
            if st[len(st) - i - 1] == '':
                st[len(st) - i - 1] = '#'
        for i in range(0,len(st)):
            if st[i] != '#':
                result.append(st[i])
        return result,inicio

    def build(self,st):
        aux = st.split(' ')
        aux, ind1 = self.tratar(aux[:])
        t = len(aux[0])+len(aux[1]) + 2 + ind1
        aux = aux[2:len(aux)-1]
        aux = ' '.join(aux)

        r = []
        for i in range(0,len(aux)):
            if aux[i] == ',' and len(r) == 0:
                return i+t
            if aux[i] == '(':
                r.append('(')
            elif aux[i] == ')':
                if len(r) != 0 :r.pop() 
                else: return -1
        return -1

    def build_tree(self,st):
        if len(st)==0:
            return None
        aux = st.split(" ") #so pra pegar a instrucao
        aux, ind1 = self.tratar(aux[:]) #retirar espacos vazios do inicio e final da lista
        if len(aux) == 1:
            root = Node(aux[0],None,None)
            return root

        point = self.build(' '.join(aux)) #retorna a posicao da virgula em st, retorna -1 se nao tiver virgula

        if (')' in st or '(' in st) and point != -1:
            right = self.build_tree(st[point+1+ind1:len(st)-1])
            left = self.build_tree(st[len(aux[0])+3:point-1+ind1])
            root = Node(aux[0],left,right)
            return root
        elif (')' in st or '(' in st) and point == -1:
            left = self.build_tree(st[len(aux[0])+3:len(st)-2])
            root = Node(aux[0],left,None)
            return root
        elif point != -1:
            lenght = len(aux[0])
            left = self.build_tree(st[lenght+3:point-2+ind1])
            right = self.build_tree(st[point+1+ind1:len(st)-1])
            root = Node(aux[0],left,right)
            return root
        else:
            root = Node(aux[0],None,None)
            return root

    def guloso(self,no):
        if no == None:
            return
        if 'Temp:' in no.instrucao:
            print('Temp ',self.jouette_exp['Temp'])
            return
        if 'CONST:' in no.instrucao:        
            print('ADDI 1',self.jouette_exp['ADDI'], ' (CONST)')
            return
        if no.instrucao == 'MOVE':
            if no.left and no.left.instrucao == 'MEM':
                if no.left.left and no.left.left.instrucao == '+' :
                    if 'CONST:' in no.left.left.right.instrucao:
                        self.guloso(no.left.left.left)
                        self.guloso(no.right)
                        print('STORE 1 ',self.jouette_exp['STORE'])
                        return
                    if 'CONST:' in no.left.left.left.instrucao:
                        self.guloso(no.left.left.right)
                        self.guloso(no.right)
                        print('STORE 2 ',self.jouette_exp['STORE'])
                        return
                if no.right and no.right.instrucao == 'MEM':
                    self.guloso(no.left.left)
                    self.guloso(no.right.left)
                    print('MOVEM ',self.jouette_exp['MOVEM'])
                    return
                if no.left.left and 'CONST:' in no.left.left.instrucao:
                    self.guloso(no.right)
                    print('STORE 3 ',self.jouette_exp['STORE'])
                    return
                self.guloso(no.left.left)
                self.guloso(no.right)
                print('STORE 4 ',self.jouette_exp['STORE'])
            return
        if no.instrucao == 'MEM':
            if no.left and no.left.instrucao == '+':
                if 'CONST:' in no.left.left.instrucao:
                    self.guloso(no.left.right)
                    print('LOAD 2 ',self.jouette_exp['LOAD'])
                    return
                else:
                    self.guloso(no.left.left)
                    self.guloso(no.right)
                    print('LOAD 1 ',self.jouette_exp['LOAD'])
                    return
            if no.left and 'CONST:' in no.left.instrucao:
                print('LOAD 3 ',self.jouette_exp['LOAD'])
                return
            self.guloso(no.left)
            print('LOAD 4 ',self.jouette_exp['LOAD'])
            return
        if no.instrucao == "+":
            if no.left != None:
                if 'CONST:' in no.left.instrucao:
                    self.guloso(no.left.left)
                    self.guloso(no.left.right)
                    self.guloso(no.right)
                    print('ADDI 2',self.jouette_exp['ADDI'])
                    return
            if no.right!= None:
                if 'CONST:' in no.right.instrucao:
                    self.guloso(no.right.left)
                    self.guloso(no.right.right)
                    self.guloso(no.left)
                    print('ADDI 3',self.jouette_exp['ADDI'])  
                    return
        if no.instrucao == "-":
            if no.right != None and 'CONST:' in no.right.instrucao:
                self.guloso(no.right.left)
                self.guloso(no.right.right)
                self.guloso(no.left)
                print('SUBI ',self.jouette_exp['SUBI'])
                return
        if no.instrucao == "+":
            self.guloso(no.left)
            self.guloso(no.right)
            print('ADD ',self.jouette_exp['ADD'])
            return
        if no.instrucao == "*":
            self.guloso(no.left)
            self.guloso(no.right)
            print('MUL ',self.jouette_exp['MUL'])
            return
        if no.instrucao == "-":
            self.guloso(no.left)
            self.guloso(no.right)
            print('SUB ',self.jouette_exp['SUB'])
            return
        if no.instrucao == "/":
            self.guloso(no.left)
            self.guloso(no.right)
            print('DIV ',self.jouette_exp['DIV'])
            return

    def check(self,no):
        result = []
        if no == None:
            result.append('None')
            return result
        if 'Temp:' in no.instrucao:
            result.append('Temp')
            return result
        if 'CONST:' in no.instrucao:        
            result.append('CONST')
            return result
        if no.instrucao == 'MOVE':
            if no.left and no.left.instrucao == 'MEM':
                if no.left.left and no.left.left.instrucao == '+' :
                    if 'CONST:' in no.left.left.right.instrucao:
                        result.append('STORE:1')
                    if 'CONST:' in no.left.left.left.instrucao:
                        result.append('STORE:2')
                if no.right and no.right.instrucao == 'MEM':
                    result.append('MOVEM')
                if no.left.left and 'CONST:' in no.left.left.instrucao:
                    result.append('STORE:3')
                else:
                    result.append('STORE:4')
        if no.instrucao == 'MEM':
            if no.left and no.left.instrucao == '+':
                if 'CONST:' in no.left.left.instrucao:
                    result.append('LOAD:2')
                else:
                    result.append('LOAD:1')
            if no.left and 'CONST:' in no.left.instrucao:
                result.append('LOAD:3')
            else:
                result.append('LOAD:4')
        if no.instrucao == "+":
            if no.left != None:
                if 'CONST:' in no.left.instrucao:
                    result.append('ADDI:2')
            if no.right!= None:
                if 'CONST:' in no.right.instrucao:
                    result.append('ADDI:3')
        if no.instrucao == "-":
            if no.right != None and 'CONST:' in no.right.instrucao:
                result.append('SUBI')
        if no.instrucao == "+":
            result.append('ADD')
        if no.instrucao == "*":
            result.append('MUL')
        if no.instrucao == "-":
            result.append('SUB')
        if no.instrucao == "/":
            result.append('DIV')
        return result

    def escolha(self,lst):
        if lst == []: return -1
        result = dict()
        cost = 99999
        val = None
        for w in lst:
            result[w] = self.jouette_peso[w]

        for t in result:
            if cost >= result[t]:
                cost = result[t]
                val = t
        if val == None: return -1
        return Item(val,cost)

    def alg_dinamico(self,no):
        self.dinamico(no)
        result = []

        for w in self.din:
            if w != None:
                result.append(w.instrucao + ' -> ' + self.jouette_exp[w.instrucao])
        return '\n'.join(result)

    def dinamico(self,no):
        if 'Temp' in no.instrucao:
            x = Item('Temp',self.jouette_peso['Temp'])
            self.din.append(x)
            return x
        if 'CONST' in no.instrucao:
            return Item('CONST',self.jouette_peso['ADDI:1'])
        l = r = w = None
        if no.left:
            l = self.dinamico(no.left)
        if no.right:
            r = self.dinamico(no.right)
        w = self.escolha(self.check(no))
        if w == -1: w = None
        if l and r and w:
            if (l.custo + r.custo) < w.custo:
                self.din += l + r
            else:
                self.din.append(w)
        elif l and r:
            self.din += l + r
        elif l and not w:
            self.din.append(l)
        elif r and not w:
            self.din.append(r)
        else:
            self.din.append(w)
        return

class Item():
    def __init__(self,instrucao=None,custo=0):
        self.instrucao = instrucao
        self.custo = custo