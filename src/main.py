from typing import Any
from fastapi import FastAPI
import socketio
from config import settings
from routes import router as api_router
from socket_handlers import register_socket_handlers
from engineio.payload import Payload
Payload.max_decode_packets = 50

sio: Any = socketio.AsyncServer(async_mode="asgi")
register_socket_handlers(sio)
socket_app = socketio.ASGIApp(sio)

app = FastAPI()
app.include_router(api_router)

app.mount("/", socket_app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.backend_port)
