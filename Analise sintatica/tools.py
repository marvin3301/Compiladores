
def getOrCreateArray(dictionary, key):
    if not key in dictionary:
        result = []
        dictionary[key] = result
    else:
        result = dictionary[key]
    return result

def isElement(element, array):
	for i in array:
		if (element == i):
			return True
	return False

def addUniqueList(lista1,lista2):
	for w in lista2:
		addUnique(w,lista1)

def addUnique(element, array):
	if not element in array:
		array.append(element)
