import uuid
from datetime import datetime

class BaseEntity:
    def __init__(self):
        self.id = self._gerar_id()
        self.data_criaçao = datetime.now()

    def __eq__ (self, other):
        return isinstance(other,self.__class__) and self.id == other.id
    
    def _gerar_id (self):
        return uuid.uuid4()
    
class Obra(BaseEntity):
    def __init__ (self, titulo, autor, ano, categoria, quantidade=1):
        super().__init__()
        self.titulo = titulo 
        self.autor = autor 
        self.ano = ano 
        self.categoria = categoria
        self.quantidade = quantidade

    def disponivel (self, estoque):
        return self.quantidade > 0 