from PyQt6.QtWidgets import QApplication
import sys
from test import ui_wds

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = ui_wds()
    ui.show()
    sys.exit(app.exec())
