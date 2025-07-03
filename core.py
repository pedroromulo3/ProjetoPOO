from models import *
from datetime import datetime, timedelta
from rich.table import Table
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
        data_devol_prevista = emprestimo.data_prev_devol.date()
        if data_devol_prevista < data_ref.date() and not emprestimo.devolvido:
            dias_atraso = (data_ref.date() - data_devol_prevista).days
            return dias_atraso * 1.0  # R$1,00 por dia
        return 0.0

    def relatorio_inventario(self):
        builder = self._relatorio_builder("Inventário do Acervo")
        return builder.construir_inventario()

    def relatorio_debitos(self, emprestimos: list):
        builder = self._relatorio_builder("Débitos em Aberto")
        return builder.construir_debitos(emprestimos, datetime.now())

    def historico_usuario(self, emprestimos: list, usuario):
        builder = self._relatorio_builder(f"Histórico de {usuario}")
        return builder.construir_historico_usuario(emprestimos, usuario)

    def _valida_obra(self, obra):
        if not isinstance(obra, Obra):
            raise TypeError("Apenas instâncias de Obra são permitidas.")

    def _relatorio_builder(self, titulo):
        return self._RelatorioBuilder(self, titulo)

    class _RelatorioBuilder:
        def __init__(self, acervo, titulo):
            self.acervo = acervo
            self.titulo = titulo

        def construir_inventario(self):
            tabela = Table(title=self.titulo)
            tabela.add_column("Obra", justify="left", style="cyan")
            tabela.add_column("Quantidade", justify="right", style="magenta")

            for obra, qtd in self.acervo.obras.items():
                tabela.add_row(str(obra), str(qtd))
            return tabela

        def construir_debitos(self, emprestimos, data_ref):
            tabela = Table(title=self.titulo)
            tabela.add_column("Usuário", style="green")
            tabela.add_column("Obra", style="cyan")
            tabela.add_column("Prev. Devolução", style="yellow")
            tabela.add_column("Dias em Atraso", justify="right", style="red")
            tabela.add_column("Valor Multa", justify="right", style="red")

            for emp in emprestimos:
                if not emp.devolvido and emp.data_prev_devol < data_ref:
                    dias_atraso = (data_ref - emp.data_prev_devol).days
                    valor_multa = dias_atraso * 1.0
                    tabela.add_row(
                        str(emp.usuario),
                        str(emp.obra),
                        emp.data_prev_devol.strftime("%d/%m/%Y"),
                        str(dias_atraso),
                        f"R$ {valor_multa:.2f}"
                    )
            return tabela

        def construir_historico_usuario(self, emprestimos, usuario):
            tabela = Table(title=self.titulo)
            tabela.add_column("Obra", style="cyan")
            tabela.add_column("Retirada", style="green")
            tabela.add_column("Prev. Devolução", style="yellow")
            tabela.add_column("Devolvido?", justify="center", style="magenta")
            tabela.add_column("Data Devolução", style="green")

            for emp in emprestimos:
                if emp.usuario == usuario:
                    devolvido = "Sim" if emp.devolvido else "Não"
                    data_dev = emp.data_devolucao_real.strftime("%d/%m/%Y") if emp.data_devolucao_real else "-"
                    tabela.add_row(
                        str(emp.obra),
                        emp.data_retirada.strftime("%d/%m/%Y"),
                        emp.data_prev_devol.strftime("%d/%m/%Y"),
                        devolvido,
                        data_dev
                    )
            return tabela
