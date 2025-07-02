from models import *
class Acervo:
    def __init__(self):
        self.obras = {}

    def __iadd__(self, obra: Obra):
        self.remover(obra)
        return self
    
    def __isub__(self, obra: Obra):
        self.remover(obra)
        return self