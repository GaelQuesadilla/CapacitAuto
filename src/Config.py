import configparser
import os

"""
This module defines a `Config` class for managing configuration settings in an INI file.

The default configuration is a dictionary with sections and key-value pairs:

* General:
    * encoding (str): Character encoding (default: "utf-8")
    * debug (bool): Enable debugging mode (default: True)
    * relevant_subjects_name (str): Format string for relevant subjects name (default: "Materias relevantes para {}")
    * relevant_grades_name (str): Format string for relevant grades name (default: "Promedio relevante para {}")
* Web:
    * kardex_url (str): URL for accessing student records (default: "https://apps.cobachbcs.edu.mx/Sice/ReportesImpresos/wf_Rep_Kardex_ws.aspx")
* School:
    * school_key (str): School identification key
    * school_shift (str): School shift (e.g., "M" for morning)
    * packages (str, comma-separated): List of offered packages
    * trainings (str, comma-separated): List of offered training areas
* Files:
    * data_dir (str): Directory for storing data files (default: "data/")
    * output_dir (str): Base directory for output files (default: "output/")
    * reports_dir (str): Directory for storing reports within output (default: "output/reports/")
    * lists_dir (str): Directory for storing lists within output (default: "output/lists/")
"""


default_config = {
    "General": {
        "encoding": "utf-8",
        "debug": True,
        "relevant_subjects_name": "Materias relevantes para {}",
        "relevant_grades_name": "Promedio relevante para {}",
    },
    "Web": {
        "kardex_url": "https://apps.cobachbcs.edu.mx/Sice/ReportesImpresos/wf_Rep_Kardex_ws.aspx",
    },
    "School": {
        "school_key": "03ECB0004K",
        "school_shift": "M",
        "packages":
            "Informatica,Servicios turísticos,Dibujo arquitectónico,Contabilidad",
        "trainings":
            "Ciencias economico administrativas,Ciencias naturales,Ciencias exactas,Ciencias sociales y humanidades",
    },
    "Files": {
        "data_dir": os.path.join(os.getcwd(), "data\\"),
        "output_dir": os.path.join(os.getcwd(), "output\\"),
        "reports_dir": os.path.join(os.getcwd(), "output\\reports\\"),
        "lists_dir": os.path.join(os.getcwd(), "output\\lists\\"),
    },
}


class Config():
    """Provides methods for creating and reading configuration settings from a file."""

    def create():
        """
        Creates a new configuration file ("config.ini") with default settings.

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
            with open("config.ini", "w") as config_file:
                config.write(config_file)
            print("Config file has been written successfully")
        except Exception as e:
            print("Error")
            print(e)

    def read(section: str, option: str):
        """Reads a specific configuration value from the file ("config.ini").

        Parameters
        ----------
        section : str
            The section name in the configuration file
        option : str
            The option name

        Returns
        -------
        str
            The value of the selected option
        """
        if not os.path.isfile("config.ini"):
            print("config.ini not found")
            create()
        config = configparser.ConfigParser()
        config.read("config.ini")
        return config.get(section, option)


if __name__ == "__main__":
    Config.create()
