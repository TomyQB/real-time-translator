import argparse
import configparser
import logging
from multiprocessing import Queue
import asyncio

# PROJECT FILES
from src.engine.translator import Translator
from src.engine.speech_recognizer import SpeechRecognizer
from src.engine.transcriptor import Transcriptor
from src.engine.translator import Translator
from src.engine.audio_generator import AudioGenerator
from src.engine.audio_editor import AudioEditor
from src.engine.speaker import Speaker

def config_args(parser):
    parser.add_argument('--name', action="store", required=False, type=str, help="test parameter")
    return True

def run_main(args: argparse.Namespace, logger: logging.Logger, config: configparser.ConfigParser, reading_queue, writing_queue: Queue, processType) -> int:
    if not logger.hasHandlers():
        logger = logging.getLogger(processType)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    if processType == "speech_recognizer":
        logger.info("Inicializando SpeechRecognizer...")
        speechReconizer = SpeechRecognizer(logger, writing_queue)
        speechReconizer.listen()

    elif processType == "transcriptor":
        logger.info("Inicializando Transcriptor...")
        transcriptor = Transcriptor(logger, reading_queue, writing_queue)
        transcriptor.transcribe()

    elif processType == "translator":
        logger.info("Inicializando Translator...")
        translator = Translator(logger, reading_queue, writing_queue)
        translator.translate()

    elif processType == "audio_generator":
        logger.info("icializando AudioGenerator...")
        audioGenerator = AudioGenerator(logger, reading_queue, writing_queue)
        asyncio.run(audioGenerator.generate())

    elif processType == "audio_editor":
        logger.info("Inicializando AudioEditor...")
        audioEditor = AudioEditor(logger, reading_queue, writing_queue)
        audioEditor.edit_audio()

    elif processType == "speaker":
        logger.info("Inicializando Speaker...")
        speaker = Speaker(logger, reading_queue)
        asyncio.run(speaker.speak())

    return 0
