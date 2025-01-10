import configparser
import os
import pathlib

"""
This module defines a `Config` class for managing configuration settings in an INI file.

The default configuration is a dictionary with sections and key-value pairs
"""


default_config = {
    "General": {
        "encoding": "utf-8",
        "debug": True,
        "relevant_subjects_name": "Materias relevantes para {}",
        "relevant_grades_name": "Promedio relevante para {}",
        "choice_name": "Opcion {}",
        "list_path_format": "Lista Alumnos {semestre}-{grupo}-{turno}.xlsx",
    },
    "Web": {
        "kardex_url": "https://apps.cobachbcs.edu.mx/Sice/ReportesImpresos/wf_Rep_Kardex_ws.aspx",
        "cache_expire_after": 72*60*60,  # 72h
        "kardex_cache_session_name": "cache/kardex"
    },
    "School": {
        "school_key": "03ECB0004K",
        "school_shift": "M",
        "packages":
            "Informatica,Servicios turisticos,Dibujo arquitectonico,Contabilidad",
        "trainings":
            "Ciencias economico administrativas,Ciencias naturales,Ciencias exactas,Ciencias sociales y humanidades",
        "max_students_in_group": 45,
        "groups": 4,
    },
    "Files": {
        "base_dir": pathlib.Path.cwd(),
        "config_dir": pathlib.Path.cwd() / "config.ini",
        "data_dir": pathlib.Path.cwd() / "data",
        "reports_dir": pathlib.Path.cwd() / "data" / "reports",
        "lists_dir": pathlib.Path.cwd() / "data" / "lists",
        "curps_dir": pathlib.Path.cwd() / "data" / "CURPS.txt",
        "all_kardex_dir": pathlib.Path.cwd() / "data" / "allKardex.json",
        "curp_report_dir": pathlib.Path.cwd() / "data" / "reports" / "curp_report.txt",

        "output_dir": pathlib.Path.cwd() / "output",
        "output_dir": pathlib.Path.cwd() / "output",
        "logs_dir": pathlib.Path.cwd() / "logs",
        "assets_dir": pathlib.Path.cwd() / "assets",
        "base_dir": pathlib.Path.cwd() / "",
        "kardex_data_dir": pathlib.Path.cwd() / "data" / "kardexData.json",
        "all_subjects_dir": pathlib.Path.cwd() / "data" / "AllSubjects.xlsx",
        "choices_dir": pathlib.Path.cwd() / "data" / "choices.xlsx",
        "list_results_dir": pathlib.Path.cwd() / "data" / "lists" / "results",
    },
    "Assets": {
        "logo_image_dir": pathlib.Path.cwd() / "assets" / "images" / "cobach_logo.png",
    },
    "Dev": {
        "enable_ttkbootstrap": False
    },
}


class Config():
    """Provides methods for creating and reading configuration settings from a file.

    * General:
        * encoding (str): Codificación de caracteres (predeterminado: "utf-8")
        * debug (bool): Habilitar el modo de depuración (predeterminado: True)
        * relevant_subjects_name (str): Formato para el nombre de materias relevantes (predeterminado: "Materias relevantes para {}")
        * relevant_grades_name (str): Formato para el nombre del promedio relevante (predeterminado: "Promedio relevante para {}")
    * Web:
        * kardex_url (str): URL para acceder a los registros de estudiantes (predeterminado: "https://apps.cobachbcs.edu.mx/Sice/ReportesImpresos/wf_Rep_Kardex_ws.aspx")
        * cache_expire_after (str): Tiempo en segundos para usar la caché (predeterminado: 72 horas)
        * kardex_cache_session_name (str): Nombre de la sesión de caché para guardar solicitudes de kardex (predeterminado: "cache/kardex")
    * School:
        * school_key (str): Clave de identificación de la escuela
        * school_shift (str): Turno de la escuela (por ejemplo, "M" para matutino)
        * packages (str, separados por comas): Lista de paquetes ofrecidos
        * trainings (str, separados por comas): Lista de áreas de capacitación ofrecidas
    * Files:
        * data_dir (str): Directorio para almacenar archivos de datos (predeterminado: "data/")
        * output_dir (str): Directorio base para archivos de salida (predeterminado: "output/")
        * reports_dir (str): Directorio para almacenar informes dentro de la salida (predeterminado: "output/reports/")
        * lists_dir (str): Directorio para almacenar listas dentro de la salida (predeterminado: "output/lists/")
        * logs_dir (str): Directorio para almacenar registros (predeterminado: "logs/")
    """

    def create():
        """
        Creates a new configuration file("config.ini") with default settings.

        Raises
        ------
        Exception
            If an error occurs while creating the file.
        """
        print("Creating config file")
        try:
            config = configparser.ConfigParser()
            config["General"] = default_config.get("General")
            config["Web"] = default_config.get("Web")
            config["School"] = default_config.get("School")
            config["Files"] = default_config.get("Files")
            config["Assets"] = default_config.get("Assets")
            config["Dev"] = default_config.get("Dev")
            with open("config.ini", "w") as config_file:
                config.write(config_file)
            print("Config file has been written successfully")
        except Exception as e:
            print("Error")
            print(e)

    def read(section: str, option: str) -> any:
        """Reads a specific configuration value from the file("config.ini").

        Parameters
        ----------
        section: str
            The section name in the configuration file
        option: str
            The option name

        Returns
        -------
        str
            The value of the selected option
        """

        configPath = pathlib.Path.cwd() / "config.ini"

        if not configPath.is_file():
            print("config.ini not found")
            config.create()
        config = configparser.ConfigParser()
        config.read("config.ini")

        value = config.get(section, option)
        defaultValue = default_config.get(section).get(option)

        try:
            if type(defaultValue) == str:
                pass
            elif type(defaultValue) == int:
                value = int(value)
            elif type(defaultValue) == float:
                value = float(value)

        except Exception:
            pass
        return value

    def getPath(section: str, option: str) -> pathlib.Path:
        path = pathlib.Path(Config.read(section, option))
        return path

    def setup():
        for option, defaultValue in default_config.get("Files").items():
            path = pathlib.Path(Config.read("Files", option))

            if path.suffix == "":
                # Create a directory
                path.mkdir(exist_ok=True)
            elif not path.is_file():
                # Create an empty file
                print(f"Creando el archivo {path}")
                path.parent.mkdir(exist_ok=True)
                path.write_text("")

        print("Setup done")


if __name__ == "__main__":
    Config.create()
    Config.setup()
