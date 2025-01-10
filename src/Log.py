from typing import Callable
import os
from src.Config import Config
import logging
import time
import pathlib

logsDir = pathlib.Path(Config.read("Files", "logs_dir"))
logsFile = logsDir / "logs.log"


def setup_logger(logsFile: str = logsFile, loggerName: str = __name__) -> logging.Logger:

    logsDir.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(
                logsFile, encoding=Config.read("General", "encoding")),
            logging.StreamHandler()
        ]
    )

    # Crear un logger específico para tu aplicación
    logger: logging.Logger = logging.getLogger(loggerName)
    return logger


def trackFunction(func: Callable):
    """Decorator for log a function

    Parameters
    ----------
    func : Callable
        The function to be decorated
    """
    logger = setup_logger(loggerName=func.__name__)

    def wrapper(*args, **kwargs):
        t1 = time.time()

        logger.info(
            f"Inicio de la función: {func.__name__} con args="
            f"{args} y kwargs={kwargs}"
        )

        try:
            result = func(*args, **kwargs)

        except KeyboardInterrupt:
            logger.warning(
                f"Función {func.__name__} interrumpida manualmente."
            )
            exit(code=1)

        except Exception as e:
            logger.exception(
                f"Error en la función: {func.__name__}. Error -> {e}"
            )
            raise

        else:
            logger.info(f"Fin de la función: {func.__name__} sin errores.")

        finally:
            t2 = time.time()
            logger.info(
                f"Función {func.__name__} ejecutada en {t2 - t1:.4f} segundos."
            )

        return result

    return wrapper
