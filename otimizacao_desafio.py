from datetime import datetime

def menu():
    opcoes = [
        "Depositar", "Sacar", "Extrato",
        "Criar Usuário", "Criar Conta", "Listar Contas", "Sair"
    ]
    print("\n### MENU ###")
    for i, opcao in enumerate(opcoes, 1):
        print(f"{i} - {opcao}")


def validar_cpf(cpf, usuarios):
    return any(u["cpf"] == cpf for u in usuarios)


def encontrar_usuario(cpf, usuarios):
    return next((u for u in usuarios if u["cpf"] == cpf), None)


def deposito(saldo, valor, extrato):
    if valor > 0:
        saldo += valor
        extrato.append(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - Depósito: +R$ {valor:.2f}")
        print("Depósito realizado com sucesso.")
    else:
        print("Valor inválido.")
    return saldo, extrato


def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if numero_saques >= limite_saques:
        print("Limite de saques diários atingido.")
    elif valor > saldo:
        print("Saldo insuficiente.")
    elif valor > limite:
        print(f"O limite máximo por saque é R$ {limite:.2f}.")
    elif valor > 0:
        saldo -= valor
        extrato.append(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - Saque: -R$ {valor:.2f}")
        numero_saques += 1
        print("Saque realizado com sucesso.")
    else:
        print("Valor inválido.")
    
    return saldo, extrato, numero_saques


def exibir_extrato(saldo, *, extrato):
    print("\n### EXTRATO ###")
    if not extrato:
        print("Nenhuma movimentação registrada.")
    else:
        for operacao in extrato:
            print(operacao)
    print(f"Saldo atual: R$ {saldo:.2f}")


def cadastrar_usuario(usuarios):
    cpf = input("Informe o CPF (apenas números): ").strip()
    
    if not cpf.isdigit() or len(cpf) != 11:
        print("CPF inválido! Digite apenas números (11 dígitos).")
        return

    if validar_cpf(cpf, usuarios):
        print("CPF já cadastrado.")
        return
    
    nome = input("Nome completo: ").strip().title()
    data_nascimento = input("Data de nascimento (DD/MM/AAAA): ").strip()
    endereco = input("Endereço (logradouro, número - bairro - cidade/sigla estado): ").strip()
    
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("Usuário cadastrado com sucesso.")


def cadastrar_conta(usuarios, contas):
    cpf = input("Informe o CPF do usuário: ").strip()
    usuario = encontrar_usuario(cpf, usuarios)
    
    if usuario:
        numero_conta = len(contas) + 1
        contas.append({"agencia": "0001", "numero_conta": numero_conta, "usuario": usuario["nome"]})
        print("Conta criada com sucesso.")
    else:
        print("Usuário não encontrado. Cadastre-o primeiro.")


def listar_contas(contas):
    print("\n### LISTA DE CONTAS ###")
    if not contas:
        print("Nenhuma conta cadastrada.")
        return

    for conta in contas:
        print(f"🏦 Agência: {conta['agencia']} | 📄 Conta: {conta['numero_conta']} | 👤 Titular: {conta['usuario']}")


dados = {
    "saldo": 0,
    "extrato": [],
    "usuarios": [],
    "contas": [],
    "numero_saques": 0,
    "limite_saque": 500,
    "limite_saques_dia": 3
}

while True:
    menu()
    opcao = input("Escolha uma opção: ").strip()

    if opcao == "1":
        try:
            valor = float(input("Digite o valor do depósito: "))
            dados["saldo"], dados["extrato"] = deposito(dados["saldo"], valor, dados["extrato"])
        except ValueError:
            print("Entrada inválida. Digite um valor numérico.")

    elif opcao == "2":
        try:
            valor = float(input("Digite o valor do saque: "))
            dados["saldo"], dados["extrato"], dados["numero_saques"] = saque(
                saldo=dados["saldo"], valor=valor, extrato=dados["extrato"], 
                limite=dados["limite_saque"], numero_saques=dados["numero_saques"], limite_saques=dados["limite_saques_dia"]
            )
        except ValueError:
            print("Entrada inválida. Digite um valor numérico.")

    elif opcao == "3":
        exibir_extrato(dados["saldo"], extrato=dados["extrato"])

    elif opcao == "4":
        cadastrar_usuario(dados["usuarios"])

    elif opcao == "5":
        cadastrar_conta(dados["usuarios"], dados["contas"])

    elif opcao == "6":
        listar_contas(dados["contas"])

    elif opcao == "7":
        print("Obrigado por utilizar nosso sistema. Até mais!")
        break

    else:
        print("Opção inválida.")
