import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import *
from PySide6.QtGui import QFontDatabase, QFont
from multiprocessing import freeze_support
from InterfaceControl import InterfaceControl


if __name__ == '__main__':
    freeze_support()
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    fontDB = QFontDatabase()
    fontDB.addApplicationFont('Font/NanumSquareRoundL.ttf')
    app.setFont(QFont('NanumSquareRoundL', 9))
    
    ex = InterfaceControl()
    ex.show()
    sys.exit(app.exec_())
