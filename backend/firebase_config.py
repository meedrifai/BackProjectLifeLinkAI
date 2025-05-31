import os
import json
import tempfile
import base64
import firebase_admin
from firebase_admin import credentials

def initialize_firebase():
    """Initialise Firebase Admin SDK avec les credentials encodés en base64 dans la variable d'environnement FIREBASE_CREDENTIALS_BASE64."""

    encoded_creds = os.environ.get("FIREBASE_CREDENTIALS_BASE64")
    if not encoded_creds:
        raise ValueError("La variable d'environnement FIREBASE_CREDENTIALS_BASE64 est manquante.")

    try:
        # Décoder la chaîne base64 en JSON string
        creds_json = base64.b64decode(encoded_creds).decode('utf-8')

        # Vérifier que c'est un JSON valide
        creds_dict = json.loads(creds_json)
        project_id = creds_dict.get('project_id', 'N/A')
        print(f"Firebase project ID détecté : {project_id}")

        # Si Firebase n'est pas déjà initialisé
        if not firebase_admin._apps:
            # Écrire temporairement les credentials dans un fichier
            with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".json") as f:
                f.write(creds_json)
                firebase_cred_file = f.name

            try:
                cred = credentials.Certificate(firebase_cred_file)
                firebase_admin.initialize_app(cred, {
                    "databaseURL": f"https://{project_id}-default-rtdb.firebaseio.com/"
                })
                print("Firebase Admin SDK initialisé avec succès !")
            finally:
                # Supprimer le fichier temporaire même en cas d'erreur
                os.unlink(firebase_cred_file)
        else:
            print("Firebase Admin SDK est déjà initialisé.")

    except json.JSONDecodeError as e:
        raise ValueError(f"Le contenu décodé n'est pas un JSON valide : {e}")
    except Exception as e:
        raise ValueError(f"Erreur lors de l'initialisation de Firebase : {e}")
