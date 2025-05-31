# firebase_config.py

import os
import base64
import tempfile
import firebase_admin
from firebase_admin import credentials

# Charger les credentials depuis la variable d’environnement encodée en base64
creds_b64 = os.environ.get("GOOGLE_CREDS_BASE64")
if not creds_b64:
    raise ValueError("La variable d’environnement GOOGLE_CREDS_BASE64 est manquante")

# Décoder et écrire dans un fichier temporaire
creds_json = base64.b64decode(creds_b64).decode("utf-8")
with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".json") as f:
    f.write(creds_json)
    f.flush()
    firebase_cred_file = f.name

# Initialiser Firebase avec l’URL de ta base de données
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_cred_file)
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://blood-3fda1-default-rtdb.firebaseio.com/"
    })
