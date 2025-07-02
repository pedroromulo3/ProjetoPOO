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
    
    def __str__(self):
        return f"{self.titulo} ({self.ano}) - {self.autor} | Categoria: {self.categoria} | Qtd: {self.quantidade}"
    
class Usuario(BaseEntity):
    def __init__(self, nome, email):
        super().__init__()
        self.nome = nome
        self.email = email
    
    def __lt__(self, other):
        return self.nome.lower() < other.nome.lower()
    
    def __str__(self):
        return self.nome
    
class Emprestimo(BaseEntity):
    def __init__(self, obra, usuario, data_retirada, data_prev_devol):
        super().__init__()
        self.obra = obra
        self.usuario = usuario
        self.data_retirada = data_retirada
        self.data_prev_devol = data_prev_devol
        self.data_devolucao_real = None

    def marcar_devolucao(self, data_dev_real):
        self.data_devolucao_real = data_dev_real
    
    def dias_atraso(self):
        if self.data_devolucao_real == None:
            print("Livro ainda não foi devolvido.")
        else:
            atraso =(self.data_devolucao_real - self.data_prev_devol).days
            return atraso

    def __str__(self):
            return f"Obra: {self.obra.titulo} | Retirada: {self.data_retirada.strftime('%d/%m/%Y')} | Prevista: {self.data_prev_devol.strftime('%d/%m/%Y')}"

