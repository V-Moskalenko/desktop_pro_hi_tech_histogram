import logging
import os
import sys
from logging.handlers import RotatingFileHandler


def find_logs_path(logs_dir_name: str = 'logs') -> str | None:
    """
    Метод поиска папки для логов, относительно запускаемого скрипта

    :param logs_dir_name: имя папки
    :return: абсолютный путь до папки
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Начинаем поиск, пока не дойдём до корня файловой системы
    while current_dir != os.path.dirname(current_dir):
        logs_dir = os.path.join(current_dir, logs_dir_name)
        if os.path.exists(logs_dir) and os.path.isdir(logs_dir):
            return logs_dir
    # Если не нашли папку "logs"
    return None


def setup_logging(logger_name: str = 'app'):
    """Настройка логгера"""
    logs_dir = find_logs_path()

    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    log_file = os.path.join(logs_dir, f'{logger_name}.log')

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    handler = RotatingFileHandler(log_file, maxBytes=1 * 1024 * 1024, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_resource_path(logs_dir_name: str = 'logs') -> str:
    """ Функция для получения корректного пути к ресурсам в упакованном приложении """
    # Если программа запущена в виде exe, то используем временную папку PyInstaller
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, logs_dir_name)
    # Если программа запущена как скрипт
    return find_logs_path(logs_dir_name)

