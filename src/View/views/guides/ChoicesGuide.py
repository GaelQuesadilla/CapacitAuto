from src.View.widgets.HTextWidget import ScrollableHTextWidget
import ttkbootstrap as ttk


class ChoicesGuide(ScrollableHTextWidget):
    def __init__(self, master, autohide=True, *args, **kwargs):
        super().__init__(master, autohide, *args, **kwargs)

        self.AddTitle("Documentación de la Vista 'Elecciones del Alumno'")

        self.AddText("La vista 'Elecciones del Alumno' permite gestionar las elecciones realizadas por los estudiantes en cuanto a su capacitación o paquete. En esta vista, se muestra una tabla con la lista de los estudiantes ordenada acorde a su CURP, semestre, grupo, turno y nombre, junto con las opciones elegidas por cada alumno. Según el semestre, los alumnos deben seleccionar entre opciones de capacitación o paquetes, y estas elecciones se reflejan en la tabla.")

        self.AddSubtitle("Componentes de la Vista")

        self.AddBulletList([
            "Barra de Acción: Contiene las opciones para generar, cargar y exportar el archivo con las elecciones de los estudiantes.",
            "Tabla de Elecciones: Muestra las columnas 'CURP', 'Semestre', 'Grupo', 'Turno', 'Nombre' y las opciones seleccionadas por el estudiante.",
        ])

        self.AddSubtitle("Funcionalidades Principales")

        self.AddBulletList([
            "Carga de Elecciones: Permite cargar un archivo con las elecciones realizadas por los estudiantes.",
            "Exportación de Elecciones: Exporta las elecciones de los estudiantes para su revisión o modificación externa.",
            "Generación de Archivos: Si el archivo no existe o desea reiniciarlo, se genera uno nuevo sin las elecciones de los estudiantes."
        ])

        self.AddSubtitle("Columna de Elecciones")

        self.AddBulletList([
            "Columnas 'CURP', 'Semestre', 'Grupo', 'Turno' y 'Nombre': Estas columnas muestran los datos personales de cada estudiante.",
            "Columnas de Opciones: En función del semestre, los estudiantes deben seleccionar opciones de capacitación o paquete y el docente deberá de subir el archivo correspondiente",
            "- Primer y segundo semestre: Debe llenar las opciones correspondientes a capacitación.",
            "- Tercer y cuarto semestre: Debe llenar las opciones correspondientes a su paquete."
        ])

        self.AddSubtitle("Elección por Paquete o Capacitación")

        self.AddBulletList([
            "Si el estudiante está en primer o segundo semestre, deberá elegir opciones dentro de los paquetes de capacitación disponibles.",
            "Si el estudiante está en tercer o cuarto semestre, deberá elegir dentro de los paquetes acordes a su ciclo académico.",
            "Las elecciones deben ser indicadas en las columnas correspondientes, por ejemplo, 'Elección Contabilidad', 'Elección Turismo', etc."
        ])

        self.AddSubtitle("Orden de Preferencia de Opciones")

        self.AddBulletList([
            "Para cada materia/paquete, el estudiante debe escribir un número del 1 al 4 en la columna correspondiente:",
            "- '1' para la primera opción.",
            "- '2' para la segunda opción.",
            "- '3' para la tercera opción.",
            "- '4' para la cuarta opción.",
            "Esto permite organizar las opciones del estudiante de acuerdo con su preferencia de manera jerárquica."
        ])

        self.AddSubtitle("Flujo de Trabajo")

        self.AddBulletList([
            "1. Generación del Archivo: Si no existe un archivo de elecciones, se genera uno con las opciones predeterminadas.",
            "2. Modificación del Archivo: Los docentes o responsables del proceso deben completar las elecciones de acuerdo con el semestre y la especialización del estudiante.",
            "3. Carga de Archivo: El archivo modificado se carga de nuevo en el sistema para su procesamiento."
        ])

        self.AddSubtitle("Casos de Uso")

        self.AddBulletList([
            "Gestión de Elecciones: Los estudiantes eligen sus opciones de capacitación o paquete, y estas elecciones son gestionadas y procesadas.",
            "Asignación de Preferencias: Las preferencias se reflejan en el orden de las opciones seleccionadas (1, 2, 3, 4).",
            "Modificación y Carga de Datos: Los archivos de elecciones se pueden modificar y cargar nuevamente en el sistema."
        ])


if __name__ == "__main__":
    from src.View.widgets.AppWindow import AppWindow
    app = AppWindow()
    component = ChoicesGuide(app)
    component.pack(fill=ttk.BOTH, expand=True)

    app.mainloop()
