from core import Acervo
from models import Obra, Usuario
from datetime import datetime, timedelta
from rich.console import Console

# Cria uma instância do console do Rich para exibir tabelas formatadas
console = Console()

# Instancia o acervo da biblioteca
acervo = Acervo()

# Cria uma obra e dois usuários
livro = Obra("POO Essencial", "Ana Silva", 2025, "Livro", 2)
joao = Usuario("João", "joao@example.com")
maria = Usuario("Maria", "maria@example.com")

# Adiciona o livro duas vezes ao acervo (aumentando a quantidade disponível)
acervo += livro
acervo += livro

# Realiza empréstimos da obra para João e Maria
emp1 = acervo.emprestar(livro, joao)
emp2 = acervo.emprestar(livro, maria)

# Define uma devolução em atraso para Maria (5 dias após a data prevista)
data_prevista_maria = emp2.data_prev_devol
data_devolucao_maria = data_prevista_maria + timedelta(days=5)
acervo.devolver(emp2, data_devolucao_maria)

# Define uma data futura (10 dias à frente) para simular cálculo de multa
data_futura = datetime.now() + timedelta(days=10)

# Exibe as multas com base na data futura
print("\n--- MULTAS ---")
print(f"João (sem devolução): R$ {acervo.valor_multa(emp1, data_futura):.2f}")
print(f"Maria (com devolução em atraso): {emp2.dias_atraso()} dias de atraso")

# Exibe o relatório de inventário atual
console.print(acervo.relatorio_inventario())

# Exibe os débitos em aberto até a data futura
console.print(acervo._relatorio_builder("Débitos em Aberto").construir_debitos([emp1, emp2], data_futura))

# Exibe o histórico de empréstimos de João e Maria
console.print(acervo.historico_usuario([emp1, emp2], joao))
console.print(acervo.historico_usuario([emp1, emp2], maria))
