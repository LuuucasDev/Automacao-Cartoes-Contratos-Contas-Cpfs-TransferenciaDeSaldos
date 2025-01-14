import json
import logging
from dotenv import load_dotenv
import os
import random
from gerar_cartao import GerarCartao
from transferir_saldo import TransferirSaldo

# Carregar variáveis de ambiente
load_dotenv()

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("automation.log"), logging.StreamHandler()]
)

# Configurações e constantes
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")
URL_LOGIN = os.getenv("URL_LOGIN")
URL_MENU = os.getenv("URL_MENU")
USUARIO = os.getenv("USUARIO")
SENHA = os.getenv("SENHA")
API_URL = os.getenv("API_URL")

def main():
    # Inicializar a classe de geração de cartões
    gerar_cartao = GerarCartao(CHROMEDRIVER_PATH, URL_LOGIN, URL_MENU, USUARIO, SENHA)

    # Gerar dados para os dois cartões (PAT e PJ)
    logging.info("Gerando cartões...")
    cartao_pj = gerar_cartao.gerar_cartao("PJ")
    cartao_pat = gerar_cartao.gerar_cartao("PAT")

    # Salvar os cartões gerados em arquivos
    with open("cartao_pj.txt", "w") as pj_file:
        json.dump(cartao_pj, pj_file, indent=4)
    with open("cartao_pat.txt", "w") as pat_file:
        json.dump(cartao_pat, pat_file, indent=4)

    logging.info("Cartões gerados e salvos com sucesso!")

    # Escolher aleatoriamente os cartões de origem e destino
    cartao_origem, cartao_destino = random.sample([cartao_pj, cartao_pat], 2)
    
    # Escolher um valor de transferência aleatório dentro do saldo do cartão de origem
    valor_transferencia = round(random.uniform(1.00, cartao_origem["saldo"]), 2)

    logging.info(f"Transferindo R${valor_transferencia} de {cartao_origem['numero_cartao']} para {cartao_destino['numero_cartao']}.")

    # Transferência de saldo entre cartões
    logging.info("Iniciando transferência de saldo...")
    transferir_saldo = TransferirSaldo(API_URL)
    response = transferir_saldo.transferir_saldo(cartao_origem, cartao_destino, valor_transferencia)

    # Salvar os saldos atualizados
    with open("cartao_pj_atualizado.txt", "w") as pj_atualizado:
        json.dump(response["cartao_destino"], pj_atualizado, indent=4)
    with open("cartao_pat_atualizado.txt", "w") as pat_atualizado:
        json.dump(response["cartao_origem"], pat_atualizado, indent=4)

    logging.info("Transferência concluída com sucesso!")

if __name__ == "__main__":
    main()
