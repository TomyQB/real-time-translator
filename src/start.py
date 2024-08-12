import argparse
import os
import sys
from time import monotonic
from tendo.singleton import SingleInstance, SingleInstanceException

# FILES
from src.main import config_args, run_main
from src.engine import init_logging, get_config

# PATH_LOG = os.path.join(os.getenv('APPDATA'), 'InteliaPharma', 'log')
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
        exit_code = run_main(args, logger, config)
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
