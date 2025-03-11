from typing import Any
from fastapi import FastAPI
import socketio
from config import settings
from routes import router as api_router
from socket_handlers import register_socket_handlers
from gcp_service import GCPService
from engineio.payload import Payload

Payload.max_decode_packets = 50

sio: Any = socketio.AsyncServer(async_mode="asgi")
gcp_service = GCPService()
register_socket_handlers(sio, gcp_service)
socket_app = socketio.ASGIApp(sio)

app = FastAPI()
app.include_router(api_router)

app.mount("/", socket_app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.backend_port,
        timeout_keep_alive=0,
        http="httptools",
        reload=True,
    )
