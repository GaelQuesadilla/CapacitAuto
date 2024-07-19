from colorama import init, Fore
import os
import datetime
from src.Config import Config

init(autoreset=True)


class Log():
    """
    A class for logging messages with different types of log levels and colors.

    Attributes
    ----------
    success : str
        Log level indicating a successful operation.
    info : str
        Log level indicating informational messages.
    error : str
        Log level indicating errors or issues.
    warning : str
        Log level indicating warnings or potential issues.

    Methods
    -------
    log(text: str, logType: str = "None", save: bool = True)
        Prints a formatted log message to the console based on the specified log type.
    """
    success = "success"
    info = "info"
    error = "error"
    warning = "warning"

    def log(text: str, logType: str = "None", save: bool = True):
        """
        Prints a formatted log message to the console based on the specified log type.

        Parameters
        ----------
        text : str
            The message to be logged.
        logType : str, optional
            The type of log message. Can be "success", "info", "error", or "warning". Default is "None".
        save : bool, optional
            A flag indicating whether to save the log message. This parameter is currently not used.
            Default is True.

        Returns
        -------
        None
        """

        if logType == Log.info:
            currentLog = f"[?] {text}"
            text = f"{Fore.BLUE}{currentLog}"

        if logType == Log.success:
            currentLog = f"[✓] {text}"
            text = f"{Fore.GREEN}{currentLog}"

        if logType == Log.error:
            currentLog = f"[✘] {text}"
            text = f"{Fore.RED}{currentLog}"

        if logType == Log.warning:
            currentLog = f"[⚠] {text}"
            text = f"{Fore.YELLOW}{currentLog}"

        print(text)

        if save:

            encoding = Config.read("General", "encoding")

            logDir = Config.read("Files", "logs_dir")
            logPath = os.path.join(logDir, "logs.txt")

            now = datetime.datetime.now()
            date = now.strftime("%Y/%m/%d %H:%M:%S")

            currentLog = currentLog.replace(Fore.RESET, "")
            with open(logPath, "a+", encoding=encoding) as logFile:
                logFile.write(f"\n[{date}]: {currentLog}")
