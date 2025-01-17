from src.View.widgets.HTextWidget import ScrollableHTextWidget
import ttkbootstrap as ttk


class ConfigGuide(ScrollableHTextWidget):
    def __init__(self, master, autohide=True, *args, **kwargs):
        super().__init__(master, autohide, *args, **kwargs)

        self.AddTitle("Documentación de Configuración de la Aplicación")

        self.AddText("Esta documentación detalla los parámetros de configuración utilizados en la aplicación. Cada sección describe las opciones disponibles y sus valores predeterminados, permitiendo personalizar el comportamiento de la aplicación según sea necesario. A continuación, se desglosan los parámetros agrupados por categoría.")

        self.AddSubtitle("General")

        self.AddBulletList([
            "encoding: Define la codificación utilizada por defecto. Valor predeterminado: utf-8.",
            "debug: Activa o desactiva el modo de depuración. Valor predeterminado: True.",
            "relevant_subjects_name: Formato para nombrar materias relevantes. Ejemplo: \"Materias relevantes para {}\".",
            "relevant_grades_name: Formato para nombrar promedios relevantes. Ejemplo: \"Promedio relevante para {}\".",
            "choice_name: Formato para identificar opciones. Ejemplo: \"Opción {}\".",
            "list_path_format: Formato para los nombres de las listas de alumnos. Ejemplo: \"Lista Alumnos {semestre}-{grupo}-{turno}.xlsx\"."
        ])

        self.AddSubtitle("Web")

        self.AddBulletList([
            "kardex_url: URL para acceder al sistema de consulta del kardex. Valor predeterminado: \"https://apps.cobachbcs.edu.mx/Sice/ReportesImpresos/wf_Rep_Kardex_ws.aspx\".",
            "cache_expire_after: Tiempo de expiración de la caché en segundos. Valor predeterminado: 72*60*60 (72 horas).",
            "kardex_cache_session_name: Nombre del archivo de sesión de caché para kardex. Valor predeterminado: \"cache/kardex\"."
        ])

        self.AddSubtitle("School")

        self.AddBulletList([
            "school_key: Clave única de la escuela. Valor predeterminado: \"03ECB0004K\".",
            "school_shift: Turno de la escuela. Valor predeterminado: \"M\" (matutino).",
            "packages: Lista de paquetes disponibles en la escuela. Valores predeterminados: \"Informática, Servicios turísticos, Dibujo arquitectónico, Contabilidad\".",
            "trainings: Capacitación ofrecida por la escuela. Valores predeterminados: \"Ciencias económico administrativas, Ciencias naturales, Ciencias exactas, Ciencias sociales y humanidades\".",
            "max_students_in_group: Máximo de estudiantes por grupo. Valor predeterminado: 45.",
            "groups: Número de grupos disponibles. Valor predeterminado: 4."
        ])

        self.AddSubtitle("Files")

        self.AddBulletList([
            "base_dir: Directorio base de la aplicación. Por defecto, el directorio actual de trabajo.",
            "config_dir: Ruta del archivo de configuración. Valor predeterminado: config.ini.",
            "data_dir: Directorio para almacenar datos. Valor predeterminado: data.",
            "reports_dir: Directorio para informes generados. Valor predeterminado: data/reports.",
            "lists_dir: Directorio para listas de estudiantes. Valor predeterminado: data/lists.",
            "curps_dir: Archivo con la lista de CURPs. Valor predeterminado: data/CURPS.txt.",
            "all_kardex_dir: Archivo JSON con todos los kardex. Valor predeterminado: data/allKardex.json.",
            "curp_report_dir: Informe de CURPs. Valor predeterminado: data/reports/curp_report.txt.",
            "output_dir: Directorio de salida para archivos generados. Valor predeterminado: output.",
            "logs_dir: Directorio para archivos de registro. Valor predeterminado: logs.",
            "assets_dir: Directorio para recursos gráficos y estáticos. Valor predeterminado: assets.",
            "kardex_data_dir: Archivo JSON con datos específicos de kardex. Valor predeterminado: data/kardexData.json.",
            "all_subjects_dir: Archivo Excel con todas las materias. Valor predeterminado: data/AllSubjects.xlsx.",
            "choices_dir: Archivo Excel con opciones de los estudiantes. Valor predeterminado: data/choices.xlsx.",
            "list_results_dir: Directorio para los resultados de listas generadas. Valor predeterminado: data/lists/results."
        ])

        self.AddSubtitle("Assets")

        self.AddBulletList([
            "logo_image_dir: Ruta del archivo de imagen del logotipo de la institución. Valor predeterminado: assets/images/cobach_logo.png."
        ])


if __name__ == "__main__":
    from src.View.widgets.AppWindow import AppWindow
    app = AppWindow()
    component = ConfigGuide(app)
    component.pack(fill=ttk.BOTH, expand=True)

    app.mainloop()
