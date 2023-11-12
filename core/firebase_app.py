from firebase_admin import credentials, initialize_app

cred = credentials.Certificate("credentials.json")
firebase_app = initialize_app(cred)
