# firebase_config.py
import firebase_admin
from firebase_admin import credentials

# Charger les credentials depuis le fichier JSON
cred = credentials.Certificate("credentials.json")

# Initialiser l'application Firebase avec les credentials et l'URL de la base de données
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://blood-3fda1-default-rtdb.firebaseio.com/"
})
