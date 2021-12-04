"""
    Contains the main function
"""

import sys

from PyQt5 import QtCore
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import QApplication

from presenter.presenter import Presenter
from resources.style import breeze_resources

if __name__ == '__main__':
    """ Creates the app and shows the GUI with the stylesheet
        requirements:
        - pyqtgraph (0.11.1)
        - pyqtchart (5.13.1 !important)
        - optional: PyQtWebEngine (5.15.3
    """
    # prevents an error caused by the QWebEngineView
    try:
        from PyQt5.QtWebEngineWidgets import QWebEngineView
        QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    except:
        QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)

    app = QApplication(sys.argv)

    # Sets the stylesheet
    file = QFile(":/dark.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())

    # Creates the simulator ans shows the view
    presenter = Presenter()
    presenter.ui.show()

    sys.exit(app.exec_())
