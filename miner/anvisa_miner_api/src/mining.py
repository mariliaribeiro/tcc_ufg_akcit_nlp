from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
import threading
import time
import sys
import os

# Adicionar o diretório pai ao path para importar os módulos de mineração
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from database import MongoDBConnection
from scraper import AnvisaScraper
from datetime import datetime
import logging

mining_bp = Blueprint('mining', __name__)

# Estado global da mineração
mining_state = {
    'is_running': False,
    'processed_count': 0,
    'target_count': 50,
    'current_medicine': None,
    'logs': [],
    'thread': None
}

class MiningLogger:
    def __init__(self):
        self.logs = []
    
    def log(self, level, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        self.logs.append(log_entry)
        mining_state['logs'] = self.logs[-100:]  # Manter apenas os últimos 100 logs
        print(log_entry)

mining_logger = MiningLogger()

def mining_worker():
    """Função que executa a mineração em thread separada"""
    try:
        db_connection = MongoDBConnection()
        scraper = AnvisaScraper()
        
        mining_logger.log("INFO", "Iniciando processo de mineração")
        mining_state['processed_count'] = db_connection.count_founded_medicines()
        
        while mining_state['is_running'] and mining_state['processed_count'] < mining_state['target_count']:
            medicines_to_process = db_connection.get_active_medicines_to_process()
            found_one_to_process = False
            
            for medicine in medicines_to_process:
                if not mining_state['is_running']:
                    break
                    
                found_one_to_process = True
                product_name = medicine.get("product_name")
                medicine_id = medicine.get("_id")
                
                mining_state['current_medicine'] = product_name
                
                if not product_name:
                    mining_logger.log("WARNING", f"Medicamento com ID {medicine_id} não possui product_name. Pulando.")
                    db_connection.update_medicine_data(medicine_id, {"founded": False, "processing_date": datetime.now()})
                    continue
                
                mining_logger.log("INFO", f"Processando medicamento: {product_name}")
                
                founded = False
                patient_leaflet_path = None
                professional_leaflet_path = None
                
                try:
                    if scraper.search_medicine(product_name):
                        leaflet_links = scraper.get_leaflet_links()
                        
                        if leaflet_links["professional_leaflet"]:
                            professional_leaflet_path = scraper.download_pdf(leaflet_links["professional_leaflet"], f"{product_name}_profissional.pdf")
                            mining_logger.log("INFO", f"Bula profissional baixada para {product_name}")
                            founded = True
                        
                        if leaflet_links["patient_leaflet"]:
                            patient_leaflet_path = scraper.download_pdf(leaflet_links["patient_leaflet"], f"{product_name}_paciente.pdf")
                            mining_logger.log("INFO", f"Bula paciente baixada para {product_name}")
                            if not founded:
                                founded = True
                    
                    update_data = {
                        "founded": founded,
                        "processing_date": datetime.now()
                    }
                    if patient_leaflet_path: 
                        update_data["patient_leaflet"] = patient_leaflet_path
                    if professional_leaflet_path: 
                        update_data["professional_leaflet"] = professional_leaflet_path
                    
                    db_connection.update_medicine_data(medicine_id, update_data)
                    
                    if founded:
                        mining_state['processed_count'] += 1
                        mining_logger.log("INFO", f"Bula(s) encontrada(s) para {product_name}. Total processado: {mining_state['processed_count']}")
                    else:
                        mining_logger.log("INFO", f"Nenhuma bula encontrada para {product_name}")
                
                except Exception as e:
                    mining_logger.log("ERROR", f"Erro ao processar {product_name}: {str(e)}")
                    db_connection.update_medicine_data(medicine_id, {"founded": False, "processing_date": datetime.now()})
                
                if mining_state['processed_count'] >= mining_state['target_count']:
                    break
                
                time.sleep(2)  # Intervalo entre requisições
            
            if not found_one_to_process:
                mining_logger.log("INFO", "Nenhum medicamento ativo encontrado para processar")
                break
        
        mining_state['is_running'] = False
        mining_state['current_medicine'] = None
        mining_logger.log("INFO", "Processo de mineração finalizado")
        
    except Exception as e:
        mining_logger.log("ERROR", f"Erro crítico na mineração: {str(e)}")
        mining_state['is_running'] = False
        mining_state['current_medicine'] = None

@mining_bp.route('/status', methods=['GET'])
@cross_origin()
def get_status():
    """Retorna o status atual da mineração"""
    return jsonify({
        'is_running': mining_state['is_running'],
        'processed_count': mining_state['processed_count'],
        'target_count': mining_state['target_count'],
        'current_medicine': mining_state['current_medicine'],
        'logs': mining_state['logs'][-20:]  # Últimos 20 logs
    })

@mining_bp.route('/start', methods=['POST'])
@cross_origin()
def start_mining():
    """Inicia o processo de mineração"""
    if mining_state['is_running']:
        return jsonify({'error': 'Mineração já está em execução'}), 400
    
    data = request.get_json() or {}
    mining_state['target_count'] = data.get('target_count', 50)
    
    mining_state['is_running'] = True
    mining_state['logs'] = []
    mining_state['thread'] = threading.Thread(target=mining_worker)
    mining_state['thread'].start()
    
    return jsonify({'message': 'Mineração iniciada com sucesso'})

@mining_bp.route('/stop', methods=['POST'])
@cross_origin()
def stop_mining():
    """Para o processo de mineração"""
    if not mining_state['is_running']:
        return jsonify({'error': 'Mineração não está em execução'}), 400
    
    mining_state['is_running'] = False
    mining_logger.log("INFO", "Parando mineração por solicitação do usuário")
    
    return jsonify({'message': 'Mineração parada com sucesso'})

@mining_bp.route('/logs', methods=['GET'])
@cross_origin()
def get_logs():
    """Retorna todos os logs da mineração"""
    return jsonify({'logs': mining_state['logs']})

@mining_bp.route('/results', methods=['GET'])
@cross_origin()
def get_results():
    """Retorna os resultados da mineração"""
    try:
        db_connection = MongoDBConnection()
        
        # Buscar medicamentos processados com sucesso
        found_medicines = list(db_connection.collection.find(
            {'founded': True},
            {'product_name': 1, 'patient_leaflet': 1, 'professional_leaflet': 1, 'processing_date': 1}
        ).limit(100))
        
        # Converter ObjectId para string
        for medicine in found_medicines:
            medicine['_id'] = str(medicine['_id'])
            if 'processing_date' in medicine:
                medicine['processing_date'] = medicine['processing_date'].isoformat()
        
        return jsonify({
            'total_found': len(found_medicines),
            'medicines': found_medicines
        })
    
    except Exception as e:
        return jsonify({'error': f'Erro ao buscar resultados: {str(e)}'}), 500

