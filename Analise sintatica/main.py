from gramatica import (Gramatica,LR1_Closure,LR1_parser)

st = "S' -> S\nS -> C C\nC -> c C\nC -> c d\nD -> ε\nT -> D"

st1 = "S -> S ; S $\nS -> id := E\nS -> print ( L )\nE -> id\nE -> num\nE -> E + E\nE -> ( S , E )\nL -> E\nL -> L , E"

st2 = "Z -> X Y Z\nZ -> d\nY -> ε\nY -> c\nX -> Y\nX -> a"

st3 = "S -> E $\nE -> T E'\nE' -> + T E'\nE' -> - T E'\nE' -> ε\nT -> F T'\nT' -> / F T'\nT' -> * F T'\nT' -> ε\nF -> id\nF -> num\nF -> ( E )"

st4 = "A -> B a\nA -> ε\nB -> b\nB -> E b\nE -> ε"

st5 = "A -> B E\nB -> ε\nE -> c"

st6 = "S -> X Y Z\nX -> a X b\nX -> ε\nY -> c Y Z c X\nY -> d\nZ -> e Z Y e\nZ -> f"

st7 = "A -> B A a\nA -> ε\nB -> b B c\nB -> A A"

st8 = "X -> a X Y b X d Y\nY -> j Y\nY -> ε\nZ -> X Y Z"

st9 = "S' -> S $\nS -> V = E\nS -> E\nE -> V\nV -> x\nV -> * E"

st10 = "A -> B E\nB -> ε\nB -> b\nB -> E b\nE -> ε"

st11 = "S' -> S $\nS -> S ; A\nS -> A\nA -> E\nA -> id := E\nE -> E + id\nE -> id"

st12 = "S' -> S $\nS -> C C\nC -> c C\nC -> d"

g = Gramatica(st11)

#g.printf()

l = LR1_Closure(g)

'''
for e in l.states:
    print('\nstate: ' + str(e) + '\nitems: ' )
    for w in l.states[e].items:
        print(str(w))
    for w in l.states[e].gotos:
        print('lendo: ' + str(w) + ' vai para = ' + str(l.states[e].gotos[w]))
    for w in l.states[e].reduce:
        print('reduce: ' + str(w) + ' pela regra ' + str(l.states[e].reduce[w]))
'''

p = LR1_parser(l)

p.read_parser("id := num ; id := id + ( id := num + num + id ) $")

'''
for w in p.parser:
    for t in p.parser[w]:
        print('parser[' + str(w) + ']['+str(t)+'] = ' + str(p.parser[w][t]))
'''

#print('\na linguagem é ambigua? ',g.ambigua)
