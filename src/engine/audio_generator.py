import edge_tts

class AudioGenerator:
    def __init__(self, logger, translated_text_queue, audio_name_queue):
        self.logger = logger
        self.translated_text_queue = translated_text_queue
        self.audio_name_queue = audio_name_queue

    async def generate(self):
        index = 0
        while True:
            text = self.translated_text_queue.get()
            filename = f"output{index}.wav"
            
            # Usar edge_tts para generar el archivo de audio directamente en formato .m4a
            communicate = edge_tts.Communicate(text, 'es-ES-AlvaroNeural', rate="-20%")
            await communicate.save(filename)
            self.audio_name_queue.put(filename)
            self.logger.info(f"Tamaño cola de audios: {self.audio_name_queue.qsize()}")
            index += 1