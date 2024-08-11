import logging
from speech_recognition import Recognizer
from multiprocessing import Queue

class Transcriptor:
    def __init__(self, logger, queue):
        self.recognizer = Recognizer()
        self.logger = logger
        self.audio_queue = queue

    # TODO: RECOGNIZE NOT WORKING IN REALTIME DELAY 0.5 HARDCODE
    def transcribe(self):
        while True:
            try:
                text = self.recognizer.recognize_google(self.audio_queue.get(), language="es-ES")
                self.logger.info(text)
            except Exception as e:
                self.logger.error(f"Error: {e}")
