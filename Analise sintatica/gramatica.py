
class Gramatica():
    alfabeto = set()
    nao_terminais = set()
    terminais = set()
    regras = []
    firsts = dict()
    follows = dict()
    nullable = dict()
    calculado = []
    calculando = set()
    texto_input = ''

    def __init__(self,text):
        self.texto_input = text
        self.ambigua = False
        self.init_regras()
        self.init_alfabeto_e_terminais()
        self.calc_first_follow_nullable()

    def get_regras_de_nao_terminal(self, nao_terminal):
        result = []
        for i in self.regras:
            if nao_terminal == i.nao_terminal:
                result.append(i)
        return result

    def get_regras_x_aparece(self, x):
        result = []
        for i in self.regras:
            if x in i.dev:
                result.append(i)
        return result

    def printf(self):
        for w in self.nao_terminais:
            print('first(' + w + ')' +' = ' + str(self.firsts[w]))
            print('follow(' + w + ')' + ' = ' + str(self.follows[w]))
            print('Nullable(' + w +')' + ' = '+ str(self.nullable[w]))
            print('---:---')

    def init_regras(self):
        lines = self.texto_input.split("\n")

        for line in lines:
            if line != "":
                rule = Rule(self, line)

                self.regras.append(rule)

                self.alfabeto = self.alfabeto.union([rule.nao_terminal])
                self.nao_terminais = self.nao_terminais.union([rule.nao_terminal])
    
    def init_alfabeto_e_terminais(self):
        for i in self.regras:
            for j in i.dev:
                if j != 'ε' and not j in self.nao_terminais:
                    self.alfabeto = self.alfabeto.union([j])
                    self.terminais = self.terminais.union([j])
    

    def all_nullable(self,st):
        for w in st:
            if w == 'ε':
                continue
            if not self.nullable[w]:
                return False
        return True

    def all_calculado(self):
        for w in self.nao_terminais:
            if not w in self.calculado:
                return False 
        return True

    def all_suspenso(self):
        for w in self.nao_terminais:
            if w in self.calculando:
                return False 
        return True

    def calc_first_follow_nullable(self):
        for x in self.alfabeto:
            self.nullable[x] = False
            self.firsts[x] = set()
            self.follows[x] = set()
        i = 0
        while i <= len(self.regras):
            for x in self.regras:
                k = len(x.dev)
                if self.all_nullable(x.dev) or k == 0 or x.dev[0] == 'ε':
                    self.nullable[x.nao_terminal] = True
            i+=1
    
        self.calculado = []
        self.calculando = set()
    
        while True:
            for x in self.nao_terminais:
                self.firsts[x] = self.calcula_first(x)
            if self.all_calculado() and self.all_suspenso():
                for x in self.nao_terminais:
                    self.firsts[x] = self.calcula_first(x)
                break
        
        self.calculado = []
        self.calculando = set()
        self.follows[self.regras[0].nao_terminal] = set(['$']) #cifrao na regra inicial

        for w in self.nao_terminais:
            self.follows[w] = self.follows[w].union(self.calc_follow(w))
            
    def calcula_first(self,c):
        m = self.get_regras_de_nao_terminal(c)
        result = set()

        for regra in m:
            for i in range(0,len(regra.dev)):
                if regra.dev[i] in self.terminais:
                    result = result.union([regra.dev[i]])
                    break
                elif regra.dev[i] in self.nao_terminais:
                    if regra.dev[i] in self.calculado and not regra.dev[i] in self.calculando:
                        result = result.union(self.firsts[regra.dev[i]])
                        if not self.nullable[regra.dev[i]]:
                            break
                    else:
                        if c == regra.dev[i]:
                            break
                        else:
                            if regra.dev[i] in self.calculando:
                                break
                            self.calculando = self.calculando.union([c])
                            self.firsts[regra.dev[i]] = self.calcula_first(regra.dev[i])
                            self.calculando.remove(c)
                            i = i - 1

        self.calculado.append(c)
        
        return result
  
    def calc_follow(self,c):
        
        m = self.get_regras_x_aparece(c)
        result = set()
        flag = False

        for x in m:
            for i in range(0,len(x.dev)): 
                if x.dev[i] in self.nao_terminais and x.dev[i] != c and flag and not x.dev[i] in self.calculando:
                    result = result.union(self.firsts[x.dev[i]])
                    if not self.nullable[x.dev[i]]:
                        flag = False
                    elif self.nullable[x.dev[i]] and i == len(x.dev) - 1:
                        if x.nao_terminal in self.calculado:
                            result = result.union(self.follows[x.nao_terminal])
                        else:
                
                            self.calculando = self.calculando.union([c])
                            self.follows[x.nao_terminal] = self.calc_follow(x.nao_terminal)
                            result = result.union(self.follows[x.nao_terminal])
                            self.calculando.remove(c)
                            self.calculado.append(x.nao_terminal)
                if x.dev[i] in self.terminais and flag:
                    result = result.union(x.dev[i])
                    flag = False

                if x.dev[i] == c and i == (len(x.dev) - 1) and not x.nao_terminal in self.calculando:
                    if x.nao_terminal == c:
                        break
                    if x.nao_terminal in self.calculado:
                        result = result.union(self.follows[x.nao_terminal])
                        break
                    else:
                        self.calculando = self.calculando.union([c])
                        self.follows[x.nao_terminal] = self.calc_follow(x.nao_terminal)
                        self.calculando.remove(c)
                        result = result.union(self.follows[x.nao_terminal])
                        self.calculado.append(x.nao_terminal)
                elif x.dev[i] == c and not i == len(x.dev)-1:
                    if x.dev[i+1] in self.terminais:
                        result = result.union([x.dev[i+1]])
                        if not c in x.dev[i+1:]:
                            break
                    if x.dev[i+1] in self.nao_terminais:
                        result = result.union(self.firsts[x.dev[i+1]])
                        if self.nullable[x.dev[i+1]]:
                            flag = True
                        else:
                            flag = False
        
        self.calculado.append(c)
        return result

    def get_sequencia_firsts(self, dev):
        result = set()
        for j in dev:
            if j in self.terminais:
                result = result.union([j])
                break
            for k in self.firsts[j]:
                result = result.union([k])
        return result
    
    def get_sequencia_follows(self, dev,look):
        result = set()
        if self.all_nullable(dev):
            result = result.union(list(look))
        for j in dev:
            if j in self.terminais:
                result = result.union([j])
                break
            for k in self.follows[j]:
                result = result.union([k])
            if not self.nullable[j]:
                break
            
        return result


