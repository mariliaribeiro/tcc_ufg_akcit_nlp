from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class AnvisaScraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.base_url = "https://consultas.anvisa.gov.br/#/bulario"

    def __del__(self):
        self.driver.quit()




from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import os

class AnvisaScraper(object):
    # ... (código existente)

    def search_medicine(self, product_name):
        self.driver.get(self.base_url)
        wait = WebDriverWait(self.driver, 10)

        # Preencher o campo "Medicamento"
        medicine_input = wait.until(EC.presence_of_element_located((By.ID, "txtMedicamento")))
        medicine_input.send_keys(product_name)

        # Clicar no botão "Consultar"
        consult_button = wait.until(EC.element_to_be_clickable((By.ID, "btnConsultar")))
        consult_button.click()

        # Aguardar o carregamento da página de resultados
        time.sleep(random.uniform(1, 3)) # Espera aleatória para evitar bloqueios

        # Verificar se há resultados
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, "//table[@id=\'resultadoBulario\']/tbody/tr")))
            return True
        except:
            return False

    def get_leaflet_links(self):
        wait = WebDriverWait(self.driver, 10)
        try:
            # Selecionar a primeira linha disponível
            first_row = wait.until(EC.presence_of_element_located((By.XPATH, "//table[@id=\'resultadoBulario\']/tbody/tr[1]")))
            first_row.click()

            # Aguardar o carregamento do grid de detalhes
            time.sleep(random.uniform(1, 3))

            # Identificar os links das bulas
            patient_leaflet_link = None
            professional_leaflet_link = None

            # Tentar encontrar a bula para o profissional primeiro
            try:
                professional_leaflet_element = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), \'Bula para o Profissional\')]")))
                professional_leaflet_link = professional_leaflet_element.get_attribute("href")
            except:
                pass

            # Tentar encontrar a bula para o paciente
            try:
                patient_leaflet_element = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), \'Bula para o Paciente\')]")))
                patient_leaflet_link = patient_leaflet_element.get_attribute("href")
            except:
                pass

            return {
                "patient_leaflet": patient_leaflet_link,
                "professional_leaflet": professional_leaflet_link
            }
        except:
            return {"patient_leaflet": None, "professional_leaflet": None}

    def download_pdf(self, url, filename, download_dir="C:/tcc/data"):
        if not url:
            return None

        os.makedirs(download_dir, exist_ok=True)
        filepath = os.path.join(download_dir, filename)

        # Selenium não baixa diretamente, então usaremos requests
        # No ambiente real, o Selenium pode ser configurado para baixar automaticamente
        # Para este ambiente simulado, vamos apenas retornar o caminho como se tivesse baixado
        # Em um ambiente real, você faria algo como:
        # response = requests.get(url, stream=True)
        # with open(filepath, 'wb') as pdf_file:
        #     for chunk in response.iter_content(chunk_size=1024):
        #         if chunk:
        #             pdf_file.write(chunk)

        # Simula o download salvando um arquivo vazio com o nome correto
        with open(filepath, 'w') as f:
            f.write("")

        return filepath


