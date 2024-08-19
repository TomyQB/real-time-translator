import argparse
import os
import sys
from time import monotonic
from multiprocessing import Process, Queue
from tendo.singleton import SingleInstance, SingleInstanceException

from src.main import config_args, run_main
from src.engine import init_logging, get_config


PATH_CONFIG = os.path.join(os.getcwd(), 'config')

if __name__ == "__main__":
    exit_code = 0
    app_name = "recognition-translation"
    me = SingleInstance()
    ts = monotonic()

    config = get_config(PATH_CONFIG)

    logconfig = os.path.join(PATH_CONFIG, 'config', 'logging.conf')

    logger = init_logging(app_name=app_name)
    try:
        args = {}
        parser = argparse.ArgumentParser(description="")
        if config_args(parser):
            args = parser.parse_args()

        recognize_queue = Queue()
        text_queue = Queue()
        translated_text_queue = Queue()

        speech_recognizer_process = Process(target=run_main, args=(args, logger, config, None, recognize_queue, "speech_recognizer"))
        transcriptor_process = Process(target=run_main, args=(args, logger, config, recognize_queue, text_queue, "transcriptor"))
        translator_process = Process(target=run_main, args=(args, logger, config, text_queue, translated_text_queue, "translator"))
        speaker_process = Process(target=run_main, args=(args, logger, config, translated_text_queue, None, "speaker"))

        speech_recognizer_process.start()
        transcriptor_process.start()
        translator_process.start()
        speaker_process.start()

        speech_recognizer_process.join()
        transcriptor_process.join()
        translator_process.join()
        speaker_process.join()

    except (KeyboardInterrupt, SystemExit):
        logger.error("Ctrl+C or SystemExit")
    except SingleInstanceException:
        logger.error(f"{app_name} is already running")
        exit_code = 1
    except Exception as e:
        logger.error('An exception raised in main thread', exc_info=True)
        exit_code = 2
    finally:
        logger.info(f"{app_name}, ended after {monotonic() - ts} seconds")
        sys.exit(exit_code)
