from pydub import AudioSegment
from pydub.silence import split_on_silence

class AudioEditor:
    def __init__(self, logger, audio_name_queue, edited_audio_queue):
        self.logger = logger
        self.audio_name_queue = audio_name_queue
        self.edited_audio_queue = edited_audio_queue

    def edit_audio(self):
        while True:
            filename = self.audio_name_queue.get()
            audio = AudioSegment.from_file(filename)
            non_silent_audio = split_on_silence(audio, min_silence_len=800, silence_thresh=-40, keep_silence=20)

            non_silent_audio[0].export(filename, format='wav')
            self.edited_audio_queue.put(filename)
            self.logger.info(f"Tamaño cola de audios editados: {self.edited_audio_queue.qsize()}")