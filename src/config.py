import configparser
import os

default_config = {
    "General": {
        "encoding": "utf-8",
        "debug": True,
    },
    "Web": {
        "kardex_url": "https://apps.cobachbcs.edu.mx/Sice/ReportesImpresos/wf_Rep_Kardex_ws.aspx",
    },
    "School": {
        "school_key": "03ECB0004K",
        "school_shift": "M",
    },
    "Files": {
        "data_dir": os.path.join(os.getcwd(), "data\\"),
        "output_dir": os.path.join(os.getcwd(), "output\\"),
        "reports_dir": os.path.join(os.getcwd(), "output\\reports\\"),
    },
}


class Config():

    def create():
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
        if not os.path.isfile("config.ini"):
            print("config.ini not found")
            create()
        config = configparser.ConfigParser()
        config.read("config.ini")
        return config.get(section, option)


if __name__ == "__main__":
    Config.create()
