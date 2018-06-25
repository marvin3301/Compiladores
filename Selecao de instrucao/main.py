from selection import selection
import time

st2 = "MOVE ( MEM ( + ( + ( CONST:1000 , MEM ( TEMP:x ) ) , TEMP:fp ) ) , CONST:0 )"
exe = "MOVE ( MEM ( + ( MEM ( + ( Temp:fp , CONST:a ) ) , * ( Temp:i , CONST:4 ) ) ) , MEM ( + ( Temp:fp , CONST:x ) ) ) "
ex1 = "MEM ( + ( Temp:fp , CONST:X ) , * ( Temp:i , CONST:4 ) )"
ex2 = " * ( Temp:i , CONST:4 ) "
st1 = "MEM ( + ( CONST:1 , CONST:2 ) )"
st2 = "MOVE ( MEM ( + ( + ( CONST:1000 , MEM ( TEMP:x ) ) , TEMP:fp ) ) , CONST:0 )"
st3 = "MEM ( CONST:1000 , + ( CONST:1 , Temp:fp ) )"
st4 = "+ ( CONST:1 , CONST:2 )"
st5 = "MOVE ( MEM ( * ( Temp:i , CONST:fp ) ) , MEM ( * ( Temp:i , CONST:fp ) ) )"
st4 = "MOVE ( MEM ( + ( CONST:13 , CONST:15 ) ) , CONST:1000 )"

select = selection()
root = select.build_tree(st4)
print('\t\tGULOSO')
inicio = time.time()
select.guloso(root)
final = time.time() - inicio
print('\nGuloso executou em ',final)
print('\n\t\tDINAMICO')
inicio = time.time()
print(select.alg_dinamico(root))
final1 = time.time() - inicio
print('\nDinamico executou em ',final1)
#print(root)