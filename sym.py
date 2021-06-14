class Sym():
    
    def __init__(self, type, data):
        self.type = type
        self.data = data
    
    def __eq__(self, other):
        return self.data == other.data and self.type == other.type
    
    def __str__(self):
        return str(self.data)
    
def NT(data):
    return Sym('NT', data)

def T(data):
    return Sym('T', data)
    
    