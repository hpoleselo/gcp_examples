import firebase_admin
from firebase_admin import firestore
import logging

firebase_admin.initialize_app()
db = firestore.client()

def write_json(request):
    from datetime import datetime
    import names
    import random
    import json

    json_data = {
        'name': names.get_full_name(),
        'age': random.randint(1,100),
        'metrics': {
            'perfomance1' : 0.86,
            'perfomance2' : 0.99,
            'perfomance3' : 1340
        } 
    }

    try:
        ref = db.collection('json_files').document()
        # Based on the collection, we're referencing the fields we created on the database 
        logging.debug(f'Dumping {json_data} to Firestore...')
        ref.set(json_data)
        return 'File has been written to Firestore', 200
    except Exception as e:
        logging.error("Could not write to Firestore, error:")
        return e, 400