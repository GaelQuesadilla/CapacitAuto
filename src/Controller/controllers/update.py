
import git
import os
from src.Config import Config
from src.Log import setup_logger, trackFunction
from src.Controller.controllers.report import report
import subprocess
import sys

logger = setup_logger(loggerName=__name__)


@trackFunction
def update():
    logger.info("Iniciando actualización")
    baseDir = Config.getPath("Files", "base_dir")
    requirementsFile = baseDir / "requirements.txt"
    try:
        repo = git.Repo(path=Config.getPath("Files", "base_dir"))
        repo.remotes.origin.pull()
        logger.log("Archivos obtenidos")

        if os.getenv("VIRTUAL_ENV"):
            logger.info("Entorno virtual detectado. Utilizando pipenv")
            try:
                subprocess.run(["pipenv", "install"])
            except subprocess.CalledProcessError as e:
                logger.error(f"Error al instalar con pipenv {e}")
                raise e
        else:
            logger.info("Entorno virtual no detectado. Utilizando pip")
            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "-r", requirementsFile]
                )
            except subprocess.CalledProcessError as e:
                logger.error(f"Error al instalar con pip: {e}")
                raise e

        logger.info("Actualización exitosa")

    except git.exc.GitCommandError as e:
        logger.error(f"No ha sido posible actualizar el programa: {e}")
        report()

    except Exception as e:
        logger.error(f"No ha sido posible actualizar el programa: {e}")
        report()
        raise e

    return True
