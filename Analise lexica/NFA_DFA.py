import re

TOKENS = [('q3','IF'),('q5','ID'),('q7', 'NUM'), ('q12', 'ELSE'),('q16','END'),('q23','REPEAT'),('q39','READ'),
         ('q29', 'UNTIL'),('q34','THEN'),('q45','WRITE'),('q49',' PONTOVIRGULA'),('q51', 'MENORQUE'),('q53','MAIORQUE'),
         ('q55','PLUS'),('q57','STAR'),('q59','MINUS'),('q61','SLASH'),('q63','ATTRIB'),( 'q66','EQUALS'),('q68','LPARENT'),('q70','RPARENT')]

TRANSITIONS = [('q0','$','q1'),('q0','$','q4'),('q0','$','q6'), ('q0','$','q8'), ('q0','$','q13'),
		('q0','$','q17'), ('q0','$','q35'), ('q0','$','q24'), ('q0','$','q30'), ('q0','$','q40'), 
        ('q0','$','q48'), ('q0','$','q50'), ('q0','$','q52'), ('q0','$','q54'), ('q0','$','q56'),
        ('q0','$','q58'),    ('q0','$','q60'), ('q0','$','q62'),
        ('q1','i','q2'), ('q2','f','q3'),
        ('q2','abcdeighjklmnopqrstuwvxyz','q4'),('q1','abcdfghjklmnopqswvxyz','q4'),('q3','abcdefghijklmnopqrstuwvxyz','q4'),
        ('q4','abcdfghjklmnopqsvxyz','q5'), ('q5','abcdefghijklmnopqrstuwvxyz','q5'), ('q6','0123456789','q7'),
        ('q7','0123456789','q7'), ('q8','e','q9'), ('q9','abcdefghijkmopqrstuwvxyz','q5'), ('q9','l','q10'), ('q10','abcdefghijklmnopqrtuwvxyz','q5'),
        ('q10','s','q11'), ('q11','e','q12'),('q12','abcdefghijklmnopqrstuwvxyz','q5'),
        ('q13','e','q14'),('q14','abcdefghijkmopqrstuwvxyz','q5'), ('q14','n','q15'), ('q15','abcefghijklmnopqrstuwvxyz','q5'),('q15','d','q16'),
        ('q16','abcdefghijklmnopqrstuwvxyz','q5'),('q17','r','q18'), ('q18','e','q19'), ('q19','p','q20'), ('q20','e','q21'), ('q21','a','q22'), ('q22','t','q23'),
        ('q35','r','q36'),('q36','abcdfghijklmnopqrstuwvxyz','q5'),('q36','e','q37'),('q37','bcdefghijklmnoqrstuwvxyz','q5'),
        ('q37','a','q38'),('q38','abcefghijklmnopqrstuwvxyz','q5'), ('q38','d','q39'),('q39','abcdefghijklmnopqrstuwvxyz','q5'),
        ('q24','u','q25'), ('q25','abcdefghijklmopqrstuwvxyz','q5'),('q25','n','q26'), ('q26','abcdefghijklmnopqrsuwvxyz','q5'),
        ('q26','t','q27'),('q27','abcdefghjklmnopqrstuwvxyz','q5'), ('q27','i','q28'), ('q28','abcdefghijkmnopqrstuwvxyz','q5'), ('q28','l','q29'),('q29','abcdefghijklmnopqrstuwvxyz','q5'),
        ('q30','t','q31'),('q31','abcdefgijklmnopqrstuwvxyz','q5'), ('q31','h','q32'),('q32','abcdfghijklmnopqrstuwvxyz','q5'), ('q32','e','q33'),('q33','abcdefghijklmopqrstuwvxyz','q5'),
        ('q33','n','q34'),('q34','abcdefghijklmnopqrstuwvxyz','q5'),
        ('q40','w','q41'),('q41','abcdefghijklmnopqstuwvxyz','q5'),('q41','r','q42'),('q42','abcdefghjklmnopqrstuwvxyz','q5'),
        ('q42','i','q43'),('q43','abcdefghijklmnopqrsuwvxyz','q5'), ('q43','t','q44'), ('q44','abcdfghijklmnopqrstuwvxyz','q5'),('q44','e','q45'),('q45','abcdefghijklmnopqrstuwvxyz','q5'),
        ('q48',';','q49'), 
        ('q50','<','q51'),
        ('q52','>','q53'),
        ('q54','+','q55'),
        ('q56','*','q57'),
        ('q58','-','q59'),
        ('q60','/','q61'),
        ('q62','=','q63'),
        ('q64',':','q65'),('q65','=','q66'),
        ('q67','(','q68'),
        ('q69',')','q70')]


