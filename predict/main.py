from PyQt6.QtWidgets import QApplication        # pip install PyQt6 -i https://pypi.tuna.tsinghua.edu.cn/simple
import sys
from ui_wds import ui_wds



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = ui_wds()
    ui.ui.show()
    sys.exit(ui.app.exec())