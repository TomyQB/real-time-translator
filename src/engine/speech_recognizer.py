import sounddevice as sd

class SpeechRecognizer:

    # Configuración de la grabación
    SAMPLE_RATE = 16000  # Vosk requiere una tasa de muestreo de 16000 Hz
    BLOCK_SIZE = 16000 * 2    # Tamaño de los bloques de audio que se procesarán (2 segundos)

    def __init__(self, logger, queue):
        self.logger = logger
        self.audio_queue = queue

    def listen(self):
        def callback(indata, frames, time, status):
            if status:
                print(status, flush=True)
            self.audio_queue.put(bytes(indata))
        
        with sd.RawInputStream(samplerate=self.SAMPLE_RATE, blocksize=self.BLOCK_SIZE, dtype='int16', channels=1, callback=callback):
            while True:
                sd.sleep(1000)
