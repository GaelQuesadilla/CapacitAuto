from colorama import init, Fore
import os
import datetime
from src.Config import Config
import time
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
    function : str
        Log level for decorators
    function_error : str
        Log level for error in decorated functions
    action: str
        Log level when request when request an action from the user

    Methods
    -------
    log(text: str, logType: str = "None", save: bool = True)
        Prints a formatted log message to the console based on the specified log type.
    """
    success = "success"
    info = "info"
    error = "error"
    warning = "warning"
    function = "function"
    function_error = "function_error"
    action = "action"

    def log(text: str, logType: str = "None", save: bool = True, show: bool = True):
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
        show: bool, optional
            If True print the log; If False do not print, Default is True

        Returns
        -------
        None
        """

        if logType == Log.info:
            currentLog = f"[?] {text}"
            text = f"{Fore.BLUE}{currentLog}"

        elif logType == Log.success:
            currentLog = f"[✓] {text}"
            text = f"{Fore.GREEN}{currentLog}"

        elif logType == Log.error:
            currentLog = f"[✘] {text}"
            text = f"{Fore.RED}{currentLog}"

        elif logType == Log.function_error:
            currentLog = f"[λ✘] {text}"
            text = f"{Fore.RED}{currentLog}"

        elif logType == Log.warning:
            currentLog = f"[⚠] {text}"
            text = f"{Fore.YELLOW}{currentLog}"

        elif logType == Log.function:
            currentLog = f"[λ] {text}"
            text = f"{Fore.LIGHTGREEN_EX}{currentLog}"

        elif logType in [Log.action, Log.warning]:
            currentLog = f"[>] {text}"
            text = f"{Fore.MAGENTA}{currentLog}"

        if show:
            text = text.replace("\n", "\n\t")
            if logType == Log.action:
                text = f"\n{text}"
            print(text)

        if save and Config.read("General", "debug"):

            encoding = Config.read("General", "encoding")

            logDir = Config.read("Files", "logs_dir")
            logPath = os.path.join(logDir, "logs.txt")

            now = datetime.datetime.now()
            date = now.strftime("%Y/%m/%d %H:%M:%S")

            currentLog = currentLog.replace("\n", "\n\t\t\t\t\t|->")

            currentLog = currentLog.replace(Fore.RESET, "")
            with open(logPath, "a+", encoding=encoding) as logFile:
                logFile.write(f"\n[{date}]: {currentLog}")


def log_function(func):
    """Decorator for log a function

    Parameters
    ----------
    func : function
        The function to be decorated
    """
    def wrapper(*args, **kwargs):
        t1 = time.time()

        Log.log(
            text=f"Inicio de la función: {func.__name__}\n{args=}\n{kwargs=}",
            logType=Log.function,
            save=True,
            show=False
        )

        try:
            result = func(*args, **kwargs)

        except Exception as e:
            Log.log(
                text=f"Error en la función: {func.__name__}\nError -> {e}",
                logType=Log.function_error,
                save=True,
                show=True
            )
        except KeyboardInterrupt:
            Log.log(
                text=f"Error en la función: {
                    func.__name__}\nError -> El sistema ha sido interrumpido",
                logType=Log.function_error,
                save=True,
                show=True
            )
            exit()

        t2 = time.time()

        Log.log(
            text=f"Fin de la función: {func.__name__}, Se ejecutó en {
                t2-t1} segundos",
            logType=Log.function,
            save=True,
            show=False
        )
        return result

    return wrapper
