from pymongo import MongoClient

class MongoDBConnection:
    def __init__(self, db_name='tcc_ufg_akcit_nlp', collection_name='drugs', host='localhost', port=27017):
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def get_active_medicines_to_process(self):
        # Seleciona medicamentos com registration_status = "Ativo" e founded = false ou founded inexistente.
        return self.collection.find({
            'registration_status': 'Ativo',
            '$or': [
                {'founded': False},
                {'founded': {'$exists': False}}
            ]
        })

    def update_medicine_data(self, medicine_id, update_data):
        self.collection.update_one({'_id': medicine_id}, {'$set': update_data})

    def count_founded_medicines(self):
        return self.collection.count_documents({'founded': True})


