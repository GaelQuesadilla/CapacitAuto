from src.View.widgets.HTextWidget import ScrollableHTextWidget
import ttkbootstrap as ttk


class ResultsCalculationGuide(ScrollableHTextWidget):
    def __init__(self, master, autohide=True, *args, **kwargs):
        super().__init__(master, autohide, *args, **kwargs)

        self.AddTitle("Documentación de la Vista 'Nuevos Grupos'")

        self.AddText("La vista 'Nuevos Grupos' permite calcular la asignación de alumnos a nuevos grupos basados en sus preferencias de materia y calificaciones. Esta funcionalidad es especialmente útil para docentes que deben organizar a los estudiantes en grupos para su capacitación. Los grupos se asignan en función de las opciones de materias preferidas de los alumnos, priorizando el promedio general y, en caso de empate, el promedio relevante de la capacitación correspondiente.")

        self.AddSubtitle("Componentes de la Vista")

        self.AddBulletList([
            "Barra de Acción: Contiene los botones para cargar, exportar y ver información del alumno. Además, incluye un botón adicional para calcular los nuevos grupos de acuerdo con los datos de los kardex disponibles.",
            "Botón Calcular Nuevos Grupos: Este botón abre una ventana emergente que permite al docente seleccionar el semestre sobre el cual se calcularán los grupos. El cálculo de los grupos se realiza en función de las opciones preferidas de los alumnos y sus calificaciones.",
            "Ventana de Selección de Semestre: Al hacer clic en el botón 'Calcular Nuevos Grupos', se despliega una ventana en la que el docente selecciona el semestre para el cual se calcularán los nuevos grupos. Este semestre será utilizado para obtener los kardex y determinar las asignaciones.",
            "Botón Aceptar: Después de seleccionar el semestre, el docente hace clic en 'Aceptar' para iniciar el proceso de cálculo de los grupos."
        ])

        self.AddSubtitle("Funcionalidades Principales")

        self.AddBulletList([
            "Cálculo Automático de Grupos: Al seleccionar un semestre y hacer clic en 'Aceptar', el sistema asignará automáticamente a los alumnos a los grupos, comenzando con su primera opción de materia. Si no hay espacio suficiente en el grupo, el estudiante será asignado a su segunda opción, luego a la tercera, y finalmente a la cuarta, repitiendo este proceso hasta un máximo de 10 intentos.",
            "Prioridad por Promedio General: Los alumnos se asignan a los grupos según su promedio general, priorizando a aquellos con mejores calificaciones. Esto asegura que los estudiantes más destacados sean asignados primero a sus opciones preferidas.",
            "Resolución de Empates: En caso de que varios alumnos tengan el mismo promedio general, se utiliza el promedio relevante de la capacitación (para la materia específica que desean cursar) para romper el empate y decidir quién será asignado primero a un grupo.",
            "Número Máximo de Intentos: El proceso de asignación se repite hasta un máximo de 10 intentos por alumno. Esto asegura que todos los alumnos tengan una oportunidad justa de ser colocados en un grupo, incluso si hay limitaciones de espacio."
        ])


if __name__ == "__main__":
    from src.View.widgets.AppWindow import AppWindow
    app = AppWindow()
    component = ConfigGuide(app)
    component.pack(fill=ttk.BOTH, expand=True)

    app.mainloop()
