import pyttsx3


class Speaker:
    def __init__(self, logger, translated_text_queue):
        self.logger = logger
        self.engine = pyttsx3.init()
        self._setup_engine()
        self.translated_text_queue = translated_text_queue

    def _setup_engine(self):
        self.engine.setProperty('rate', 140)
        voices = self.engine.getProperty("voices")
        if voices:
            selected_voice = next((voice.id for voice in voices if 'en' in voice.languages), None)
            self.engine.setProperty("voice", selected_voice if selected_voice else voices[2].id)
        else:
            raise ValueError("No voices available or 'voices' is not a valid list.")

    def speak(self):
        while True:
            self.engine.say(self.translated_text_queue.get())
            self.engine.runAndWait()
