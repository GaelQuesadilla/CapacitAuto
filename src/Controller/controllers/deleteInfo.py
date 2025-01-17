from src.Config import Config
import pathlib
import shutil
from src.Log import setup_logger

logger = setup_logger(loggerName=__name__)


def deleteInfo():
    dataDir: pathlib.Path = Config.getPath("Files", "data_dir")

    if dataDir.is_dir():
        logger.info("Eliminando directorio")
        try:
            shutil.rmtree(dataDir)
            Config.setup()
        except Exception as e:
            logger.error(
                "No ha sido posible eliminar la información de la aplicación"
            )
            raise e


if __name__ == "__main__":
    deleteInfo()
