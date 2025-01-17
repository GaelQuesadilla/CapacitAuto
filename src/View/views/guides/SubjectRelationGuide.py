from src.View.widgets.HTextWidget import ScrollableHTextWidget
import ttkbootstrap as ttk


class SubjectRelationGuide(ScrollableHTextWidget):
    def __init__(self, master, autohide=True, *args, **kwargs):
        super().__init__(master, autohide, *args, **kwargs)

        self.AddTitle("Documentación de la Vista 'Relación de Materias'")

        self.AddText("La vista 'Relación de Materias' permite visualizar y gestionar las materias disponibles para cada semestre, así como las materias relevantes que se deben tomar en cuenta para la capacitación o paquete correspondiente. A través de esta vista, el usuario docente puede cargar, exportar y generar un archivo con la información de las materias y sus respectivas relaciones. El archivo generado se puede modificar externamente mediante aplicaciones como Excel, google sheets u Open Office para definir las materias relevantes que se tomarán en cuenta para cada capacitación.")

        self.AddSubtitle("Componentes de la Vista")

        self.AddBulletList([
            "Barra de Acción: Contiene los botones para cargar, exportar o generar el archivo (el archivo que se generará solo contentrá las materias disponibles, no se incluirán datos de la relación de materias).",
            "Columnas de Materias: Hay seis columnas donde se muestran las materias disponibles para cada semestre de acuerdo a los datos obtenidos de los kardex.",
            "Columnas de Materias Relevantes: Columnas adicionales en las que se deben ingresar las materias relevantes para cada capacitación o paquete, de acuerdo con las especificaciones del docente."
        ])

        self.AddSubtitle("Funcionalidades Principales")

        self.AddBulletList([
            "Carga de Datos: Permite cargar un archivo que contenga la relación de materias con los datos correspondientes.",
            "Exportación de Datos: Los datos se pueden exportar para su modificación en programas externos como Excel, Google Sheets u Open Office.",
            "Generación de Archivos: Si el archivo no existe, se puede generar uno nuevo con los datos correspondientes.",

        ])

        self.AddSubtitle("Flujo de Trabajo")

        self.AddBulletList([
            "1. Generación del Archivo: En caso de que no exista el archivo será necesario generar uno nuevo archivo mediante el botón 'Generar archivo'",
            "2. Modificación Externa: El archivo generado puede ser exportado mediante el botón 'Exportar archivo' para su posterior modificación en Excel, Google Sheets u Open Office para que los docentes especifiquen las materias relevantes.",
            "3. Carga de Archivo Modificado: Después de realizar las modificaciones necesarias, el archivo se carga nuevamente en el sistema para su integración y uso posterior mediante el botón 'Cargar archivo'."
        ])

        self.AddSubtitle("Casos de Uso")

        self.AddBulletList([
            "Definición de Materias Relevantes: Los docentes especifican qué materias se consideran relevantes para cada paquete de capacitación.",
            "Gestión de Datos de Materias: Permite la administración de las materias disponibles y su relación con las materias relevantes a lo largo de los semestres.",
            "Generación y Modificación de Archivos: Facilita la creación de un archivo que puede ser modificado externamente para personalizar la relación de materias.",
            "En caso de que el usuario docente decida no utilizar relación de materias relevantes deberá de generar el archivo y no modificarlo"
        ])


if __name__ == "__main__":
    from src.View.widgets.AppWindow import AppWindow
    app = AppWindow()
    component = SubjectRelationGuide(app)
    component.pack(fill=ttk.BOTH, expand=True)

    app.mainloop()
