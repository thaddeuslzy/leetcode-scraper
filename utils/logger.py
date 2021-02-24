from os import environ
from sys import stdout
from datetime import datetime
from logging import getLogger, StreamHandler, FileHandler, DEBUG, INFO, Formatter


def create_logger(logger_name):
  """Create and return a new logger.
  Args:
    logger_name: The name to give the logger.
  """
  logger = getLogger(logger_name)
  formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s')

  stream_handler = StreamHandler(stdout)
  stream_handler.setFormatter(formatter)

  # file_handler = None

  # if 'VERBOSE' in environ and environ['VERBOSE'] == '1':
  #   stream_handler.setLevel(DEBUG)
  #   if file_handler:
  #     file_handler.setLevel(DEBUG)
  #   logger.setLevel(DEBUG)
  # else:
  stream_handler.setLevel(INFO)
  # if file_handler:
  #   file_handler.setLevel(INFO)
  logger.setLevel(INFO)

  logger.addHandler(stream_handler)
  # if file_handler:
  #   logger.addHandler(file_handler)
  return logger
