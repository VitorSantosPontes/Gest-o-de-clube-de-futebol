import tkinter as tk
from tkinter import ttk, messagebox
from clube import Clube, Jogador, Tecnico


class InterfaceClube:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title('Sistema de Gestão de um Clube de Futebol')
        self.janela.geometry('960x650')
        self.janela.minsize(780, 540)
        self.clube = Clube('Meu Clube')

        estilo = ttk.Style()
        if 'clam' in estilo.theme_names():
            estilo.theme_use('clam')
        estilo.configure('Titulo.TLabel', font=('Arial', 17, 'bold'))
        estilo.configure('TButton', padding=7)
        estilo.configure('Treeview', rowheight=27)
        estilo.configure('Treeview.Heading', font=('Arial', 10, 'bold'))

        topo = ttk.Frame(janela, padding=16)
        topo.pack(fill='x')
        ttk.Label(topo, text='⚽ Gestão do Clube de Futebol', style='Titulo.TLabel').pack(anchor='w')
        ttk.Label(topo, text='Cadastre membros, acompanhe estatísticas e consulte a folha salarial.').pack(anchor='w', pady=(5, 0))

        self.abas = ttk.Notebook(janela)
        self.abas.pack(fill='both', expand=True, padx=16, pady=(0, 16))
        self.aba_cadastro = ttk.Frame(self.abas, padding=18)
        self.aba_membros = ttk.Frame(self.abas, padding=18)
        self.aba_acoes = ttk.Frame(self.abas, padding=18)
        self.abas.add(self.aba_cadastro, text='Cadastrar')
        self.abas.add(self.aba_membros, text='Membros')
        self.abas.add(self.aba_acoes, text='Gols e assistências')
        self.montar_cadastro()
        self.montar_membros()
        self.montar_acoes()
        self.atualizar_lista()

    def montar_cadastro(self):
        quadro = ttk.LabelFrame(self.aba_cadastro, text='Dados do membro', padding=18)
        quadro.pack(fill='x')
        self.tipo = tk.StringVar(value='Jogador')
        self.nome = tk.StringVar()
        self.idade = tk.StringVar()
        self.salario = tk.StringVar()
        self.extra = tk.StringVar()
        ttk.Label(quadro, text='Tipo de membro').grid(row=0, column=0, sticky='w', pady=7)
        tipos = ttk.Combobox(quadro, textvariable=self.tipo, values=['Jogador', 'Técnico'], state='readonly', width=27)
        tipos.grid(row=0, column=1, sticky='ew', padx=10, pady=7)
        tipos.bind('<<ComboboxSelected>>', self.atualizar_campo_extra)
        for linha, titulo, variavel in [(1, 'Nome', self.nome), (2, 'Idade', self.idade), (3, 'Salário (R$)', self.salario)]:
            ttk.Label(quadro, text=titulo).grid(row=linha, column=0, sticky='w', pady=7)
            ttk.Entry(quadro, textvariable=variavel).grid(row=linha, column=1, sticky='ew', padx=10, pady=7)
        self.rotulo_extra = ttk.Label(quadro, text='Posição')
        self.rotulo_extra.grid(row=4, column=0, sticky='w', pady=7)
        ttk.Entry(quadro, textvariable=self.extra).grid(row=4, column=1, sticky='ew', padx=10, pady=7)
        quadro.columnconfigure(1, weight=1)
        ttk.Button(self.aba_cadastro, text='Cadastrar membro', command=self.cadastrar).pack(anchor='w', pady=18)

    def atualizar_campo_extra(self, evento=None):
        self.rotulo_extra.configure(text='Posição' if self.tipo.get() == 'Jogador' else 'Licenças')
        self.extra.set('')

    def cadastrar(self):
        nome = self.nome.get().strip()
        extra = self.extra.get().strip()
        try:
            idade = int(self.idade.get().strip())
            salario = float(self.salario.get().strip().replace(',', '.'))
            if idade < 1 or salario < 0 or not nome or not extra:
                raise ValueError
        except ValueError:
            messagebox.showerror('Dados inválidos', 'Preencha nome, idade positiva, salário não negativo e posição/licenças corretamente.')
            return
        if self.clube.buscar_membro(nome) is not None:
            messagebox.showwarning('Nome repetido', 'Já existe um membro com esse nome. Use um nome diferente.')
            return
        if self.tipo.get() == 'Jogador':
            pessoa = Jogador(nome, idade, salario, extra)
        else:
            pessoa = Tecnico(nome, idade, salario, extra)
        self.clube.adicionar_membro(pessoa)
        for campo in (self.nome, self.idade, self.salario, self.extra):
            campo.set('')
        self.atualizar_lista()
        messagebox.showinfo('Cadastro realizado', 'Membro cadastrado com sucesso!')

    def montar_membros(self):
        barra = ttk.Frame(self.aba_membros)
        barra.pack(fill='x', pady=(0, 12))
        ttk.Button(barra, text='Atualizar lista', command=self.atualizar_lista).pack(side='left', padx=(0, 8))
        ttk.Button(barra, text='Consultar selecionado', command=self.consultar).pack(side='left', padx=(0, 8))
        ttk.Button(barra, text='Remover selecionado', command=self.remover).pack(side='left')
        colunas = ('tipo', 'nome', 'idade', 'salario')
        self.tabela = ttk.Treeview(self.aba_membros, columns=colunas, show='headings', selectmode='browse')
        for coluna, titulo, largura in [('tipo', 'Tipo', 120), ('nome', 'Nome', 260), ('idade', 'Idade', 100), ('salario', 'Salário (R$)', 160)]:
            self.tabela.heading(coluna, text=titulo)
            self.tabela.column(coluna, width=largura, anchor='w')
        rolagem = ttk.Scrollbar(self.aba_membros, orient='vertical', command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=rolagem.set)
        rolagem.pack(side='right', fill='y')
        self.tabela.pack(fill='both', expand=True)
        self.tabela.bind('<Double-1>', lambda evento: self.consultar())
        self.resumo = ttk.Label(self.aba_membros, text='')
        self.resumo.pack(anchor='w', pady=(12, 0))

    def atualizar_lista(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)
        # Usa a lista de membros fornecida pelo próprio clube, sem acessar atributos privados.
        # A busca por nome é realizada pelas operações públicas da classe Clube.
        self.nomes_exibidos = []
        # O método listar_membros() produz texto; uma lista estruturada permite montar a tabela.
        for pessoa in self.clube.listar_objetos():
            self.nomes_exibidos.append(pessoa.consultar_nome())
            tipo = 'Jogador' if isinstance(pessoa, Jogador) else 'Técnico'
            self.tabela.insert('', 'end', values=(tipo, pessoa.consultar_nome(), pessoa.consultar_idade(), f'{pessoa.consultar_salario():.2f}'))
        self.resumo.configure(text=f'Membros cadastrados: {len(self.nomes_exibidos)}     |     Folha salarial total: R$ {self.clube.calcular_folha_salarial():.2f}')
        self.atualizar_jogadores()

    def selecionado(self):
        itens = self.tabela.selection()
        if not itens:
            messagebox.showwarning('Seleção necessária', 'Selecione um membro na tabela.')
            return None
        nome = self.tabela.item(itens[0], 'values')[1]
        return self.clube.buscar_membro(nome)

    def consultar(self):
        pessoa = self.selecionado()
        if pessoa is not None:
            messagebox.showinfo('Dados do membro', pessoa.apresentar())

    def remover(self):
        pessoa = self.selecionado()
        if pessoa is not None and messagebox.askyesno('Confirmar remoção', f'Remover {pessoa.consultar_nome()} do clube?'):
            self.clube.remover_membro(pessoa.consultar_nome())
            self.atualizar_lista()

    def montar_acoes(self):
        quadro = ttk.LabelFrame(self.aba_acoes, text='Estatísticas dos jogadores', padding=18)
        quadro.pack(fill='x')
        ttk.Label(quadro, text='Selecione um jogador').pack(anchor='w')
        self.jogador_escolhido = tk.StringVar()
        self.combo_jogadores = ttk.Combobox(quadro, textvariable=self.jogador_escolhido, state='readonly', width=40)
        self.combo_jogadores.pack(anchor='w', pady=10)
        botoes = ttk.Frame(quadro)
        botoes.pack(anchor='w', pady=8)
        ttk.Button(botoes, text='Registrar gol', command=lambda: self.registrar('gol')).pack(side='left', padx=(0, 10))
        ttk.Button(botoes, text='Registrar assistência', command=lambda: self.registrar('assistencia')).pack(side='left')
        ttk.Button(quadro, text='Ver estatísticas do jogador', command=self.ver_estatisticas).pack(anchor='w', pady=8)

    def atualizar_jogadores(self):
        nomes = [p.consultar_nome() for p in self.clube.listar_objetos() if isinstance(p, Jogador)]
        self.combo_jogadores['values'] = nomes
        if self.jogador_escolhido.get() not in nomes:
            self.jogador_escolhido.set('')

    def jogador_atual(self):
        pessoa = self.clube.buscar_membro(self.jogador_escolhido.get())
        if not isinstance(pessoa, Jogador):
            messagebox.showwarning('Jogador necessário', 'Selecione um jogador cadastrado.')
            return None
        return pessoa

    def registrar(self, acao):
        jogador = self.jogador_atual()
        if jogador is not None:
            resultado = jogador.marcar_gol() if acao == 'gol' else jogador.dar_assistencia()
            messagebox.showinfo('Registro realizado', resultado)

    def ver_estatisticas(self):
        jogador = self.jogador_atual()
        if jogador is not None:
            messagebox.showinfo('Estatísticas', jogador.apresentar())


if __name__ == '__main__':
    raiz = tk.Tk()
    InterfaceClube(raiz)
    raiz.mainloop()
