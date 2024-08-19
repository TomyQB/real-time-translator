import edge_tts


class AudioGenerator:
    
    def __init__(self, logger, translated_text_queue, audio_name_queue):
        self.logger = logger
        self.translated_text_queue = translated_text_queue
        self.audio_name_queue = audio_name_queue
    

    # VOZ 9 LATENCIA 6
    async def generate(self):
        index = 0
        while True:
            filename = f"output{index}.m4a"
            communicate = edge_tts.Communicate(self.translated_text_queue.get(), 'en-GB-RyanNeural')
            await communicate.save(filename)
            self.audio_name_queue.put(filename)
            index += 1