import asyncio
import queue
import sys
import threading
from typing import Dict

from google.cloud import speech
from google.cloud import translate_v2 as translate

from config import settings

clients = {}

class ClientData:
    def __init__(self, transcribe_thread, conn, config: Dict, namespace: str):
        self._buff = queue.Queue()
        self._thread = transcribe_thread
        self._closed = True
        self._conn = conn
        self.general_config = {dict_key: config[dict_key] for dict_key in config if dict_key != 'audio'}
        self.audio_config = config['audio']
        self.namespace = namespace

    async def close(self):
        self._closed = True
        self._buff.put(None)
        self._thread.join()
        await self._conn.emit('endGoogleCloudStream', '')

    def start_audio_stream(self):
        self._closed = False
        self._thread.start()

    def add_audio_data(self, data):
        self._buff.put(data)

    def generator(self):
        while not self._closed:
            chunk = self._buff.get()
            if chunk is None:
                return

            data = [chunk]

            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b"".join(data)

    async def send_client_data(self, data, is_final: bool):
        await self._conn.emit('speechData', {'data': data, 'isFinal': is_final}, namespace=self.namespace)


async def listen_translate_loop(responses, client: ClientData, translate_client: translate.Client, translate_language: str):
    num_chars_printed = 0
    interim_flush_counter = 0
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript

        overwrite_chars = " " * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + "\r")
            sys.stdout.flush()
            interim_flush_counter += 1

            if client and interim_flush_counter % 3 == 0:
                interim_flush_counter = 0
                await client.send_client_data(transcript + overwrite_chars + "\r", False)

            num_chars_printed = len(transcript)
        else:
            text = transcript + overwrite_chars
            print(text)
            
            translationResult = translate_client.translate(text, target_language=translate_language)
            
            print('Text: {}'.format(translationResult['input']))
            print('Translation: {}'.format(translationResult['translatedText']))
            print('Detected source language: {}'.format(translationResult['detectedSourceLanguage']))

            if client:
                await client.send_client_data(translationResult['translatedText'], True)

            num_chars_printed = 0


class GCPService:
    encoding_map = {'LINEAR16': speech.RecognitionConfig.AudioEncoding.LINEAR16}

    @staticmethod
    async def start_listen(client_id: str):
        client = clients[client_id]
        
        speech_client = speech.SpeechClient.from_service_account_json(settings.google_service_json_file)
        translate_client = translate.Client.from_service_account_json(settings.google_service_json_file)
        
        config = speech.RecognitionConfig(encoding=GCPService.encoding_map[client.audio_config['encoding']], sample_rate_hertz=client.audio_config['sampleRateHertz'],
                                          language_code=client.audio_config['languageCode'], enable_automatic_punctuation=True)
        
        streaming_config = speech.StreamingRecognitionConfig(config=config, interim_results=client.general_config['interimResults'])

        audio_generator = client.generator()
        requests = (speech.StreamingRecognizeRequest(audio_content=content) for content in audio_generator)
        responses = speech_client.streaming_recognize(streaming_config, requests)
        
        await listen_translate_loop(responses, client, translate_client, client.general_config['targetLanguage'])

    @staticmethod
    async def start_stream(sio, client_id: str, config: Dict, namespace: str):
        if client_id not in clients:
            clients[client_id] = ClientData(threading.Thread(target=asyncio.run, args=(GCPService.start_listen(client_id),)), sio, config, namespace=namespace)
            clients[client_id].start_audio_stream()
        else:
            print('Warning - already running transcription for client')

    @staticmethod
    async def stop_stream(client_id: str):
        if client_id in clients:
            await clients[client_id].close()
            del clients[client_id]

    @staticmethod
    def add_audio_data(client_id: str, data):
        if client_id not in clients:
            return

        clients[client_id].add_audio_data(data)
    
    @staticmethod
    def detect_language(text: str):
        translate_client = translate.Client.from_service_account_json(settings.google_service_json_file)
        return translate_client.detect_language(text)
    
    @staticmethod
    def get_supported_languages():
        translate_client = translate.Client.from_service_account_json(settings.google_service_json_file)
        return translate_client.get_languages()
