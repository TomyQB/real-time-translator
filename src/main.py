import argparse
import configparser
import logging
from multiprocessing import freeze_support

# PROJECT FILES
from src.engine.translator import instantiate_tools, play, trans3, listen


def config_args(parser):
    parser.add_argument('--name', action="store", required=False, type=str, help="test parameter")
    return True


def run_main(args: argparse.Namespace, logger: logging.Logger, config: configparser.ConfigParser) -> int:
    # Instantiate tools translator
    recognizer, microphone = instantiate_tools(logger)

    # Start listening with asyncio
    listen(recognizer=recognizer, logger=logger)


