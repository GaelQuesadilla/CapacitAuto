from git import Repo
from src.Config import Config
from src.Log import setup_logger, trackFunction
logger = setup_logger(loggerName=__name__)


@trackFunction
def update():
    logger.info("Iniciando actualización")
    try:
        repo = Repo(path=Config.getPath("Files", "base_dir"))
        repo.remotes.origin.pull()
        logger.info("Actualización exitosa")

    except Exception as e:
        logger.error("No ha sido posible actualizar el programa")
        raise e

    return True
