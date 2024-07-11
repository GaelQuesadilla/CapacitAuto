import configparser
import os

default_config = {
    "General": {
    }
}


def create():

    print("Creating config file")
    try:
        config = configparser.ConfigParser()
        config["General"] = default_config.get("General")
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
    create()
