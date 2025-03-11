import firebase_admin
from firebase_admin import credentials, auth, exceptions as firebase_exceptions
from config import settings

cred = credentials.Certificate(settings.google_service_json_file)
firebase_admin.initialize_app(cred)


def verify_token(token: str):
    try:
        return auth.verify_id_token(token)
    except firebase_exceptions.FirebaseError as fbe:
        print(f"Unauthorized: Invalid token: {fbe}", flush=True)
        return None
    except (KeyError, TypeError) as e:
        print(f"Unauthorized: missing token: {e}", flush=True)
        return None
