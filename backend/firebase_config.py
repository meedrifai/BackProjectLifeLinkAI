# firebase_config.py

import os
import json
import tempfile
import firebase_admin
from firebase_admin import credentials

def initialize_firebase():
    """Initialize Firebase using raw JSON credentials from environment variable"""
    
    # Récupérer les credentials depuis la variable d'environnement
    creds_json = os.environ.get("FIREBASE_CREDENTIALS")
    
    if not creds_json:
        raise ValueError("La variable d'environnement FIREBASE_CREDENTIALS est manquante")
    
    try:
        # Valider que c'est du JSON valide
        creds_dict = json.loads(creds_json)
        print(f"Firebase project ID: {creds_dict.get('project_id', 'N/A')}")
        
        # Créer un fichier temporaire pour les credentials
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".json") as f:
            f.write(creds_json)
            f.flush()
            firebase_cred_file = f.name
        
        # Initialiser Firebase si ce n'est pas déjà fait
        if not firebase_admin._apps:
            cred = credentials.Certificate(firebase_cred_file)
            firebase_admin.initialize_app(cred, {
                "databaseURL": "https://blood-3fda1-default-rtdb.firebaseio.com/"
            })
            print("Firebase Admin SDK initialized successfully!")
        
        # Nettoyer le fichier temporaire
        os.unlink(firebase_cred_file)
        
    except json.JSONDecodeError as e:
        raise ValueError(f"FIREBASE_CREDENTIALS n'est pas du JSON valide: {e}")
    except Exception as e:
        raise ValueError(f"Erreur lors de l'initialisation de Firebase: {e}")

# Initialiser Firebase au chargement du module
initialize_firebase()