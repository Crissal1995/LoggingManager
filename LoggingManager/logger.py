import logging
import inspect
import enum
import os


class Levels(enum.Enum):
    """
    Alert levels for logging
    """
    NOTSET = logging.NOTSET
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class Logger:
    """
    Oggetto logger vero e proprio, fa da wrapper di logging.Logger,
    con la particolarità che nell' __init__ è possibile decidere un filepath
    per il file di log da creare (andando a mascherare la complessità
    del modulo logging).
    Nel costruttore, inoltre, è possibile passare un livello di logging
    (uno dei valori dell'enum Levels) e decidere se aprire il file
    in modalità append oppure write.
    È possibile gestire l'estensione dei file di log (default '.log'),
    cambiare livello di logging ed infine loggare un messaggio (eventualmente
    con un diverso livello di logging rispetto quello attuale).
    """
    ext = '.log'

    def __init__(self, filepath: str, append: bool, level: Levels, log_folder, formatter):
        self.log_folder = log_folder
        self.formatter = formatter

        # sanitize input by user
        sane_fp = self._sanitize_filepath(filepath)
        self.filepath = sane_fp

        # get name removing '.log' from name
        filename = os.path.basename(os.path.splitext(sane_fp)[0])

        # set current level of priority
        self._current_level = level

        # setup logger with utility function
        self.logger = self._setup_logger(filename, sane_fp, level, append)

        # write line if append to distinguish between elements
        if append:
            self.logger.debug('NEW SESSION'.center(51, '-'))

    def log(self, *args, **kwargs):
        level = kwargs.get('level', self._current_level).value
        to_write = ''
        for arg in args:
            to_write += str(arg) + ' '
        to_write = to_write.strip()  # remove leading and trailing spaces
        to_write_dict = dict(name=Logger._get_caller_name(), content=to_write)
        to_write_format = '{name}\n{content}\n'
        try:
            self.logger.log(level, to_write_format.format(**to_write_dict))
        except UnicodeError as e:
            to_write_dict['content'] = '[UNICODE ERROR] ' + str(e)
            self.logger.log(level, to_write_format.format(**to_write_dict))

    def info(self, *args, **kwargs):
        return self.log(*args, **kwargs, level=Levels.INFO)

    def debug(self, *args, **kwargs):
        return self.log(*args, **kwargs, level=Levels.DEBUG)

    def error(self, *args, **kwargs):
        return self.log(*args, **kwargs, level=Levels.ERROR)

    def warning(self, *args, **kwargs):
        return self.log(*args, **kwargs, level=Levels.WARNING)

    def critical(self, *args, **kwargs):
        return self.log(*args, **kwargs, level=Levels.CRITICAL)

    def change_level(self, new_level: Levels):
        self._current_level = new_level

    def get_file_handler(self):
        return self.logger.handlers[0]

    def _setup_logger(self, name, log_file, level: Levels, append: bool):
        mode = 'a' if append else 'w'
        handler = logging.FileHandler(log_file, mode)
        handler.setFormatter(self.formatter)

        logger = logging.getLogger(name)
        logger.setLevel(level.value)
        logger.addHandler(handler)

        return logger

    def _sanitize_filepath(self, filepath: str):
        # test/foo/bar/my_log -> my_log
        filepath = os.path.basename(filepath)

        # test/foo/bar/ -> ''
        if not filepath:
            raise ValueError('Cannot create a folder as log!')

        # my_log or my_log.xyz
        if not filepath.lower().endswith(Logger.ext):
            # my_log -> my_log.log
            # my_log.sublog -> my_log.sublog.log
            filepath += Logger.ext

        # my_log.log -> <log_folder>/my_log.log
        return os.path.join(self.log_folder, filepath)

    @staticmethod
    def _get_caller_name():
        # stack situation when this function is called:
        # _get_caller_name [0]
        # log [1]
        # <function> [2]
        last_frame = inspect.stack()[2]
        # FrameInfo(frame, filename, lineno, function, code_context, index)
        return last_frame[3]
