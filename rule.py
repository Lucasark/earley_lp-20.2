class Rule():
    
    def __init__(self, name, production):
        self.name = name
        self.production = production
        
    def __repr__(self):
        out = 'Rule(\'' + self.name + '\', ['
        for i in range(len(self.production)):
            if(i>0):
                out += ', '
            out += self.production[i].type + '(\'' + self.production[i].data + '\')'
        
        out += '])'
        return out