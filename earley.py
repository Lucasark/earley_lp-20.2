# https://anytree.readthedocs.io/en/latest/index.html
from anytree.importer import DictImporter
from anytree import RenderTree
import rule as r
import sym as s
import copy
from sym import NT, T
import grammar as g

importer = DictImporter()

parser = {}

enums = {
  "DISTINCT": 1,
  "SIMILAR": 2,
  "IDENTICAL": 3,
  "PRODUCEONE": 4,
  "PRODUCETWO": 5,
  "PRODUCEALL": 6
}

parser["PRODUCEONE"] = enums["PRODUCEONE"]
parser["PRODUCETWO"] = enums["PRODUCETWO"]
parser["PRODUCEALL"] = enums["PRODUCEALL"]
parser["PRODUCECOUNT"] = enums["PRODUCETWO"]

def removeEps(grm):
    newG = copy.deepcopy(grm)
        
    for i in grm:
        if(['epsilon'] in grm[i]):
            for j in grm:
                for prod in grm[j]:
                    if(i in prod):
                        nSym = 0
                        for symb in prod:
                            if(i == symb):
                                nSym += 1
                        
                        loop = nSym*2
                        zeroLeft = len(str(bin(nSym))[2:])
                        for k in range(loop):
                            binSym = str(bin(k))[2:]
                            if(len(binSym) != zeroLeft):
                                binSym = "0"*(zeroLeft - len(binSym)) + binSym
                            aux = prod.copy()
                            rec = 0
                            for det in range(len(binSym)):
                                if(binSym[det] == "1"):
                                    idx = 0
                                    nidx = 0
                                    for occ in prod:
                                        if(occ == i):
                                            if(rec == nidx):
                                                aux[idx] = ""
                                            nidx += 1
                                        idx += 1
                                rec += 1
                            l = list(filter(lambda x: x != "", aux))     
                            if(l not in newG[j] and l != []):
                                newG[j].append(l)
                            

            newG[i].remove(['epsilon'])
            grm = copy.deepcopy(newG)

    return newG

def arraysEqual(a, b):
  if(a == b):
    return True

  if(a == None or b == None):
    return False

  if(len(a) != len(b)):
    return False

  for i in range(len(a)):
    if(a[i] != b[i]):
        return False
    
  return True


class State():
    
    def __init__(self, rule, index, predecessor, backPointers=None):
        self.rule = rule
        self.index = index
        self.predecessor = predecessor
        if(backPointers):
            self.backPointers = backPointers
        else:
            self.backPointers = []
            
    def done(self):
        return (self.index == len(self.rule.production))
    
    def compare(self, other):
        if(self.rule == other.rule and self.index == other.index and self.predecessor == other.predecessor):
            if(arraysEqual(self.backPointers, other.backPointers)):
                return enums["IDENTICAL"]
            else:
                return enums["SIMILAR"]
        else:
            return enums["DISTINCT"]
    
    def next(self):
        return self.rule.production[self.index]
    
    def toString(self):
        return ('(' + str(self.rule.name) + ' -> ' + ('').join([str(y) for y in self.rule.production[0:self.index]])
                + '*' + ('').join([str(x) for x in self.rule.production[self.index:]]) + ', ' + str(self.predecessor)
                + ')')


def findNones(state, count):
    if(state.backPointers == []):
        return count
    else:
        for back in state.backPointers:
            # print(back)
            if back == None:
                count = count+1
            else:
                count = findNones(back, count)
    return count

