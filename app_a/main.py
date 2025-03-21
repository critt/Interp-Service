from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from firebase_admin import auth
from config import settings
import requests

app = FastAPI()


class WebSocketRequest(BaseModel):
    user_id: str
    session_id: str


@app.post("/start-websocket-session")
def start_websocket_session(request: WebSocketRequest):
    # Authenticate user with Firebase
    try:
        user = auth.get_user(request.user_id)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Assign an App B instance (or spin up if necessary)
    app_b_url = assign_app_b_instance(request.session_id)

    return {"websocket_url": app_b_url}


def assign_app_b_instance(session_id: str) -> str:
    # Logic to assign an App B instance (e.g., from a pool or Kubernetes service)
    # For now, return a placeholder URL
    return f"ws://app-b-service/{session_id}"
