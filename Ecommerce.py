# e_commerce.py
# Esqueleto do sistema de E-commerce em Python.
# Objetivo: fornecer somente as estruturas básicas + comentários orientando a implementação.
# Observações didáticas:
# - Para valores monetários, prefira 'decimal.Decimal' a 'float' (precisão).
# - IDs podem ser gerados com uuid.uuid4().
# - Se desejar, adicione validações (ex.: CPF, email) como extensão.

import uuid                     # gerar identificadores únicos (UUID)
from decimal import Decimal     # representação apropriada de dinheiro
from typing import List, Dict   # anotações de tipo (listas e dicionários)


# =========================
# CLASSE PESSOA
# =========================
class Pessoa:
    """
    Representa uma pessoa com atributos básicos.
    Atributos obrigatórios: nome, cpf, email.

    Tarefas do aluno:
    - Implementar o construtor (__init__) atribuindo os atributos.
    - (Opcional) Validar CPF / email.
    - (Opcional) Criar __str__/__repr__ para facilitar a depuração.
    """

    def __init__(self, nome: str, cpf: str, email: str) -> None:
        self.nome = nome
        self.cpf = cpf
        self.email = email

    def __repr__(self):
        return f"Pessoa(nome={self.nome}, cpf={self.cpf}, email={self.email})"


# =========================
# CLASSE CLIENTE
# =========================
class Cliente:
    """
    Representa um cliente do e-commerce, associado a uma Pessoa.
    Atributos: pessoa (objeto Pessoa), id_cliente (str).

    Tarefas do aluno:
    - Implementar o construtor recebendo uma Pessoa.
    - Gerar id_cliente com str(uuid.uuid4()).
    - (Opcional) Criar __str__/__repr__.
    """

    def __init__(self, pessoa: Pessoa) -> None:
        self.pessoa = pessoa
        self.id_cliente = str(uuid.uuid4())

    def __repr__(self):
        return f"Cliente(id_cliente={self.id_cliente}, pessoa={self.pessoa})"


# =========================
# CLASSE PRODUTO
# =========================
class Produto:
    """
    Representa um produto disponível para venda.
    Atributos: nome (str), preco (Decimal), estoque (int).

    Tarefas do aluno:
    - Implementar o construtor e armazenar os atributos.
    - (Opcional) Validar: preco >= 0 e estoque >= 0.
    - (Opcional) Criar __str__/__repr__.
    - (Opcional) Métodos utilitários (ex.: pode_atender, debitar, creditar) se o enunciado pedir.
    """

    def __init__(self, nome: str, preco: Decimal, estoque: int) -> None:
        if preco < 0 or estoque < 0:
            raise ValueError("Preço e estoque devem ser não-negativos.")
        self.nome = nome
        self.preco = preco
        self.estoque = estoque

    def __repr__(self):
        return f"Produto(nome={self.nome}, preco={self.preco}, estoque={self.estoque})"


# =========================
# CLASSE ITEMPEDIDO
# =========================
class ItemPedido:
    """
    Representa um item dentro de um pedido (produto + quantidade).
    Atributos: produto (Produto), quantidade (int).

    Tarefas do aluno:
    - Implementar o construtor.
    - Implementar calcular_total() = produto.preco * quantidade.
    """

    def __init__(self, produto: Produto, quantidade: int) -> None:
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser maior que zero.")
        self.produto = produto
        self.quantidade = quantidade

    def calcular_total(self) -> Decimal:
        return self.produto.preco * Decimal(self.quantidade)


# =========================
# CLASSE PEDIDO
# =========================
class Pedido:
    """
    Representa um pedido realizado por um cliente.
    Atributos: cliente (Cliente), itens (List[ItemPedido]).

    Tarefas do aluno:
    - Implementar o construtor inicializando a lista de itens vazia.
    - Implementar adicionar_item(produto, quantidade): cria ItemPedido e adiciona à lista.
    - Implementar calcular_total(): soma dos totais dos itens.
    - (Opcional) confirmar(): validar estoques e debitar (se fizer parte do enunciado).
    """

    def __init__(self, cliente: Cliente) -> None:
        self.cliente = cliente
        self.itens: List[ItemPedido] = []

    def adicionar_item(self, produto: Produto, quantidade: int) -> None:
        item = ItemPedido(produto, quantidade)
        self.itens.append(item)

    def calcular_total(self) -> Decimal:
        return sum(item.calcular_total() for item in self.itens)


