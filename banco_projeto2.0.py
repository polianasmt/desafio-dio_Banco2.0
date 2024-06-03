"""
Deposito, saque, extrato, criar usuario e conta corrente
"""
import os
import sys

def validar_cpf(cpf_validar):
        
        global cpf_falso
        cpf_falso = True

        nove_digitos = cpf_validar[:9]
        dez_digitos = cpf_validar[:10]

        contagem_regressiva_1 = 10
        contagem_regressiva_2 = 11

        resultados_1 = 0
        resultados_2 = 0

        for digito in nove_digitos:
            resultados_1 += int(digito) * contagem_regressiva_1
            contagem_regressiva_1 -= 1
    
        digito_1 = (resultados_1 * 10) % 11
        comparacao_1 = digito_1 if digito_1 <= 9 else 0

        for digito_2 in dez_digitos:
            resultados_2 += int(digito_2) * contagem_regressiva_2
            contagem_regressiva_2 -= 1

        digito_2 = (resultados_2 * 10) % 11
        comparacao_2 = digito_2 if digito_2 <= 9 else 0

        cpf_gerado = f'{nove_digitos}{digito_1}{digito_2}'

        if cpf_validar != cpf_gerado:
            cpf_falso = False
            print("\nO cpf '{}' não é valido.".format(cpf_validar))


def criar_usuario(usuarios):

    os.system('cls')
    nome = input("Nome: ")
    data_nasc = input("Data de nascimento: ")

    while(True):
        cpf = input("CPF: ")
        usuario = filtrar_usuario(cpf, usuarios)
        validar_cpf(cpf)

        if cpf_falso == True:
            break

    print("\nEndereço - Logradouro, número, bairro, cidade/sigla estado")
    logradouro = input("\tLogradouro: ")
    numero_casa = input("\tNúmero: ")
    bairro = input("\tBairro: ")
    cidade_sigla = input("\tCidade/sigla estado: ")
    
    usuarios.append({"nome": nome, "data_nasc": data_nasc, "cpf": cpf, "endereco": [logradouro, numero_casa, bairro, cidade_sigla]})

    os.system('cls')
    print("Usuário criado com sucesso.")

    return usuarios

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def iniciar_conta(usuarios):
    os.system('cls')
    cpf_conta = input("Insira o CPF: ")
    usuario = filtrar_usuario(cpf_conta, usuarios)
    global usuario_encontrado 

    if usuario:
        usuario_encontrado = True
        os.system('cls')
        print(f"Bem vindo(a) {usuario['nome']}")
        menu_usuario()
    else:
        os.system('cls')
        usuario_encontrado = False
        print("Usuário não encontrado.")
        menu_conta()

def menu_usuario():
    menu = """
    MENU DO USUÁRIO
    [1] Depósito
    [2] Saque
    [3] Extrato
    [4] Sair da conta
    """
    print(menu)     
    
def criar_conta_corrente(agencia, numero_conta, usuarios):
    os.system('cls')
    cpf = input("Insira o CPF: ")
    usuarios = filtrar_usuario(cpf, usuarios)

    if usuarios:
        os.system('cls')
        print("Conta corrente criada com sucesso.")
        contas = {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuarios}
    else:
        print("Usuario não encontrado.")

    return contas

def listar_usuarios(usuarios):
    os.system('cls')
    print("#" * 10, "Usuarios", "#" * 10)
    if not usuarios:
        os.system('cls')
        print("Nenhum usuario cadastrado.")
    else:
        for usuario in usuarios:
            print(f"{usuario['nome']} - {usuario['cpf']}")


def listar_contas(contas):
    for conta in contas:
        os.system('cls')
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 10)
def menu_conta():
    menu = """
    MENU 
    [1] Novo usuário
    [2] Nova conta
    [3] Entrar 
    [4] Listar contas
    [5] Listar usuarios
    [6] Sair
    """
    print(menu)
    
def exibir_extrato(saldo ,/,*, extrato):
    os.system('cls')
    print("#" * 10, "Extrato", "#" * 10)
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")


def saque(*, saldo, valor, extrato, limite, numero_saque, limite_saques):

    #excedeu_limite_de_saque = numero_saques > limite_saques
    excedeu_limite_valor = valor > limite
    
    if valor > saldo:
        os.system('cls')
        print("Não foi possivel realizar o saque por falta de saldo.")

    elif excedeu_limite_valor:
        os.system('cls')
        print(f"O limite para sacar é de até R$ {limite}.")
            
    elif numero_saque >= limite_saques:
        os.system('cls')
        print("Não foi possivel realizar o saque pois excedeu o limite diario de saques.")
    
    else:
        os.system('cls')
        print(f"O saque de R$ {valor} foi realizado com sucesso.")
        numero_saque += 1
        extrato += f"\nSaque: R$ {valor:.2f}."
        saldo -= valor

    return saldo, extrato, numero_saque


def deposito(saldo, valor, extrato, /):

    if valor < 0:
        os.system('cls')
        print("O valor não pode ser negativo.")
    else:
        os.system('cls')
        saldo += valor
        extrato += f"\nDeposito: R$ {valor:.2f}."
        print(f"O valor de R$ {valor:.2f} foi depositado com sucesso.")

    return saldo, extrato


def main():

    LIMITE_SAQUES_DIARIOS = 3
    AGENCIA = "0001"

    saldo = 0
    limite_saque = 500
    extrato = ""
    numero_saques = 0
    usuario = []
    contas = []
    opcoes_validas = ['1', '2', '3', '4', '5']

    while(True):
        apresentar_menu = menu_conta()
        escolha = input(f"\nEscolha: ")

        if escolha not in opcoes_validas:
            os.system('cls')
            print("Opção inválida.")

        if escolha == '1': #novo usuario
            criar_usuario(usuario)

        elif escolha == '2': #nova conta
            numero_conta = len(contas) + 1
            conta = criar_conta_corrente(AGENCIA, numero_conta, usuario)

            if conta:
                contas.append(conta)
    
        if escolha == '3':
            iniciar_conta(usuario)

            while(True):
                opcao = input("Escolha: ")

                if usuario_encontrado:
                    if opcao == '1':
                        valor_deposito = float(input("Entre com o valor do depósito R$ "))
                        saldo, extrato = deposito(saldo, valor_deposito, extrato)
                        menu_usuario()
                        
                    if opcao == '2':
                        valor_saque = float(input("\nEntre com o valor a ser sacado R$ "))
                        saldo, extrato, numero_saques = saque(saldo=saldo, valor=valor_saque, extrato=extrato, limite=limite_saque, numero_saque=numero_saques, limite_saques=LIMITE_SAQUES_DIARIOS)
                        menu_usuario()

                    if opcao == '3':
                        exibir_extrato(saldo, extrato=extrato)
                        menu_usuario()
                
                    if opcao == '4':
                        os.system('cls')
                        break
                else:
                    iniciar_conta(usuario)


        if escolha == '4': #listar contas
            listar_contas(contas)

        if escolha == '5':
            listar_usuarios(usuario)

        continue

   

        # elif escolha == '7':
        #     sys.exit(0)
        
        # else:
        #     os.system('cls')
        #     print("Opção invalida.")


main()