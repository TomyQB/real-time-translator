import pyttsx3
import pygame
import edge_tts
import asyncio
from pydub import AudioSegment
from pydub.playback import play


class Speaker:
    
    def __init__(self, logger, audio_name_queue):
        self.logger = logger
        self.engine = pyttsx3.init()
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
        self._setup_engine()
        self.audio_name_queue = audio_name_queue

    def _setup_engine(self):
        self.engine.setProperty('rate', 120)
        voices = self.engine.getProperty("voices")
        if voices:
            selected_voice = next((voice.id for voice in voices if 'en' in voice.languages), None)
            self.engine.setProperty("voice", selected_voice if selected_voice else voices[3].id)
        else:
            raise ValueError("No voices available or 'voices' is not a valid list.")  

    # VOZ 9 LATENCIA 6
    async def speak(self):
        while True:
            try:
                pygame.mixer.music.load(self.audio_name_queue.get())
                while pygame.mixer.music.get_busy():
                    await asyncio.sleep(0.1)
                pygame.mixer.music.play()
            except Exception as e:
                self.logger.error(e)
                continue

    # VOZ 0 LATENCIA 8
    # def speak(self):
    #     int = 0
    #     while True:

    #         filename = "output" + str(int) + ".wav"
    #         self.logger.info("BEFORE: " + str(int))
    #         # Guardar el texto en un archivo de audio WAV
    #         self.engine.save_to_file(self.translated_text_queue.get(), filename)
    #         self.engine.runAndWait()  # Esperar a que se guarde el archivo

    #         self.logger.info("MIDDLE: " + str(int))

    #         pygame.mixer.music.load(filename)
    #         pygame.mixer.music.play()
    #         self.logger.info("AFTER: " + str(int))
    #         int += 1