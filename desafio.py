def exibir_menu():
    print("\n### MENU ###")
    print("1 - Depositar")
    print("2 - Sacar")
    print("3 - Extrato")
    print("4 - Sair")


saldo = 0
transacoes = []
saques_realizados = 0
LIMITE_SAQUE = 3
LIMITE_SAQUE_VALOR = 500

while True:
    exibir_menu()
    escolha = input("Selecione uma opção: ").strip()

    if escolha == "1":
        valor = input("Informe o valor do depósito: ").strip()
        
        if valor.replace(".", "").isdigit():
            valor = float(valor)
            if valor > 0:
                saldo += valor
                transacoes.append(f"Depósito: +R$ {valor:.2f}")
                print("Depósito efetuado com sucesso.")
            else:
                print("O valor do depósito deve ser positivo.")
        else:
            print("Entrada inválida. Tente novamente.")

    elif escolha == "2":
        if saques_realizados < LIMITE_SAQUE:
            valor = input("Informe o valor do saque: ").strip()
            
            if valor.replace(".", "").isdigit():
                valor = float(valor)
                if valor > saldo:
                    print("Saldo insuficiente.")
                elif valor > LIMITE_SAQUE_VALOR:
                    print(f"Valor máximo para saque: R$ {LIMITE_SAQUE_VALOR:.2f}")
                elif valor > 0:
                    saldo -= valor
                    saques_realizados += 1
                    transacoes.append(f"Saque: -R$ {valor:.2f}")
                    print("Saque realizado com sucesso.")
                else:
                    print("O valor do saque deve ser positivo.")
            else:
                print("Entrada inválida. Tente novamente.")
        else:
            print("Limite de saques diários atingido.")

    elif escolha == "3":
        print("\n### EXTRATO ###")
        if transacoes:
            for t in transacoes:
                print(t)
        else:
            print("Nenhuma movimentação registrada.")
        print(f"Saldo atual: R$ {saldo:.2f}")

    elif escolha == "4":
        print("Obrigado por utilizar nossos serviços.")
        break

    else:
        print("Opção inválida. Escolha uma opção do menu.")
