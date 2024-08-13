from mtranslate import translate

class Translator:
    def __init__(self, logger, text_queue, translated_text_queue):
        self.logger = logger
        self.text_queue = text_queue
        self.translated_text_queue = translated_text_queue

    def translate(self):
        while True: 
            translated_text = translate(self.text_queue.get(), "en")
            self.logger.info(translated_text)
            self.translated_text_queue.put(translated_text)
