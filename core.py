from models import *
from datetime import datetime, timedelta
from rich.table import Table

class Acervo:
    """Classe que gerencia o acervo de obras e operações de empréstimo, devolução e relatórios."""

    def __init__(self):
        """Inicializa o acervo com um dicionário vazio de obras."""
        self.obras = {}

    def __iadd__(self, obra: Obra):
        """Adiciona uma obra ao acervo utilizando o operador +=.

        Args:
            obra (Obra): Obra a ser adicionada.

        Returns:
            Acervo: O próprio acervo com a obra adicionada.
        """
        self.adicionar(obra)
        return self

    def __isub__(self, obra: Obra):
        """Remove uma obra do acervo utilizando o operador -=.

        Args:
            obra (Obra): Obra a ser removida.

        Returns:
            Acervo: O próprio acervo com a obra removida.
        """
        self.remover(obra)
        return self

    def adicionar(self, obra):
        """Adiciona uma unidade da obra ao acervo.

        Args:
            obra (Obra): Obra a ser adicionada.
        """
        if obra in self.obras:
            self.obras[obra] += 1
        else:
            self.obras[obra] = 1

    def remover(self, obra):
        """Remove uma unidade da obra do acervo.

        Args:
            obra (Obra): Obra a ser removida.
        """
        if obra in self.obras:
            if self.obras[obra] > 1:
                self.obras[obra] -= 1
            else:
                del self.obras[obra]

    def emprestar(self, obra, usuario, dias: int = 7):
        """Realiza um empréstimo de uma obra para um usuário.

        Args:
            obra (Obra): Obra a ser emprestada.
            usuario (Usuario): Usuário que irá pegar emprestado.
            dias (int, optional): Dias de empréstimo. Default é 7.

        Returns:
            Emprestimo: Instância do empréstimo realizado.
        """
        if obra not in self.obras or self.obras[obra] == 0:
            raise ValueError("Obra indisponível no acervo.")
        self.obras[obra] -= 1
        data_retirada = datetime.now()
        data_prev_devol = data_retirada + timedelta(days=dias)
        return Emprestimo(obra, usuario, data_retirada, data_prev_devol)

    def devolver(self, emprestimo, data_dev: datetime):
        """Registra a devolução de uma obra.

        Args:
            emprestimo (Emprestimo): Empréstimo a ser devolvido.
            data_dev (datetime): Data da devolução.
        """
        emprestimo.marcar_devolucao(data_dev)
        if emprestimo.obra in self.obras:
            self.obras[emprestimo.obra] += 1
        else:
            self.obras[emprestimo.obra] = 1

    def renovar(self, emprestimo, dias_extras):
        """Renova o prazo de devolução de um empréstimo.

        Args:
            emprestimo (Emprestimo): Empréstimo a ser renovado.
            dias_extras (int): Dias a adicionar ao prazo atual.

        Raises:
            ValueError: Se a nova data for anterior à atual.
        """
        nova_data = emprestimo.data_prev_devol + timedelta(days=dias_extras)
        if nova_data < emprestimo.data_prev_devol:
            raise ValueError("A data nova não pode ser anterior à data atual.")
        emprestimo.data_prev_devol = nova_data

    def valor_multa(self, emprestimo, data_ref):
        """Calcula o valor da multa com base na data de referência.

        Args:
            emprestimo (Emprestimo): Empréstimo em análise.
            data_ref (datetime): Data usada como base.

        Returns:
            float: Valor da multa.
        """
        data_devol_prevista = emprestimo.data_prev_devol.date()
        if data_devol_prevista < data_ref.date() and not emprestimo.devolvido:
            dias_atraso = (data_ref.date() - data_devol_prevista).days
            return dias_atraso * 1.0
        return 0.0

    def relatorio_inventario(self):
        """Gera o relatório de inventário do acervo.

        Returns:
            Table: Tabela formatada com as obras e quantidades.
        """
        builder = self._relatorio_builder("Inventário do Acervo")
        return builder.construir_inventario()

    def relatorio_debitos(self, emprestimos: list):
        """Gera o relatório de débitos em aberto.

        Args:
            emprestimos (list): Lista de empréstimos.

        Returns:
            Table: Tabela com os débitos em aberto.
        """
        builder = self._relatorio_builder("Débitos em Aberto")
        return builder.construir_debitos(emprestimos, datetime.now())

    def historico_usuario(self, emprestimos: list, usuario):
        """Gera o histórico de empréstimos de um usuário.

        Args:
            emprestimos (list): Lista de empréstimos.
            usuario (Usuario): Usuário em questão.

        Returns:
            Table: Tabela com o histórico.
        """
        builder = self._relatorio_builder(f"Histórico de {usuario}")
        return builder.construir_historico_usuario(emprestimos, usuario)

    def _valida_obra(self, obra):
        """Valida se o objeto é uma instância de Obra.

        Args:
            obra (any): Objeto a validar.

        Raises:
            TypeError: Se o objeto não for do tipo Obra.
        """
        if not isinstance(obra, Obra):
            raise TypeError("Apenas instâncias de Obra são permitidas.")

    def _relatorio_builder(self, titulo):
        """Cria um construtor de relatórios.

        Args:
            titulo (str): Título do relatório.

        Returns:
            _RelatorioBuilder: Instância do builder.
        """
        return self._RelatorioBuilder(self, titulo)

    class _RelatorioBuilder:
        """Classe interna responsável por construir relatórios formatados."""

        def __init__(self, acervo, titulo):
            """Inicializa o builder de relatório.

            Args:
                acervo (Acervo): Instância do acervo.
                titulo (str): Título do relatório.
            """
            self.acervo = acervo
            self.titulo = titulo

        def construir_inventario(self):
            """Constrói o relatório de inventário.

            Returns:
                Table: Tabela do inventário.
            """
            tabela = Table(title=self.titulo)
            tabela.add_column("Obra", justify="left", style="cyan")
            tabela.add_column("Quantidade", justify="right", style="magenta")
            for obra, qtd in self.acervo.obras.items():
                tabela.add_row(str(obra), str(qtd))
            return tabela

        def construir_debitos(self, emprestimos, data_ref):
            """Constrói o relatório de débitos em aberto.

            Args:
                emprestimos (list): Lista de empréstimos.
                data_ref (datetime): Data de referência.

            Returns:
                Table: Tabela de débitos.
            """
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
            """Constrói o histórico de empréstimos de um usuário.

            Args:
                emprestimos (list): Lista de empréstimos.
                usuario (Usuario): Usuário desejado.

            Returns:
                Table: Tabela de histórico.
            """
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

