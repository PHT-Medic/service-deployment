import logging

from loguru import logger
from elasticapm.handlers.logging import Formatter
import ecs_logging



def test_logging_try():
    fh = logging.FileHandler('test_json.log')
    formatter = ecs_logging.StdlibFormatter()
    fh.setFormatter(formatter)
    logger.add(fh, format="{message}")


    logger.info("Lets start this testscript")
    logger.info("This is just the beginning")
    logger.info("Nobody will know what is coming next")
    logger.warning("Danger is ahead.")
    logger.warning("A lot of unknown bugs and problems.")
    logger.warning("Brace yourself.")
    logger.debug("Starting to tackle the problems.")
    logger.debug("Changing configurations in order to tackle the problem.")
    logger.debug("Further changing...")
    logger.info("Problems are getting smaller...")
    logger.info("Problems are solved!!!!")


def test_logging_try2():
    fh = logging.FileHandler('test_text.log')
    formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)
    logger.add(fh, format="{message}")


    logger.info("Lets start this testscript")
    logger.info("This is just the beginning")
    logger.info("Noody will know what is coming next")
    logger.warning("Danger is ahead.")
    logger.warning("A lot of unknown bugs and problems.")
    logger.warning("Brace yourself.")
    logger.debug("Starting to tackle the problems.")
    logger.debug("Changing configurations in order to tackle the problem.")
    logger.debug("Further changing...")
    logger.info("Problems are getting smaller...")
    logger.info("Problems are solved!!!!")





