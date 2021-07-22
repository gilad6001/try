import logging


class Logger:
    logger = logging.getLogger('AppLogger')

    def __init__(self):
        self.logger.setLevel(logging.DEBUG)
        stream_handler = logging.StreamHandler()
        open("output.log", 'w').close()
        file_handler = logging.FileHandler("output.log")
        logger_format = 'LOGGER: %(asctime)-15s %(levelname)-4s %(message)s'
        stream_handler.setFormatter(logging.Formatter(logger_format))
        file_handler.setFormatter(logging.Formatter(logger_format))
        self.logger.addHandler(stream_handler)
        self.logger.addHandler(file_handler)

    @classmethod
    def get(cls):
        return cls.logger


logger_instance = Logger()
