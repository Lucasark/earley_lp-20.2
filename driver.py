from sys import argv, exit
from earley import parse, printDerivation, parseGrm

def initDriver(arquivo, palavra):
    stringArray = ""
    
    file1 = open(arquivo, 'r')
    Lines = file1.readlines()
    
    for line in Lines:
        stringArray += str(line)

    printDerivation(parse(parseGrm(stringArray), palavra))
    return

if  __name__ == "__main__":
    # Tratar existência dos parâmtros de entrada...
    
    #MOCK
    # arquivo = "grm/plus.grm"
    # palavra = "a+a+a"
    
    try:
        arquivo = argv[1]
    except:
        print("Entrada de arquivo invalida")
        #Finish DEBUG
        exit()
        
    try:
        palavra = argv[2]
    except:
        print("Entrada de palavra invalida")
        #Finish DEGUB
        exit()
    
    if(arquivo != None and palavra != None):
        initDriver(arquivo, palavra)