class Rule():
    
    def __init__(self, gramatica, texto):
        self.gramatica = gramatica
        self.index = len(gramatica.regras)

        splt = texto.split(' -> ')

        self.nao_terminal = splt[0]
        self.dev = splt[1].split(' ')

    def __str__(self):
        return self.nao_terminal + " -> " + str(self.dev)

    def __eq__(self, other):
        if self.nao_terminal != other.nao_terminal:
            return False
        if len(self.dev) != len(other.dev):
            return False
        for dev in self.dev:
            if not dev in other.dev:
                return False
        return True

class State():
	
    def __init__(self, index, items):
        self.index = index
        self.items = items[:]
        self.gotos = dict()
        self.reduce = dict()
        self.finished = False
    
    def __eq__(self,other):
        if len(self.items) != len(other.items):
            return False
        for w in other.items:
            if not w in self.items:
                return False
        return True

class Item():

    def __init__(self, regra, dotindex):
        self.regra = regra
        self.dotindex = dotindex
        self.lookaheads = []
        self.used = False

    def __str__(self):
        return (self.regra.nao_terminal + ' -> ' + ('' if self.dotindex > len(self.regra.dev) else ' '.join(self.regra.dev[0:self.dotindex]) + '.' + 
                                                ' '.join(self.regra.dev[self.dotindex:])) + ' :: ' + ' '.join(self.lookaheads))
    def __eq__(self,other):
        return self.regra == other.regra and self.dotindex == other.dotindex and self.lookaheads == other.lookaheads

