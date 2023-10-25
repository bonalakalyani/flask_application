import os
import logging
from logging.handlers import RotatingFileHandler
from service.config import Config


def get_custom_formatter(config: Config) -> logging.Formatter:
    return logging.Formatter(config.LOG_FORMAT)


# log = logging.getLogger('urllib3')
# log.setLevel(logging.DEBUG)
# formatter_api = logging.Formatter(
#         '[%(asctime)s] %(levelname)s in %(filename)s:%(lineno)d '
#         '%(message)s')
# log_file_path = "./dayforce/logger_details/logger_info.log"
# # error_log_file_path = "./dayforce/logger_details/error.log"
# log_dir = os.path.dirname(log_file_path)
# os.makedirs(log_dir, exist_ok=True)
# fh = RotatingFileHandler(
#     log_file_path,
#     mode='a',
#     maxBytes=5 * 1024 * 1024,
#     backupCount=2,
#     encoding=None,
#     delay=0
# )
# fh.setFormatter(formatter_api)
# log.addHandler(fh)


# # Create file handler for error logs
# error_fh = RotatingFileHandler(
#     error_log_file_path,
#     mode='a',
#     maxBytes=5 * 1024 * 1024,
#     backupCount=2,
#     encoding=None,
#     delay=0
# )
# formatter_error = logging.Formatter("[%(asctime)s]  %(levelname)s - %(message)s") # noqa: E501
# error_fh.setFormatter(formatter_error)
# error_fh.setLevel(logging.ERROR)
# log.addHandler(error_fh)
