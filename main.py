from clube import Clube, Jogador, Tecnico

MENU = (
    "===== SISTEMA DE GESTÃO DO CLUBE =====\n"
    "1 - Cadastrar jogador\n"
    "2 - Cadastrar técnico\n"
    "3 - Listar membros\n"
    "4 - Registrar gol\n"
    "5 - Registrar assistência\n"
    "6 - Consultar membro\n"
    "7 - Consultar folha salarial\n"
    "8 - Remover membro\n"
    "0 - Sair\n"
    "Escolha uma opção: "
)


def ler_inteiro(mensagem, minimo=0):
    erro = ""

    while True:
        try:
            valor = int(input(f"{erro}{mensagem}"))

            if valor < minimo:
                erro = f"Digite um número maior ou igual a {minimo}.\n"
            else:
                return valor

        except ValueError:
            erro = "Digite um número inteiro válido.\n"


def ler_salario():
    erro = ""

    while True:
        try:
            salario = float(input(f"{erro}Salário: R$ ").replace(",", "."))

            if salario < 0:
                erro = "O salário não pode ser negativo.\n"
            else:
                return salario

        except ValueError:
            erro = "Digite um salário válido.\n"


def cadastrar_jogador(clube):
    nome = input("Nome do jogador: ")
    idade = ler_inteiro("Idade: ", 1)
    salario = ler_salario()
    posicao = input("Posição: ")

    jogador = Jogador(nome, idade, salario, posicao)
    return clube.adicionar_membro(jogador)


def cadastrar_tecnico(clube):
    nome = input("Nome do técnico: ")
    idade = ler_inteiro("Idade: ", 1)
    salario = ler_salario()
    licencas = input("Licenças do técnico: ")

    tecnico = Tecnico(nome, idade, salario, licencas)
    return clube.adicionar_membro(tecnico)


def registrar_gol(clube):
    nome = input("Nome do jogador: ")
    pessoa = clube.buscar_membro(nome)

    if isinstance(pessoa, Jogador):
        return pessoa.marcar_gol()
    return "Jogador não encontrado."


def registrar_assistencia(clube):
    nome = input("Nome do jogador: ")
    pessoa = clube.buscar_membro(nome)

    if isinstance(pessoa, Jogador):
        return pessoa.dar_assistencia()
    return "Jogador não encontrado."


def consultar_membro(clube):
    nome = input("Nome do membro: ")
    pessoa = clube.buscar_membro(nome)

    if pessoa is not None:
        return pessoa.apresentar()
    return "Membro não encontrado."


def consultar_folha(clube):
    total = clube.calcular_folha_salarial()
    return f"Folha salarial total: R$ {total:.2f}"


def remover_membro(clube):
    nome = input("Nome do membro que deseja remover: ")
    return clube.remover_membro(nome)


def main():
    nome_clube = input("Nome do clube de futebol: ")
    clube = Clube(nome_clube)

    # Sem usar print: o resultado da última ação aparece junto do próximo menu.
    resultado = ""

    while True:
        cabecalho = f"\n{resultado}\n\n" if resultado else "\n"
        opcao = input(cabecalho + MENU)

        if opcao == "1":
            resultado = cadastrar_jogador(clube)

        elif opcao == "2":
            resultado = cadastrar_tecnico(clube)

        elif opcao == "3":
            resultado = clube.listar_membros()

        elif opcao == "4":
            resultado = registrar_gol(clube)

        elif opcao == "5":
            resultado = registrar_assistencia(clube)

        elif opcao == "6":
            resultado = consultar_membro(clube)

        elif opcao == "7":
            resultado = consultar_folha(clube)

        elif opcao == "8":
            resultado = remover_membro(clube)

        elif opcao == "0":
            return "Sistema encerrado."

        else:
            resultado = "Opção inválida. Tente novamente."


if __name__ == "__main__":
    main()