def parseAux(grammar, str, produceCount=None):
    # print(grammar, str)
    
    oldProduceCount = parser["PRODUCECOUNT"]
    if(produceCount):
        parser["PRODUCECOUNT"] = produceCount
    
    chart = []
    for lop in range(len(str)+1): 
        chart.append([])
        
    def seen(state, strPos):
        count = 0
        # print("L:", len(chart[strPos]))
        for i in range(len(chart[strPos])):
            equalness = state.compare(chart[strPos][i])
            if(equalness == enums["IDENTICAL"] or (equalness == enums["SIMILAR"] and parser["PRODUCECOUNT"] == enums["PRODUCEONE"])):
                return True
            if(equalness == enums["SIMILAR"] and parser["PRODUCECOUNT"] == enums["PRODUCETWO"]):
                count += 1
                if count > 1:
                    return True

        return False
    
    def scanner(state, strPos):
        if(strPos < len(str)):
            if(state.next() == (T(str[strPos]))):
                newBPs = state.backPointers.copy()
                newBPs.append(None)
                advanced = State(state.rule, state.index+1, state.predecessor, newBPs)
                if(not(seen(advanced, strPos+1))):
                    chart[strPos+1].append(advanced)
    
    def completer(state, strPos):
        thisSym = NT(state.rule.name)
        for i in range(len(chart[state.predecessor])):
            prevState = chart[state.predecessor][i]
            if(not(prevState.done()) and thisSym == (prevState.next())):
                newBPs = prevState.backPointers.copy()
                newBPs.append(state)
                advanced = State(prevState.rule, prevState.index+1, prevState.predecessor, newBPs)
                if(not(seen(advanced, strPos))):
                    chart[strPos].append(advanced)
    
    def predictor(state, strPos):
        sym = state.next()
        for i in range(len(grammar.symbolMap[sym.data]["rules"])):
            advanced = State(grammar.symbolMap[sym.data]["rules"][i], 0, strPos)
            if(not seen(advanced, strPos)):
                chart[strPos].append(advanced)
        
        for i in range(len(chart[strPos])):
          candidate = chart[strPos][i]
          if(candidate.rule.name == sym.data and candidate.predecessor == strPos and candidate.done()):
              #slice(0)?
            newBPs = state.backPointers.copy()
            newBPs.append(candidate)
            advanced = State(state.rule, state.index+1, state.predecessor, newBPs)
            if(not seen(advanced, strPos)):
              chart[strPos].append(advanced)
    
    startSym = grammar.start
    gammaRule = r.Rule(['GAMMA'], [NT(startSym)])
    chart[0].append(State(gammaRule, 0, 0))
    
    for i in range(len(str)+1):
        j = 0
        # for j in (chart[i]):
        while(j < len(chart[i])):
            state = chart[i][j]
            # print( "I: ",i,"J:", j, "|  ",state.toString())
            if(not(state.done())):
                if(state.next().type == 'NT'):
                        # print("p")
                        predictor(state, i)
                else:
                    # print("s")
                    scanner(state, i)
            else:
                # print("c")
                completer(state, i)
            j += 1
    
    parses = []
    valid = False
    for i in range(len(chart[len(str)])):
        state = chart[len(str)][i]
        if(state.rule == gammaRule and state.done()):
            parses.append(state)
            valid = True
    
    if not valid:
        #Mal formada ? Meio sem sentido mas ok...
        possible = {"index": -1, "number": -1}
        for x in range(len(chart[len(chart)-1])):
            # print(chart[len(chart)-1][x])
            noneRep = 0
            noneRep = findNones(chart[len(chart)-1][x], noneRep) 
            # print(noneRep)
            if(noneRep > possible["number"]):
                possible["index"] = x
                possible["number"] = noneRep
            
            
        # print("Mal Formada Melhorzinha", chart[len(chart)-1][possible["index"]])
        parses.append(chart[len(chart)-1][possible["index"]])
    
    parser["PRODUCECOUNT"] = oldProduceCount
    #return possiveis parses...
    return {"parses": parses, "valid": valid}

def parseGrm(g):
    
    grammar = {}
    grammarArray = g.split('\n')
    for i in grammarArray:
        # print(i)
        prod = i.split()
        if not(prod[0] in grammar):
            grammar[prod[0]] = []
        
        for j in range(2, len(prod)):
            if not(prod[j] == "|" or prod[j] == "->"):
                prodAux = prod[j].split(".")
                grammar[prod[0]].append(prodAux)
            
    #Removendo [eps]
    newGrammar = removeEps(grammar)
    return newGrammar

def transToClassGrammar(grammar):
    allNT = []
    for gNT in grammar:
        allNT.append(gNT)
        
    newClassGrammar = []
    for nt in grammar:
        for sb in grammar[nt]:
            symArray = []
            for symb in sb: 
                if(symb in allNT):
                    symArray.append(s.NT(symb))
                else:
                    symArray.append(s.T(symb))
            rule = r.Rule(nt, symArray)
            newClassGrammar.append(rule)
             
    return g.Grammar(newClassGrammar)

def treeParseRule():
    return

def derivationTree(parse):
    # print(parse.rule)
    out = {"root" : parse.rule.name,
            "children" : []}
    
    for j in range(parse.index):
        if(parse.rule.production[j].type == 'T'):
            out["children"].append({"root": parse.rule.production[j].data})
        else:
            out["children"].append(derivationTree(parse.backPointers[j]))
            
    return out


def parse(g, w):
    # test = transToClassGrammar(g)
    a = parseAux(transToClassGrammar(g), w)
    
    dev = []
    if(a["valid"]):
        #Bem formada ou ambiguo
        maxAmb = 0
        for i in a["parses"]:
            dev.append(derivationTree(i.backPointers[0]))
            maxAmb += 1
            if maxAmb == 2:
                break
    else:
        #Mal formada
        print("<-------Mal formada------>")
        dev.append(derivationTree(a["parses"][0]))
        
    return dev

def printDerivation(d):
    for p in d:
        root = importer.import_(p)
        print(RenderTree(root))