from src.View.widgets.HTextWidget import ScrollableHTextWidget
import ttkbootstrap as ttk


class ListsGuide(ScrollableHTextWidget):
    def __init__(self, master, autohide=True, *args, **kwargs):
        super().__init__(master, autohide, *args, **kwargs)

        self.AddTitle("Documentación de la Vista 'Lista de Alumnos'")

        self.AddText("La vista 'Lista de Alumnos' permite gestionar la información de los estudiantes, facilitando la visualización de sus datos personales y académicos. Esta vista es útil para docentes que necesitan consultar y exportar información de los alumnos de manera eficiente. Además, el usuario docente puede ver la lista de estudiantes seleccionados en función de un semestre o grupo específico.")

        self.AddSubtitle("Componentes de la Vista")

        self.AddBulletList([
            "Barra de Acción: Contiene los botones para cargar un archivo, exportar un archivo y ver la información de un alumno. Es importante notar que no se recomienda utilizar la opción de cargar archivo, ya que las listas de alumnos se generan automáticamente al solicitar los kardex en la vista de Administración de CURPs.",
            "Botón Cargar Archivo: Permite cargar un archivo con la lista de alumnos, pero esta acción no es necesaria, ya que las listas se generan automáticamente en el proceso de solicitud de kardex.",
            "Botón Exportar Archivo: Permite exportar la lista de alumnos en un formato que puede ser modificado o utilizado en otras aplicaciones como Excel o Google Sheets.",
            "Botón Ver Información del Alumno: Al hacer clic en este botón, se abrirá una ventana emergente que muestra la información detallada del alumno seleccionado.",
            "Selector de Lista: En la parte superior de la vista, se encuentra un selector en el que puedes elegir entre las listas disponibles de alumnos. Esto permite al docente ver la lista correspondiente al semestre o grupo que necesite consultar."
        ])

        self.AddSubtitle("Funcionalidades Principales")

        self.AddBulletList([
            "Generación Automática de Listas: Las listas de alumnos se generan automáticamente al solicitar los kardex desde la vista de Administración de CURPs. Esto elimina la necesidad de cargar archivos manualmente, lo que optimiza el proceso de gestión.",
            "Visualización de Información Detallada: Al seleccionar un alumno y hacer clic en 'Ver Información del Alumno', se abre una ventana emergente con los datos personales y académicos del estudiante, como nombre, promedio y las materias en las que está inscrito.",
            "Exportación de Listas: La opción 'Exportar Archivo' permite al docente generar un archivo con la lista de alumnos, que puede ser utilizado para reportes, análisis o registros externos en programas como Excel o Google Sheets.",
            "Selección de Lista: El selector de lista permite elegir entre diversas listas disponibles de alumnos, como las listas correspondientes a distintos semestres o grupos, asegurando que se pueda acceder rápidamente a la información específica que se necesita."
        ])

        self.AddSubtitle("Casos de Uso")

        self.AddBulletList([
            "Consulta de listas: Un docente necesita consultar la lista de alumnos de un semestre específico. Puede seleccionar la lista desde el selector en la parte superior, visualizar las materias correspondientes y revisar el desempeño académico de cada estudiante.",
            "Consulta de calificaciones: Un docente quiere ver información detallada sobre un estudiante en particular, como su promedio y materias inscritas. Para esto, selecciona al alumno y hace clic en el botón 'Ver Información del Alumno', obteniendo los datos relevantes en una ventana emergente."
        ])


if __name__ == "__main__":
    from src.View.widgets.AppWindow import AppWindow
    app = AppWindow()
    component = ListsGuide(app)
    component.pack(fill=ttk.BOTH, expand=True)

    app.mainloop()