# =========================
# CLASSE MENU
# =========================
class Menu:
    """
    Gerencia o e-commerce: cadastro de clientes, produtos e pedidos.
    Sugestões de estruturas em memória:
    - clientes: Dict[str, Cliente]  (chave = CPF)
    - produtos: Dict[str, Produto]  (chave = ID ou nome; defina a estratégia)
    - pedidos: List[Pedido]

    Tarefas do aluno:
    - Implementar o construtor, inicializando as coleções.
    - Implementar métodos de cadastro e criação de pedidos.
    - Implementar exibir_menu() com interação via input() (CLI simples).
    """

    def __init__(self) -> None:
        self.clientes: Dict[str, Cliente] = {}
        self.produtos: Dict[str, Produto] = {}
        self.pedidos: List[Pedido] = []

    def cadastrar_cliente(self, nome: str, cpf: str, email: str) -> None:
        pessoa = Pessoa(nome, cpf, email)
        cliente = Cliente(pessoa)
        self.clientes[cpf] = cliente
        print(f"Cliente cadastrado: {cliente}")

    def cadastrar_produto(self, nome: str, preco: Decimal, estoque: int) -> None:
        produto = Produto(nome, preco, estoque)
        self.produtos[nome] = produto
        print(f"Produto cadastrado: {produto}")

    def criar_pedido(self, cpf: str) -> None:
        cliente = self.clientes.get(cpf)
        if not cliente:
            print("Cliente não encontrado.")
            return
        pedido = Pedido(cliente)
        while True:
            print("Produtos disponíveis:")
            for nome, produto in self.produtos.items():
                print(f"{nome} - Preço: {produto.preco} - Estoque: {produto.estoque}")
            nome_produto = input("Digite o nome do produto (ou 'fim' para encerrar): ")
            if nome_produto.lower() == 'fim':
                break
            produto = self.produtos.get(nome_produto)
            if not produto:
                print("Produto não encontrado.")
                continue
            try:
                quantidade = int(input("Quantidade: "))
                if quantidade > produto.estoque:
                    print("Estoque insuficiente.")
                    continue
                pedido.adicionar_item(produto, quantidade)
                produto.estoque -= quantidade
            except ValueError:
                print("Quantidade inválida.")
        total = pedido.calcular_total()
        print(f"Total do pedido: {total}")
        self.pedidos.append(pedido)

    def listar_pedidos(self) -> None:
        for idx, pedido in enumerate(self.pedidos, 1):
            print(f"Pedido {idx} - Cliente: {pedido.cliente.pessoa.nome}")
            for item in pedido.itens:
                print(f"  {item.produto.nome} x {item.quantidade} = {item.calcular_total()}")
            print(f"Total: {pedido.calcular_total()}\n")

    def exibir_menu(self) -> None:
        while True:
            print("\n--- Menu E-commerce ---")
            print("1. Cadastrar cliente")
            print("2. Cadastrar produto")
            print("3. Criar pedido")
            print("4. Listar pedidos")
            print("0. Sair")
            opcao = input("Escolha uma opção: ")
            if opcao == "1":
                nome = input("Nome: ")
                cpf = input("CPF: ")
                email = input("Email: ")
                self.cadastrar_cliente(nome, cpf, email)
            elif opcao == "2":
                nome = input("Nome do produto: ")
                preco = Decimal(input("Preço: "))
                estoque = int(input("Estoque: "))
                self.cadastrar_produto(nome, preco, estoque)
            elif opcao == "3":
                cpf = input("CPF do cliente: ")
                self.criar_pedido(cpf)
            elif opcao == "4":
                self.listar_pedidos()
            elif opcao == "0":
                print("Saindo...")
                break
            else:
                print("Opção inválida.")


# =========================
# PONTO DE ENTRADA
# =========================
if __name__ == "__main__":
    # Instancia o Menu e inicia a CLI.
    # Aluno deve implementar os métodos do Menu para que a interação funcione.
    menu = Menu()
    menu.exibir_menu()
