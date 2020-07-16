import os
import subprocess
import sys
import typing
from pathlib import Path
import logging

from LoggingManager import logger


class Manager:
    """
    Manager dei logger.
    Ha conoscenza di:
        - *log_folder*: la cartella in cui bisogna salvare i log; viene recuperata automaticamente dal ConfigManager
        - *formatter*: lo stile di format dei logger; contiene un timestamp, il livello di priorità del log e il contenuto del messaggio
    L'unico metodo richiamabile è get_logger(filepath, append=True, level=LoggingLevels.INFO),
    il quale ritorna un logger che scrive in un file specificato in filepath,
    in modalità append o write, e con un livello di priorità settato.
    """
    log_folder = 'logs'

    # altri attributi per il Formatter qui:
    # https://docs.python.org/3/library/logging.html#logrecord-attributes
    formatter = logging.Formatter('%(asctime)s %(levelname)s : %(message)s')

    # https://docs.python.org/3/library/sys.html#sys.platform
    _is_win = sys.platform in ('win32', 'cygwin')
    _changed_win_map = False

    @classmethod
    def get_logger(cls,
                   filepath: typing.Union[str, Path],
                   append: bool = True,
                   level: typing.Union[str, logger.Levels] = logger.Levels.INFO,
                   log_folder: typing.Union[str, Path] = None,
                   formatter: logging.Formatter = None
                   ) -> logger.Logger:
        if isinstance(level, str):
            level = logger.Levels.get_level(level)

        filepath = str(filepath)
        log_folder = log_folder or cls.log_folder
        formatter = formatter or cls.formatter

        # fix windows unicode error when writing to file
        if cls._is_win and not cls._changed_win_map:
            subprocess.run(['chcp', '65001'], shell=True, stdout=subprocess.DEVNULL)
            cls._changed_win_map = True

        # create dir(s) to write logs inside
        os.makedirs(os.path.join(os.getcwd(), cls.log_folder), exist_ok=True)

        return logger.Logger(filepath, append, level, log_folder, formatter)
