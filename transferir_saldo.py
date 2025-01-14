import logging
import requests

class TransferirSaldo:
    def __init__(self, api_url):
        self.api_url = api_url

    def transferir_saldo(self, cartao_origem, cartao_destino, valor):
        """Realiza a transferência de saldo entre dois cartões."""
        logging.info(f"Iniciando transferência de R${valor} de {cartao_origem['numero_cartao']} para {cartao_destino['numero_cartao']}.")
        payload = {
            "cartao_origem": {
                "numero": cartao_origem["numero_cartao"],
                "saldo": cartao_origem["saldo"]
            },
            "cartao_destino": {
                "numero": cartao_destino["numero_cartao"],
                "saldo": cartao_destino["saldo"]
            },
            "valor": valor
        }

        try:
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            logging.info("Transferência realizada com sucesso!")
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro na transferência: {e}")
            raise