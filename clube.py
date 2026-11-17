from abc import ABC, abstractmethod

SEPARADOR = "--------------------"


class Pessoa(ABC):
    def __init__(self, nome, idade, salario):
        self.__nome = nome
        self.__idade = idade
        self.__salario = salario

    def consultar_nome(self):
        return self.__nome

    def consultar_idade(self):
        return self.__idade

    def consultar_salario(self):
        return self.__salario

    @abstractmethod
    def apresentar(self):
        pass


class Jogador(Pessoa):
    def __init__(self, nome, idade, salario, posicao):
        super().__init__(nome, idade, salario)
        self.__posicao = posicao
        self.__gols = 0
        self.__assistencias = 0

    def marcar_gol(self):
        self.__gols += 1
        return "Gol registrado com sucesso!"

    def dar_assistencia(self):
        self.__assistencias += 1
        return "Assistência registrada com sucesso!"

    def apresentar(self):
        return (
            f"Jogador: {self.consultar_nome()}\n"
            f"Idade: {self.consultar_idade()}\n"
            f"Salário: R$ {self.consultar_salario():.2f}\n"
            f"Posição: {self.__posicao}\n"
            f"Gols: {self.__gols}\n"
            f"Assistências: {self.__assistencias}"
        )


class Tecnico(Pessoa):
    def __init__(self, nome, idade, salario, licencas):
        super().__init__(nome, idade, salario)
        self.__licencas = licencas

    def apresentar(self):
        return (
            f"Técnico: {self.consultar_nome()}\n"
            f"Idade: {self.consultar_idade()}\n"
            f"Salário: R$ {self.consultar_salario():.2f}\n"
            f"Licenças: {self.__licencas}"
        )


class Clube:
    def __init__(self, nome):
        self.__nome = nome
        self.__membros = []

    def adicionar_membro(self, pessoa):
        self.__membros.append(pessoa)
        return "Membro cadastrado com sucesso!"

    def listar_membros(self):
        if not self.__membros:
            return "Nenhum membro cadastrado."

        blocos = [f"{SEPARADOR}\n{pessoa.apresentar()}" for pessoa in self.__membros]
        return "\n".join(blocos)

    def listar_objetos(self):
        return self.__membros.copy()

    def buscar_membro(self, nome):
        for pessoa in self.__membros:
            if pessoa.consultar_nome().lower() == nome.lower():
                return pessoa
        return None

    def calcular_folha_salarial(self):
        total = 0

        for pessoa in self.__membros:
            total += pessoa.consultar_salario()

        return total

    def remover_membro(self, nome):
        pessoa = self.buscar_membro(nome)

        if pessoa is not None:
            self.__membros.remove(pessoa)
            return "Membro removido com sucesso!"
        return "Membro não encontrado."


