import webbrowser
from src.Config import Config
import pathlib
from typing import List
import urllib.parse
import platform
import sys
from git import Repo
import datetime

from src.Log import setup_logger

logger = setup_logger(loggerName=__name__)


def report():
    logger.info("Iniciando reporte")
    logsDir: pathlib.Path = Config.getPath("Files", "logs_dir") / "logs.log"
    configDir: pathlib.Path = Config.getPath("Files", "config_dir")
    encoding = Config.read("General", "encoding")

    lastLogs = "No hay registros disponibles"
    configValues = "El archivo config.ini no se encuentra disponible"

    if logsDir.is_file():
        lastLogs: List[str] = logsDir.read_text(
            encoding=encoding).splitlines()[-10:]
        lastLogs = "\n".join(lastLogs)

    if configDir.is_file():
        configValues: List[str] = configDir.read_text().splitlines()
        configValues = "\n".join(configValues)

    commitHash = "No disponible"
    commitMessage = "No disponible"
    commitAuthor = "No disponible"
    commitDate = "No disponible"
    currentBranch = "No disponible"
    try:
        repo = Repo(Config.getPath("Files", "base_dir"))
        currentBranch = repo.active_branch
        commit = repo.head.commit

        commitHash = commit.hexsha
        commitMessage = commit.message.strip()
        commitAuthor = commit.author.name
        commitDate = datetime.datetime.fromtimestamp(
            commit.committed_date).strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        pass

    params = {
        "to": "gaelglz032@gmail.com",
        "subject": "Capacitauto - Reporte de errores",
        "body": f"""*<<Por favor, describa el problema, como le afecta y enumere los pasos específicos que siguió antes de encontrar el problema, de ser posible agregue fotos o videos>>*
*<Si es posible agregue medios de contacto>*
-------------- NO MODIFICAR --------------
>> Sistema
Sistema operativo: {platform.system()}
Versión del sistema operativo: {platform.version()}
Versión de python: {sys.version}
Commit hash: {commitHash}
Commit message: {commitMessage}
Commit author: {commitAuthor}
Commit date: {commitDate}
Branch: {currentBranch}
-------------- NO MODIFICAR --------------
>> Últimos registros
{lastLogs}
-------------- NO MODIFICAR --------------
>> Configuración
{configValues}
"""
    }

    url = "mailto:?" + urllib.parse.urlencode(params)

    webbrowser.open(url)


if __name__ == "__main__":
    report()
