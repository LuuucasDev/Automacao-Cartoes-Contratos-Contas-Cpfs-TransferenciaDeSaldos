import random
import json
import os

# Função para gerar CPF aleatório
def gerar_cpf():
    def calc_digitos(cpf):
        soma = sum((10 - i) * int(v) for i, v in enumerate(cpf[:9]))
        d1 = (soma * 10 % 11) % 10
        soma = sum((11 - i) * int(v) for i, v in enumerate(cpf[:9] + str(d1)))
        d2 = (soma * 10 % 11) % 10
        return f"{d1}{d2}"

    cpf_base = "".join([str(random.randint(0, 9)) for _ in range(9)])
    return cpf_base + calc_digitos(cpf_base)

# Função para gerar CNPJ aleatório
def gerar_cnpj():
    def calc_digitos(cnpj):
        pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        pesos2 = [6] + pesos1
        soma1 = sum(x * int(y) for x, y in zip(pesos1, cnpj[:12]))
        d1 = 11 - soma1 % 11
        d1 = d1 if d1 < 10 else 0
        soma2 = sum(x * int(y) for x, y in zip(pesos2, cnpj[:12] + [d1]))
        d2 = 11 - soma2 % 11
        d2 = d2 if d2 < 10 else 0
        return [d1, d2]

    base = [random.randint(0, 9) for _ in range(8)] + [0, 0, 0, 1]
    digitos = calc_digitos(base)
    return "".join(map(str, base + digitos))

# Função para gerar número de cartão aleatório (16 dígitos)
def gerar_numero_cartao():
    return "".join([str(random.randint(0, 9)) for _ in range(16)])

# Função para gerar contrato aleatório (com base fixa e últimos dois números variáveis)
def gerar_contrato(base_contrato):
    ultimos_dois = random.randint(10, 99)
    return f"{base_contrato[:-2]}{ultimos_dois}"

# Função para gerar conta aleatória (somente números)
def gerar_conta():
    return f"{random.randint(100000, 999999)}"

# Função para gerar saldo aleatório
def gerar_saldo():
    return round(random.uniform(0, 1000), 2)

# Função para transferir saldo de um cartão para outro
def transferir_saldo(cartao_origem, cartao_destino, valor_transferencia):
    if cartao_origem["saldo"] >= valor_transferencia:
        cartao_origem["saldo"] -= valor_transferencia
        cartao_destino["saldo"] += valor_transferencia
        return True
    else:
        return False

# Função para carregar os dados do arquivo
def carregar_dados_arquivo(arquivo):
    if os.path.exists(arquivo):
        with open(arquivo, "r") as f:
            return json.load(f)
    else:
        return {"cartoes": []}

# Função para salvar os dados no arquivo
def salvar_dados_arquivo(dados, arquivo):
    with open(arquivo, "w") as f:
        json.dump(dados, f, indent=4)

# Função para mostrar os saldos
def exibir_saldos(dados):
    for cartao in dados["cartoes"]:
        print(f"Tipo: {cartao['tipo']}, Saldo: R${cartao['saldo']:.2f}")

# Arquivo onde os dados serão salvos
arquivo = "cartoes_dados.txt"

# Carregar os dados dos cartões do arquivo
dados = carregar_dados_arquivo(arquivo)

# Exibir os saldos dos cartões
print("Saldos atuais dos cartões:")
exibir_saldos(dados)

# Solicitar ao usuário o cartão de origem e o valor da transferência
cartao_origem_tipo = input("Digite o tipo do cartão de origem (refeicao/alimentacao): ").strip().lower()
cartao_destino_tipo = input("Digite o tipo do cartão de destino (refeicao/alimentacao): ").strip().lower()
valor_transferencia = float(input("Digite o valor a ser transferido: R$"))

# Encontrar os cartões de origem e destino
cartao_origem = next((cartao for cartao in dados["cartoes"] if cartao["tipo"] == cartao_origem_tipo), None)
cartao_destino = next((cartao for cartao in dados["cartoes"] if cartao["tipo"] == cartao_destino_tipo), None)

# Verificar se os cartões existem
if cartao_origem and cartao_destino:
    sucesso = transferir_saldo(cartao_origem, cartao_destino, valor_transferencia)
    if sucesso:
        salvar_dados_arquivo(dados, arquivo)
        print(f"Transferência de R${valor_transferencia:.2f} realizada com sucesso!")
        print(f"Novo saldo do cartão {cartao_origem['tipo']}: R${cartao_origem['saldo']:.2f}")
        print(f"Novo saldo do cartão {cartao_destino['tipo']}: R${cartao_destino['saldo']:.2f}")
    else:
        print("Saldo insuficiente para a transferência.")
else:
    print("Cartão de origem ou destino não encontrado.")

