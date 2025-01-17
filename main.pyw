from src.View.App import App
import os
import sys
from src.Controller.controllers.report import report

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

if __name__ == "__main__":
    try:
        app = App()
        app.mainloop()
    except Exception as e:
        report()
