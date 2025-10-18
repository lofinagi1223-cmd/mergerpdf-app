import firebase_admin
from firebase_admin import credentials, firestore
import datetime
import json
import os

class Database:
    _instance = None  # Singleton

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._init_firebase()
        return cls._instance

    def _init_firebase(self):
        if not firebase_admin._apps:
            cred_info = json.loads(os.environ["FIREBASE_KEY"])
            cred = credentials.Certificate(cred_info)
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()

        # Usuários pré-definidos (modo temporário)
        self.USERS = {
            "admin": {"email": "admin@certo.com", "senha": "1234"},
            "rafael": {"email": "rafael@certo.com", "senha": "abcd"},
        }

    # ------------------------------
    # Métodos (ações do banco)
    # ------------------------------
    def validar_usuario(self, email, senha):
        """Valida o usuário com base na lista local"""
        for nome, info in self.USERS.items():
            if info["email"] == email and info["senha"] == senha:
                return True, nome
        return False, None

    def registrar_login(self, email):
        """Salva no Firestore o registro do login"""
        self.db.collection("logins").add({
            "email": email,
            "data": datetime.datetime.now()
        })

    def registrar_merge(self, usuario, arquivos_selecionados):
        """Registra no Firestore o evento de mesclagem"""
        self.db.collection("pdfs").add({
            "usuario": usuario,
            "data_upload": datetime.datetime.now(),
            "arquivos_selecionados": arquivos_selecionados
        })
