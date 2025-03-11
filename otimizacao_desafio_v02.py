from datetime import datetime
from abc import ABC, abstractmethod

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if self.valor > 0:
            conta.saldo += self.valor
            conta.historico.adicionar_transacao(self)
            return True
        return False

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if 0 < self.valor <= conta.saldo:
            conta.saldo -= self.valor
            conta.historico.adicionar_transacao(self)
            return True
        return False

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        descricao = f"{timestamp} - {'Depósito' if isinstance(transacao, Deposito) else 'Saque'}: R$ {transacao.valor:.2f}"
        self.transacoes.append(descricao)

class Conta:
    def __init__(self, cliente, numero):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = "0001"
        self.cliente = cliente
        self.historico = Historico()

    def sacar(self, valor):
        return Saque(valor).registrar(self)

    def depositar(self, valor):
        return Deposito(valor).registrar(self)

class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500, limite_saques=3):
        super().__init__(cliente, numero)
        self.limite = limite
        self.limite_saques = limite_saques
        self.saques_realizados = 0

    def sacar(self, valor):
        if self.saques_realizados >= self.limite_saques:
            return False
        if valor > self.limite:
            return False
        if super().sacar(valor):
            self.saques_realizados += 1
            return True
        return False

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        return transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class Banco:
    def __init__(self):
        self.clientes = []
        self.contas = []

    def cadastrar_cliente(self, cpf, nome, data_nascimento, endereco):
        if any(cliente.cpf == cpf for cliente in self.clientes):
            return None
        cliente = PessoaFisica(cpf, nome, data_nascimento, endereco)
        self.clientes.append(cliente)
        return cliente

    def criar_conta(self, cliente):
        numero_conta = len(self.contas) + 1
        conta = ContaCorrente(cliente, numero_conta)
        cliente.adicionar_conta(conta)
        self.contas.append(conta)
        return conta

banco = Banco()
while True:
    print("\n1 - Criar Cliente")
    print("2 - Criar Conta")
    print("3 - Depositar")
    print("4 - Sacar")
    print("5 - Extrato")
    print("6 - Sair")
    opcao = input("Escolha uma opção: ")
    if opcao == "1":
        cpf = input("CPF: ")
        nome = input("Nome: ")
        data_nascimento = input("Data de Nascimento: ")
        endereco = input("Endereço: ")
        cliente = banco.cadastrar_cliente(cpf, nome, data_nascimento, endereco)
        if cliente:
            print("Cliente cadastrado com sucesso.")
        else:
            print("CPF já cadastrado.")
    elif opcao == "2":
        cpf = input("CPF do Cliente: ")
        cliente = next((c for c in banco.clientes if c.cpf == cpf), None)
        if cliente:
            conta = banco.criar_conta(cliente)
            print(f"Conta {conta.numero} criada com sucesso.")
        else:
            print("Cliente não encontrado.")
    elif opcao == "3":
        numero = int(input("Número da Conta: "))
        valor = float(input("Valor: "))
        conta = next((c for c in banco.contas if c.numero == numero), None)
        if conta and conta.depositar(valor):
            print("Depósito realizado com sucesso.")
        else:
            print("Erro no depósito.")
    elif opcao == "4":
        numero = int(input("Número da Conta: "))
        valor = float(input("Valor: "))
        conta = next((c for c in banco.contas if c.numero == numero), None)
        if conta and conta.sacar(valor):
            print("Saque realizado com sucesso.")
        else:
            print("Erro no saque.")
    elif opcao == "5":
        numero = int(input("Número da Conta: "))
        conta = next((c for c in banco.contas if c.numero == numero), None)
        if conta:
            print("\n### EXTRATO ###")
            for transacao in conta.historico.transacoes:
                print(transacao)
            print(f"Saldo: R$ {conta.saldo:.2f}")
        else:
            print("Conta não encontrada.")
    elif opcao == "6":
        break
    else:
        print("Opção inválida.")
