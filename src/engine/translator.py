import logging
from concurrent.futures import ThreadPoolExecutor
from speech_recognition import Recognizer, Microphone
from mtranslate import translate
import pyttsx3
import threading
import functools


class Translator:
    def __init__(self, logger):
        self.recognizer = Recognizer()
        self.microphone = Microphone()
        self.logger = logger
        self.engine = pyttsx3.init()
        self._setup_engine()
        self.running = True  # Control de ejecución
        self.executor = ThreadPoolExecutor(max_workers=5)

    def _setup_engine(self):
        try:
            voices = self.engine.getProperty("voices")

            if not isinstance(voices, list) or not voices:
                raise ValueError("No voices available or 'voices' is not a valid list.")

            # Intentar encontrar una voz en inglés
            selected_voice = None
            for voice in voices:
                if hasattr(voice, 'languages') and 'en' in voice.languages:
                    selected_voice = voice.id
                    break

            if not selected_voice:
                self.logger.warning("No English voice found, using the first available voice.")
                selected_voice = voices[0].id

            self.engine.setProperty("voice", selected_voice)
        except Exception as e:
            self.logger.error(f"Error setting up text-to-speech engine: {e}")

    def instantiate_tools(self):
        try:
            self.recognizer.pause_threshold = 0.5
            self.recognizer.energy_threshold = 300
            self.recognizer.dynamic_energy_threshold = True
        except OSError as e:
            self.logger.error("No Audio Device Available or Incompatible: %s", str(e))
            exit(0)

    @functools.lru_cache(maxsize=100)
    def trans3(self, string, lan):
        try:
            return translate(string, lan)
        except Exception as e:
            self.logger.error(f"Translation error: {e}")
            return string

    def play(self, translated_text):
        self.engine.say(translated_text)
        self.engine.runAndWait()

    def split_and_play(self, translated_text):
        sentences = translated_text.split('. ')
        for sentence in sentences:
            self.play(sentence)

    def recognize_and_translate(self, audio):
        try:
            text = self.recognizer.recognize_google(audio, language="es-ES")
            self.logger.info(f"You said: {text}")
            translated_text = self.trans3(text, "en")
            self.logger.info(f"Translated: {translated_text}")
            self.split_and_play(translated_text)
        except Exception as e:
            self.logger.error(f"Recognition/Translation error: {e}")

    def listen(self):
        self.instantiate_tools()
        with self.executor as executor:
            while self.running:
                with self.microphone as source:
                    try:
                        audio = self.recognizer.listen(source, phrase_time_limit=5)
                        executor.submit(self.recognize_and_translate, audio)
                    except Exception as e:
                        self.logger.error(f"Listening error: {e}")
                        break  # Rompe el bucle en caso de un error crítico

    def stop_listening(self):
        self.running = False  # Detiene el bucle de escucha
