from src.View.widgets.HTextWidget import ScrollableHTextWidget
import ttkbootstrap as ttk


class CurpManagementGuide(ScrollableHTextWidget):
    def __init__(self, master, autohide=True, *args, **kwargs):
        super().__init__(master, autohide, *args, **kwargs)

        self.AddTitle("Documentación de la Vista 'Administración de CURPS'")

        self.AddText("La vista 'Administración de CURPS' permite gestionar los CURPs de los estudiantes y consultar información relacionada con sus kardex. Esta interfaz está diseñada para cargar, verificar y solicitar los kardex de manera eficiente, mostrando el estado actual de cada CURP y cualquier error asociado.")

        self.AddSubtitle("Componentes de la Vista")

        self.AddBulletList([
            "Encabezado de la Vista: Contiene el título 'Administración de CURPS' y botones de acción como 'Exportar archivo', 'Cargar CURPs desde archivo' y 'Solicitar kardex'.",
            "Tabla de Datos: Muestra la información organizada en columnas como 'No.', 'CURP', 'Nombre', 'Semestre' y 'Estado', con CURPs inválidos resaltados en rojo."
        ])

        self.AddSubtitle("Funcionalidades Principales")

        self.AddBulletList([
            "Validación de CURPs: Se muestra el resultado de la petición al Kardex, este puede ser 'No solicitado', 'CURP no valida' y 'kardex solicitado'",
            "Carga y Exportación de Datos: Se pueden cargar CURPs desde un archivo de texto (*.txt) en el que se especifique en cada línea una CURP, y exportar la lista con sus estados.",
            "Solicitud de Kardex: Permite solicitar y guardar los Kardex"
        ])

        self.AddSubtitle("Indicadores Visuales")

        self.AddBulletList([
            "Resaltado Rojo: Aquellas CURPS cuya petición al Kardex haya sido rechazada se mostrarán con un fondo rojo",
            "Resaltado Amarillo: CURPs que no han sido solicitadas en el archivo local de Kardex se mostrarán con un fondo color amarillo",
        ])

        self.AddSubtitle("Casos de Uso")

        self.AddBulletList([
            "Gestión masiva de CURPs: Permite importar grandes volúmenes de CURPs y verificar su disponibilidad.",
            "Verificación de Kardex: Facilita la solicitud de kardex para múltiples estudiantes.",
            "Identificación de Errores: CURPs incorrectos son fácilmente identificables para su corrección."
        ])


if __name__ == "__main__":
    from src.View.widgets.AppWindow import AppWindow
    app = AppWindow()
    component = CurpManagementGuide(app)
    component.pack(fill=ttk.BOTH, expand=True)

    app.mainloop()
