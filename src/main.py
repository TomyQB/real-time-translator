import argparse
import configparser
import logging
from multiprocessing import freeze_support

# PROJECT FILES
from src.engine.translator import Translator


def config_args(parser):
    parser.add_argument('--name', action="store", required=False, type=str, help="test parameter")
    return True


def run_main(args: argparse.Namespace, logger: logging.Logger, config: configparser.ConfigParser) -> int:
    # Instantiate tools translator
    translator = Translator(logger=logger)
    if translator.recognizer and translator.microphone:
        # Start listening with the recognizer
        translator.listen()
    return 0


