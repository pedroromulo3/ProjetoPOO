from core import Acervo
from models import Obra, Usuario
from datetime import datetime, timedelta
from rich.console import Console

console = Console()

# Setup inicial
acervo = Acervo()
livro = Obra("POO Essencial", "Ana Silva", 2025, "Livro", 2)
joao = Usuario("João", "joao@example.com")
maria = Usuario("Maria", "maria@example.com")

# Adiciona ao acervo
acervo += livro
acervo += livro

# Empréstimos
emp1 = acervo.emprestar(livro, joao)   # João NÃO devolveu (em atraso)
emp2 = acervo.emprestar(livro, maria)  # Maria devolveu com atraso

# Devolve o da Maria com atraso de 5 dias
data_prevista_maria = emp2.data_prev_devol
data_devolucao_maria = data_prevista_maria + timedelta(days=5)
acervo.devolver(emp2, data_devolucao_maria)

# Simula data atual bem no futuro (para gerar multa em João)
data_futura = datetime.now() + timedelta(days=10)

# Simulações
print("\n--- MULTAS ---")
print(f"João (sem devolução): R$ {acervo.valor_multa(emp1, data_futura):.2f}")
print(f"Maria (com devolução em atraso): {emp2.dias_atraso()} dias de atraso")

# Relatórios
console.print(acervo.relatorio_inventario())
console.print(acervo._relatorio_builder("Débitos em Aberto").construir_debitos([emp1, emp2], data_futura))
console.print(acervo.historico_usuario([emp1, emp2], joao))
console.print(acervo.historico_usuario([emp1, emp2], maria))
