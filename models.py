import uuid
from datetime import datetime

class BaseEntity:
    """Classe base para entidades do sistema, contendo ID único e data de criação."""

    def __init__(self):
        """Inicializa a entidade com ID único e data de criação atual."""
        self.id = self._gerar_id()
        self.data_criacao = datetime.now()

    def __eq__(self, other):
        """Compara entidades com base no ID e classe.

        Args:
            other (BaseEntity): Outro objeto para comparar.

        Returns:
            bool: True se forem do mesmo tipo e ID, False caso contrário.
        """
        return isinstance(other, self.__class__) and self.id == other.id

    def _gerar_id(self):
        """Gera um UUID para identificação única.

        Returns:
            UUID: Identificador único.
        """
        return uuid.uuid4()

class Obra(BaseEntity):
    """Classe que representa uma obra (livro, filme etc.)."""

    def __init__(self, titulo, autor, ano, categoria, quantidade=1):
        """Inicializa uma obra com suas informações básicas.

        Args:
            titulo (str): Título da obra.
            autor (str): Nome do autor.
            ano (int): Ano de publicação.
            categoria (str): Categoria da obra.
            quantidade (int, optional): Quantidade em estoque. Default é 1.
        """
        super().__init__()
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.categoria = categoria
        self.quantidade = quantidade

    def __eq__(self, other):
        """Compara obras por título e autor.

        Args:
            other (Obra): Outra obra.

        Returns:
            bool: True se tiverem mesmo título e autor.
        """
        if isinstance(other, Obra):
            return self.titulo == other.titulo and self.autor == other.autor
        return False

    def __hash__(self):
        """Gera hash com base no título e autor.

        Returns:
            int: Hash da obra.
        """
        return hash((self.titulo, self.autor))

    def disponivel(self, estoque):
        """Verifica se a obra está disponível.

        Args:
            estoque (dict): Dicionário de obras.

        Returns:
            bool: True se quantidade > 0.
        """
        return self.quantidade > 0

    def __str__(self):
        """Retorna string formatada da obra.

        Returns:
            str: Representação da obra.
        """
        return f"{self.titulo} ({self.ano}) - {self.autor} | Categoria: {self.categoria} | Qtd: {self.quantidade}"

class Usuario(BaseEntity):
    """Classe que representa um usuário do sistema."""

    def __init__(self, nome, email):
        """Inicializa um usuário com nome e email.

        Args:
            nome (str): Nome do usuário.
            email (str): Email do usuário.
        """
        super().__init__()
        self.nome = nome
        self.email = email

    def __lt__(self, other):
        """Compara usuários alfabeticamente pelo nome.

        Args:
            other (Usuario): Outro usuário.

        Returns:
            bool: True se nome for menor (ordem alfabética).
        """
        return self.nome.lower() < other.nome.lower()

    def __str__(self):
        """Retorna o nome do usuário.

        Returns:
            str: Nome.
        """
        return self.nome

class Emprestimo(BaseEntity):
    """Classe que representa um empréstimo de uma obra para um usuário."""

    def __init__(self, obra, usuario, data_retirada, data_prev_devol):
        """Inicializa um empréstimo.

        Args:
            obra (Obra): Obra emprestada.
            usuario (Usuario): Usuário que pegou emprestado.
            data_retirada (datetime): Data da retirada.
            data_prev_devol (datetime): Data prevista para devolução.
        """
        super().__init__()
        self.obra = obra
        self.usuario = usuario
        self.data_retirada = data_retirada
        self.data_prev_devol = data_prev_devol
        self.data_devolucao_real = None

    def marcar_devolucao(self, data_dev_real):
        """Marca a data real de devolução.

        Args:
            data_dev_real (datetime): Data em que a obra foi devolvida.
        """
        self.data_devolucao_real = data_dev_real

    @property
    def devolvido(self):
        """Verifica se a obra foi devolvida.

        Returns:
            bool: True se foi devolvida.
        """
        return self.data_devolucao_real is not None

    def dias_atraso(self):
        """Calcula os dias de atraso na devolução.

        Returns:
            int | None: Dias de atraso ou None se não devolvido.
        """
        if self.data_devolucao_real is None:
            print("Livro ainda não foi devolvido.")
        else:
            atraso = (self.data_devolucao_real - self.data_prev_devol).days
            return atraso

    def __str__(self):
        """Retorna uma string formatada do empréstimo.

        Returns:
            str: Resumo do empréstimo.
        """
        return f"Obra: {self.obra.titulo} | Retirada: {self.data_retirada.strftime('%d/%m/%Y')} | Prevista: {self.data_prev_devol.strftime('%d/%m/%Y')}"


