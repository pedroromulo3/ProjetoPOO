from core import Acervo
from models import Obra, Usuario
from datetime import date, timedelta

acervo = Acervo()
livro = Obra("POO Essencial", "Ana Silva", 2025, "Livro", 2)
joao  = Usuario("João", "joao@example.com")

acervo += livro                # adiciona exemplar
emp = acervo.emprestar(livro, joao)  # empresta

# simula atraso de 3 dias
after3 = date.today() + timedelta(days=3)
print("Multa:", acervo.valor_multa(emp, after3))

print(acervo.relatorio_inventario())
