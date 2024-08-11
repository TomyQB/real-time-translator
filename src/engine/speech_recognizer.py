import logging
from speech_recognition import Recognizer, Microphone
from multiprocessing import Queue

class SpeechRecognizer:
    def __init__(self, logger, queue):
        self.recognizer = Recognizer()
        self.microphone = Microphone()
        self.logger = logger
        self.audio_queue = queue

    def instantiate_tools(self):
        try:
            self.recognizer.pause_threshold = 0.5  # Reduce el tiempo de pausa
            self.recognizer.energy_threshold = 300  # Ajusta el umbral de energía
            self.recognizer.dynamic_energy_threshold = True  # Ajuste dinámico del umbral de energía
        except OSError as e:
            self.logger.error(f"No Audio Device Available or Incompatible: {e}")
            exit(0)

    # TODO: FIX EXECUTOR MULTIPLE INSTANCE NOT WORKING
    def listen(self):
        while True:
            with self.microphone as source:
                self.audio_queue.put(self.recognizer.listen(source, phrase_time_limit=2))
