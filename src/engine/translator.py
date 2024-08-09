import logging
from concurrent.futures import ThreadPoolExecutor

from speech_recognition import Recognizer, Microphone
from mtranslate import translate
import pyttsx3
import threading


class Translator:
    def __init__(self, logger):
        self.recognizer = Recognizer()
        self.microphone = Microphone()
        self.logger = logger
        self.translation_cache = {}
        self.engine = pyttsx3.init()
        self._setup_engine()
        self.executor = ThreadPoolExecutor(max_workers=5)

    def _setup_engine(self):
        voices = self.engine.getProperty("voices")
        if voices:
            # Intenta encontrar una voz en inglés
            selected_voice = next((voice.id for voice in voices if 'en' in voice.languages), None)
            self.engine.setProperty("voice", selected_voice if selected_voice else voices[0].id)
        else:
            raise ValueError("No voices available or 'voices' is not a valid list.")

    def instantiate_tools(self):
        try:
            self.recognizer.pause_threshold = 0.5  # Reduce el tiempo de pausa
            self.recognizer.energy_threshold = 300  # Ajusta el umbral de energía
            self.recognizer.dynamic_energy_threshold = True  # Ajuste dinámico del umbral de energía
        except OSError as e:
            self.logger.error("No Audio Device Available or Incompatible: %s", str(e))
            exit(0)

    def trans3(self, string, lan):
        try:
            if string not in self.translation_cache:
                self.translation_cache[string] = translate(string, lan)
            return self.translation_cache[string]
        except Exception as e:
            self.logger.error(f"Translation error: {e}")
            return string  # Devuelve el texto original si falla la traducción

    def play(self, translated_text):
        self.engine.say(translated_text)
        self.engine.runAndWait()

    def split_and_play(self, translated_text):
        sentences = translated_text.split('. ')
        for sentence in sentences:
            self.play(sentence)

    def recognize_and_translate(self, recognizer, audio):
        try:
            text = recognizer.recognize_google(audio, language="es-ES")
            self.logger.info(f"You said: {text}")
            translated_text = self.trans3(text, "en")
            self.logger.info(f"Translated: {translated_text}")
            self.split_and_play(translated_text)
        except Exception as e:
            self.logger.error(f"Error: {e}")

    def listen(self):
        while True:
            with self.microphone as source:
                audio = self.recognizer.listen(source, phrase_time_limit=5)
                self.executor.submit(self.recognize_and_translate, self.recognizer, audio)