class Grammar():
    
    def __init__(self, rules, start=None):
        self.rules = rules
        
        if(start):
            self.start = start
        else:
            self.start = rules[0].name
            
        self.symbolMap = {}
        
        if(start):
            self.symbolsList = [start]
        else:
            self.symbolsList = []
        
        if(start):
            self.symbolMap[start] = {rules: []}
        
        for i in range(len(self.rules)):
            sym = self.rules[i].name
            if(not(sym in self.symbolMap)):
                self.symbolMap[sym] = {"rules": []}
                self.symbolsList.append(sym)
            
            for j in range(len(self.rules[i].production)):
                rhsSym = self.rules[i].production[j]
                if(rhsSym.type == 'NT' and not(rhsSym.data in self.symbolMap)):
                    self.symbolMap[rhsSym.data] = {"rules": []}
                    self.symbolsList.append(rhsSym.data)
                    
            self.symbolMap[sym]["rules"].append(self.rules[i])
            
    def __repr__(self):
        pass
    
    def __str__(self):
        out = 'Grammar([\n  '
        for i in range(len(self.rules)):
            if(i>0):
                out += ',\n  '
            out += repr(self.rules[i])
        out += '\n], \'' + self.start + '\')'
        return out