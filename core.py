from models import *
from datetime import datetime, timedelta
class Acervo:
    def __init__(self):
        self.obras = {}

    def __iadd__(self, obra: Obra):
        self.adicionar(obra)
        return self
    
    def __isub__(self, obra: Obra):
        self.remover(obra)
        return self
    
    def adicionar(self, obra):
        if obra in self.obras:
            self.obras[obra] += 1
        else:
            self.obras[obra] = 1

    def remover(self, obra):
        if obra in self.obras:
            if self.obras[obra] > 1:
                self.obras[obra] -= 1
            else:
                del self.obras[obra]

    def emprestar(self, obra, usuario, dias: int = 7):
        if obra not in self.obras or self.obras[obra] == 0:
            raise ValueError("Obra indisponível no acervo.")
        self.obras[obra] -= 1
        data_retirada = datetime.now()
        data_prev_devol = data_retirada + timedelta(days = dias)
        return Emprestimo(obra, usuario, data_retirada, data_prev_devol)
    
    def devolver(self, emprestimo, data_dev: datetime):
        emprestimo.marcar_devolucao(data_dev)
        if emprestimo.obra in self.obras:
            self.obras[emprestimo.obra] += 1
        else:
            self.obras[emprestimo.obra] = 1
    
    def renovar(self, emprestimo, dias_extras):
        nova_data = emprestimo.data_prev_devol + timedelta(days=dias_extras)
        if nova_data < emprestimo.data_prev_devol:
            raise ValueError("A data nova não pode ser anterior a data atual.")
        
        emprestimo.data_prev_devol = nova_data
    
    def valor_multa(self, emprestimo, data_ref):
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    #valor_multa