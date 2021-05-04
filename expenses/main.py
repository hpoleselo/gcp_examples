import firebase_admin
from firebase_admin import firestore

# In order to use firestore, we have to add a .env file which contains the google-credentials.json
# That we downloaded in


firebase_admin.initialize_app()
db = firestore.client()

def set_expense(request):
    from datetime import datetime
    import random
    try:
        # Name of the collection referenced
        ref = db.collection('expenses').document()
        # Based on the collection, we're referencing the fields we created on the database 
        ref.set({'createdAt': datetime.now() ,'expense': random.randint(1,200)})
        return 200
    except Exception as e:
        return e, 400