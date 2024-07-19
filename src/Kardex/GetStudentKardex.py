from src.Config import Config
import requests


def GetStudentKardex(curp: str):
    """Fetches the kardex information for a student using their CURP.

    Parameters
    ----------
    curp : str
        The student's CURP (Clave Única de Registro de Población).

    Returns
    -------
    response: request.Response
        The Http response object containing the student's kardex page.
    """
    base_url = Config.read("Web", "kardex_url")
    base_params = {
        "curpAlumno": curp,
        "clavePlantel": Config.read("School", "school_key"),
        "turno": Config.read("School", "school_shift"),
    }

    response = requests.get(base_url, params=base_params)

    return response


if __name__ == "__main__":
    pass
