from typing import Dict


class IStreamingService:
    async def start_stream(self, sio, client_id: str, config: Dict, namespace: str):
        raise NotImplementedError

    async def stop_stream(self, client_id: str):
        raise NotImplementedError

    def add_audio_data(self, client_id: str, data):
        raise NotImplementedError

    def detect_language(self, text: str):
        raise NotImplementedError

    def get_supported_languages(self):
        raise NotImplementedError
