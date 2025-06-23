import logging
import os

from app.setting.setting import BASE_DIR

logs_dir = os.path.join(BASE_DIR, 'logs')
str_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

error_logger = logging.getLogger('error_logger')
error_logger.setLevel(logging.ERROR)

formatter = logging.Formatter(str_format)
error_file_log = os.path.join(logs_dir, 'errors.log')
error_file_handler = logging.FileHandler(error_file_log)
error_file_handler.setFormatter(formatter)
error_logger.addHandler(error_file_handler)
error_logger.addHandler(logging.StreamHandler())

logging.basicConfig(
    level=logging.DEBUG,
    format=str_format,
)