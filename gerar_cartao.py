import random
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class GerarCartao:
    def __init__(self, chromedriver_path, url_login, url_menu, usuario, senha):
        self.chromedriver_path = chromedriver_path
        self.url_login = url_login
        self.url_menu = url_menu
        self.usuario = usuario
        self.senha = senha

    def _gerar_dados_cartao(self, tipo):
        """Gera dados aleatórios para um cartão."""
        return {
            "tipo": tipo,
            "numero_cartao": "".join([str(random.randint(0, 9)) for _ in range(16)]),
            "conta": str(random.randint(100000, 999999)),
            "cpf": "34304437682",
            "contrato": "123479",
            "empresa": "18744523000108",
            "saldo": 190.00
        }

    def _realizar_login(self, driver):
        """Realiza login no site FVS."""
        logging.info("Realizando login no site FVS.")
        driver.get(self.url_login)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "txtLogin")))

        driver.find_element(By.ID, "txtLogin").send_keys(self.usuario)
        driver.find_element(By.ID, "txtSenha").send_keys(self.senha)
        driver.find_element(By.ID, "btnLogin").click()

        WebDriverWait(driver, 10).until(EC.url_to_be(self.url_menu))
        logging.info("Login realizado com sucesso!")

    def gerar_cartao(self, tipo):
        """Gera um cartão do tipo especificado."""
        logging.info(f"Iniciando geração de cartão do tipo {tipo}.")
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        service = Service(self.chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        try:
            self._realizar_login(driver)
            driver.get(self.url_menu)

            # Gera dados do cartão
            dados_cartao = self._gerar_dados_cartao(tipo)

            # Simula o preenchimento no site
            driver.find_element(By.ID, "campo_tipo").send_keys(dados_cartao["tipo"])
            driver.find_element(By.ID, "campo_numero_cartao").send_keys(dados_cartao["numero_cartao"])
            driver.find_element(By.ID, "campo_conta").send_keys(dados_cartao["conta"])
            driver.find_element(By.ID, "campo_cpf").send_keys(dados_cartao["cpf"])
            driver.find_element(By.ID, "campo_contrato").send_keys(dados_cartao["contrato"])
            driver.find_element(By.ID, "campo_empresa").send_keys(dados_cartao["empresa"])
            driver.find_element(By.ID, "campo_saldo").send_keys(str(dados_cartao["saldo"]))

            driver.find_element(By.ID, "botao_submit").click()

            WebDriverWait(driver, 10).until(EC.alert_is_present())
            driver.switch_to.alert.accept()

            logging.info(f"Cartão {tipo} gerado com sucesso!")
            return dados_cartao

        except Exception as e:
            logging.error(f"Erro ao gerar cartão do tipo {tipo}: {e}")
            raise

        finally:
            driver.quit()