class LR1_Closure():

    def __init__(self,gramatica):
        self.gramatica = gramatica
        self.states = dict()
        self.build_automata()

    def build_closure(self,items):
        
        closure = items

        while True:
            old_closure = closure[:]

            for item in old_closure:
                if len(item.regra.dev) <= item.dotindex:
                    break
                for w in self.gramatica.get_regras_de_nao_terminal(item.regra.dev[item.dotindex]):
                    if len(item.regra.dev) >= item.dotindex + 1:
                        t = self.gramatica.get_sequencia_follows(item.regra.dev[item.dotindex+1:],item.lookaheads)
                    else:
                        t = self.gramatica.get_sequencia_follows([],item.lookaheads)
                    it = Item(w,0)
                    it.lookaheads += t

                    if it in closure:
                        continue
                    closure.append(it)
            
            if old_closure == closure:
                break

        return closure

    def get_indice(self,dicionario,elemento):
        for w in dicionario.keys():
            if elemento == dicionario[w]:
                return w
        return None
    
    def all_finished(self):
        for s in self.states:
            for i in self.states[s].items:
                if not i.used:
                    return False
        return True
    
    def check_state_and_add(self,state,index):
        for st in self.states.keys():
            if self.states[st] == state:
                    return st
        
        self.states[index] = state
        return -1
        
    def build_automata(self):
        item1 = Item(self.gramatica.regras[0],0)
        item1.lookaheads = ["$"]
        lista = self.build_closure([item1])
        state1 = State(0, lista)
        self.states[0] = state1
        index = 1

        while True:
            old_states = dict(self.states)

            for x in old_states.keys():
                for t in old_states[x].items:
                    if not t.used:
                        t.used = True
                        if t.dotindex + 1 > len(t.regra.dev):
                            continue
                        if t.regra.dev[t.dotindex] == '$':
                            self.states[x].gotos[t.regra.dev[t.dotindex]] = -1
                            continue
                        it = Item(t.regra,t.dotindex+1)
                        it.lookaheads = t.lookaheads[:]
                        keys_box = []
                        keys_box.append(it)
                        for w in old_states[x].items:
                            if w.dotindex >= len(w.regra.dev):
                                continue
                            if t.regra.dev[t.dotindex] == w.regra.dev[w.dotindex] and not w.used:
                                if w.dotindex + 1 > len(w.regra.dev):
                                    continue
                                it = Item(w.regra,w.dotindex+1)
                                it.lookaheads = w.lookaheads[:]
                                w.used = True
                                keys_box.append(it)
                        new_state = State(index,self.build_closure(keys_box))

                        check = self.check_state_and_add(new_state,index)
                        if check == -1:
                            #print('1 check = ' + str(index) + ' goto ' + str(t.regra.dev[t.dotindex]))                            
                            self.states[x].gotos[t.regra.dev[t.dotindex]] = index
                            index += 1
                        else:
                            #print('check = ' + str(check) + ' goto ' + str(t.regra.dev[t.dotindex]))
                            self.states[x].gotos[t.regra.dev[t.dotindex]] = check
                        
            if old_states == self.states:
                break
    
        for st in self.states.keys():
            for w in self.states[st].items:
                if len(w.regra.dev) == w.dotindex:
                    for t in w.lookaheads:
                        self.states[st].reduce[t] = self.gramatica.regras.index(w.regra) 

class LR1_parser():
    
    def __init__(self,lr1table):
        self.lr1table = lr1table
        self.gramatica = lr1table.gramatica
        self.parser = dict()
        self.build_parser()
        self.errors = 0
        self.tindex = -1
    
    def build_parser(self):
        for i in range(0,len(self.lr1table.states)):
            self.parser[i] = dict()
            for w in self.lr1table.gramatica.alfabeto:
                self.parser[i][w] = []
            if '$' not in self.lr1table.gramatica.alfabeto:
                for i in range(0,len(self.lr1table.states)):
                    self.parser[i]['$'] = []

        for st in self.lr1table.states:
            w = self.lr1table.states[st]
            for reduce in w.reduce.keys():
                self.parser[st][reduce] += ['R' + str(w.reduce[reduce])]

        for st in self.lr1table.states:
            w = self.lr1table.states[st]
            for goto in w.gotos.keys():
                if self.parser[st][goto] != []:
                    self.lr1table.gramatica.ambigua = True
                if w.gotos[goto] == -1:
                    self.parser[st][goto] += ['ACC']
                elif goto in self.lr1table.gramatica.terminais:
                    self.parser[st][goto] += ['S' + str(w.gotos[goto])]
                else:
                    self.parser[st][goto] += ['G' + str(w.gotos[goto])]


    def read_parser(self,text):
        self.tokens = text.split(' ')
        notfound = True
        tkn = self.nexttoken()
        tab = self.parser
        s = 0
        stk = ['invalid',0]
        ppk = []
        
        while notfound:
            if tkn == '':
                break
            if not tkn in self.gramatica.alfabeto:
                self.error()
                stk = ['invalid',0]
                ppk = []
                tkn = self.nexttoken()
            st = s
            s = int(stk.pop())
            ppk.append(s)

            if tab[s][tkn] != [] and tab[s][tkn][0] == 'ACC' and tkn == '$':
                notfound = False
            elif tab[s][tkn] != [] and tab[s][tkn][0][0] == 'S':
                stk.append(tkn)
                stk.append(tab[s][tkn][0][1:])
                tkn = self.nexttoken()
            elif tab[s][tkn] != [] and tab[s][tkn][0][0] == 'R':
                index = int(tab[s][tkn][0][1:])
                regra = self.gramatica.regras[index]
                rmcount = 0 if '$' in regra.dev else len(regra.dev) 
                while rmcount:
                    stk.pop()
                    ppk.pop()
                    rmcount -= 1
                st = ppk[len(ppk)-1]
                stk.append(regra.nao_terminal)
                stk.append(tab[st][regra.nao_terminal][0][1:])
            else:
                self.error()
                stk = ['invalid',0]
                ppk = []
                tkn = self.nexttoken()
        if self.errors == 0:
            print('Success !!!')
        else:
            print('Fail !!!')

    def nexttoken(self):
        self.tindex += 1
        return self.token()

    def error(self):
        self.errors += 1
        print ("Erro de sintaxe no token", self.token())
    
    def token(self):
        return self.tokens[self.tindex] if len(self.tokens) > self.tindex else ''
