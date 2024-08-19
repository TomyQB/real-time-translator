import vosk
import json

class Transcriptor:

    SAMPLE_RATE = 16000  # Tasa de muestreo

    model = vosk.Model("vosk-model-small-es-0.42")

    def __init__(self, logger, recognize_queue, text_queue):
        self.logger = logger
        self.recognize_queue = recognize_queue
        self.text_queue = text_queue

    def transcribe(self):
        recognizer = vosk.KaldiRecognizer(self.model, self.SAMPLE_RATE)
        last_result = ""  # Variable para almacenar el último resultado completo
        last_partial = ""  # Variable para almacenar la última transcripción parcial
        
        while True:
            audio_data = self.recognize_queue.get()
            if recognizer.AcceptWaveform(audio_data):
                result = recognizer.Result()
                result_dict = json.loads(result)
                complete_result = result_dict.get("text", "").strip()
                
                if complete_result != last_result:
                    last_result = complete_result  # Actualizar el último resultado completo
                last_partial = ""  # Restablecer la transcripción parcial
            else:
                partial_result = recognizer.PartialResult()
                partial_result_dict = json.loads(partial_result)
                current_partial = partial_result_dict.get("partial", "").strip()

                # Comparar la transcripción parcial actual con la última
                if current_partial != last_partial:
                    # Imprimir solo la nueva parte de la transcripción parcial
                    new_words = current_partial[len(last_partial):].strip()
                    if new_words:
                        self.logger.info(new_words)
                        self.text_queue.put(new_words)
                    last_partial = current_partial  # Actualizar la última transcripción parcial
