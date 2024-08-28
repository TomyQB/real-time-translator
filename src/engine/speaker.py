import pyttsx3
import pygame
import edge_tts
import asyncio
from pydub import AudioSegment
from pydub.playback import play


class Speaker:
    
    def __init__(self, logger, edited_audio_queue):
        self.logger = logger
        self.engine = pyttsx3.init()
        # self._setup_engine()
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
        self.edited_audio_queue = edited_audio_queue
        
    # def _setup_engine(self):
    #     self.engine.setProperty('rate', 120)
    #     voices = self.engine.getProperty("voices")
    #     if voices:
    #         selected_voice = next((voice.id for voice in voices if 'en' in voice.languages), None)
    #         self.engine.setProperty("voice", selected_voice if selected_voice else voices[3].id)
    #     else:
    #         raise ValueError("No voices available or 'voices' is not a valid list.")  


    # async def speak(self):
    #     while True:
    #         first_time_delay = True
    #         try:
    #             filename = self.edited_audio_queue.get()
    #             pygame.mixer.music.load(filename)
    #             pygame.mixer.music.play()
    #             while pygame.mixer.music.get_busy():
    #                 await asyncio.sleep(0.01)
    #         except Exception as e:
    #             self.logger.error(e)
    #             continue

    # VOZ 0 LATENCIA 8
    def speak(self):
        int = 0
        while True:

            filename = "output" + str(int) + ".wav"
            self.engine.save_to_file(self.edited_audio_queue.get(), filename)
            self.engine.runAndWait()
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            int += 1