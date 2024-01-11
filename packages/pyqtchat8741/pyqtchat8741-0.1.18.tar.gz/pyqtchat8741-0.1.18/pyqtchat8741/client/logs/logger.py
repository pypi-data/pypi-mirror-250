import logging
import sys
import os

from ..core.variables import LOGGING_LEVEL

# создаём формировщик логов (formatter):
client_formatter = logging.Formatter("%(asctime)s %(levelname)s %(filename)s %(message)s")

# Подготовка имени файла для логирования
path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, "client.log")

# создаём потоки вывода логов
steam = logging.StreamHandler(sys.stderr)
steam.setFormatter(client_formatter)
steam.setLevel(logging.ERROR)
log_file = logging.FileHandler(path, encoding="utf8")
log_file.setFormatter(client_formatter)

# создаём регистратор и настраиваем его
logger = logging.getLogger("client")
logger.addHandler(steam)
logger.addHandler(log_file)
logger.setLevel(LOGGING_LEVEL)


def log(func_to_log):
    """
    Декоратор, выполняющий логирование вызовов функций.
    Сохраняет события типа debug, содержащие
    информацию о имени вызываемой функиции, параметры с которыми
    вызывается функция, и модуль, вызывающий функцию.
    """

    def log_saver(*args, **kwargs):
        logger.debug(
            f"Была вызвана функция {func_to_log.__name__} c параметрами {args} , {kwargs}. "
            f"Вызов из модуля {func_to_log.__module__}"
        )
        ret = func_to_log(*args, **kwargs)
        return ret

    return log_saver


# отладка
if __name__ == "__main__":
    logger.critical("Test critical event")
    logger.error("Test error ivent")
    logger.debug("Test debug ivent")
    logger.info("Test info ivent")
