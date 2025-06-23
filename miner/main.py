from database import MongoDBConnection
from scraper import AnvisaScraper
import time
from datetime import datetime
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    db_connection = MongoDBConnection()
    scraper = AnvisaScraper()

    processed_count = db_connection.count_founded_medicines()
    logging.info(f"Iniciando o processamento. {processed_count} bulas já foram encontradas.")

    while processed_count < 50:
        medicines_to_process = db_connection.get_active_medicines_to_process()
        found_one_to_process = False
        for medicine in medicines_to_process:
            found_one_to_process = True
            product_name = medicine.get("product_name")
            medicine_id = medicine.get("_id")

            if not product_name:
                logging.warning(f"Medicamento com ID {medicine_id} não possui product_name. Pulando.")
                db_connection.update_medicine_data(medicine_id, {"founded": False, "processing_date": datetime.now()})
                continue

            logging.info(f"Processando medicamento: {product_name} (ID: {medicine_id})")
            
            founded = False
            patient_leaflet_path = None
            professional_leaflet_path = None

            try:
                if scraper.search_medicine(product_name):
                    leaflet_links = scraper.get_leaflet_links()
                    
                    if leaflet_links["professional_leaflet"]:
                        professional_leaflet_path = scraper.download_pdf(leaflet_links["professional_leaflet"], f"{product_name}_profissional.pdf")
                        logging.info(f"Bula profissional baixada para {product_name}: {professional_leaflet_path}")
                        founded = True
                    
                    if leaflet_links["patient_leaflet"] and not founded: # Baixa a de paciente se a profissional não foi encontrada
                        patient_leaflet_path = scraper.download_pdf(leaflet_links["patient_leaflet"], f"{product_name}_paciente.pdf")
                        logging.info(f"Bula paciente baixada para {product_name}: {patient_leaflet_path}")
                        founded = True
                    elif leaflet_links["patient_leaflet"] and founded: # Se a profissional foi encontrada, baixa a de paciente também
                        patient_leaflet_path = scraper.download_pdf(leaflet_links["patient_leaflet"], f"{product_name}_paciente.pdf")
                        logging.info(f"Bula paciente baixada para {product_name}: {patient_leaflet_path}")

                update_data = {
                    "founded": founded,
                    "processing_date": datetime.now()
                }
                if patient_leaflet_path: update_data["patient_leaflet"] = patient_leaflet_path
                if professional_leaflet_path: update_data["professional_leaflet"] = professional_leaflet_path

                db_connection.update_medicine_data(medicine_id, update_data)
                if founded:
                    processed_count += 1
                    logging.info(f"Bula(s) encontrada(s) e dados atualizados para {product_name}. Total processado: {processed_count}")
                else:
                    logging.info(f"Nenhuma bula encontrada para {product_name}.")

            except Exception as e:
                logging.error(f"Erro ao processar {product_name} (ID: {medicine_id}): {e}")
                db_connection.update_medicine_data(medicine_id, {"founded": False, "processing_date": datetime.now()})
            
            if processed_count >= 50:
                break

            time.sleep(random.uniform(1, 3)) # Intervalo entre as requisições
        
        if not found_one_to_process:
            logging.info("Nenhum medicamento ativo com 'founded=false' ou inexistente encontrado. Encerrando.")
            break

    logging.info("Processamento concluído ou limite de 50 bulas atingido.")

if __name__ == "__main__":
    main()