SIGMA = ['$', 'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
        '0','1','2','3','4','5','6','7','8','9','<','>','-',';',':','=','+','/','*','(',')',' ']

EMPTY = '$'

def edge(s, c):
    conj = set()
    for t in TRANSITIONS:
        if s == t[0] and t[1].find(c) != -1:
           conj.add(t[2])
    return conj

def closure(s):
    clo = set()
    for t in TRANSITIONS:
    	if t[0] == s:
    	    clo = clo.union(edge(s,EMPTY))
    	    for x in clo:
    	    	clo = clo.union(closure(x))

    if clo == set():
       return [s]
    return clo

def DFAed(d, c):
        l = closure(d)
        lst = set()
        for j in l:
                p =  edge(j,c)
                if p != set():
                        lst = lst.union(p)
                                        
        return lst



DFAstates = []
DFAtransitions = dict()

def get(c):
        if c == set():
                return False
        for a in DFAstates:
                if a == c:
                        return True

        return False            


def NFA_DFA():
        DFAstates.append(set())
        DFAstates.append(closure('q0'))
        p = 1
        j = 0
        z = -1
        while j <= p:
                for c in SIGMA:
                        s = set()
                        for cj in DFAstates[j]:
                                e = DFAed(cj, c)
                                if len(e) != 0:
                                        s = s.union(e)
                        if len(s)==0:
                                continue
                        z+=1
                        if get(s):
                                DFAtransitions[z] = (DFAstates[j], c, s)
                        else:
                                p+=1
                                DFAstates.append(s)
                                DFAtransitions[z] = (DFAstates[j], c, s) 
                j+=1

def edgeTransitions(s, c):
    conj = set()
    for x in range(len(DFAtransitions)):
        if s == DFAtransitions[x][0] and DFAtransitions[x][1].find(c) != -1:
                 return DFAtransitions[x]

    return None


#NFA_DFA()
     
def ler_arquivo():
    file = open("in.txt", 'r+')
    dirtyCode = file.read()
    dirtyCode = descomenta(dirtyCode)
    cleanCode = ''
    for ch in dirtyCode:
        if(ch in SIGMA):
        	if(ch==';'): cleanCode+=' '
        	cleanCode += ch
    return cleanCode

def esc_arq(str):
    file = open("out.txt", 'w')
    file.write(str)

def descomenta(text):
    text = re.sub(r'{.*}', '', text)
    return text     

def isfinal(s):
    for state in TOKENS:
        for z in s:
            if z == state[0]:
                return state
    return None

def input(s):
    palavra = ''
    tokenized = ''
    state = DFAstates[1]
    for i in range(len(s)):
        e = edgeTransitions(state,s[i])
        if(e!=None):
            #print e
            state = e[2]
            palavra += s[i]
        else:
            final = isfinal(state)
            if final != None:
                #print final[1]
                tokenized += final[1] + ( ("(" + palavra + ")") if final[1] in ('ID', 'NUM') else '') + ', '
                palavra = ''
                state = DFAstates[1]
            else:
                if palavra != "":
                    print "palavra '" + palavra + "' nao pertence a linguagem"
                state = DFAstates[1]
    esc_arq(tokenized)

NFA_DFA()

input(ler_arquivo()) 


