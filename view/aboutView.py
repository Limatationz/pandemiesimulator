"""
    Element of the view.
    Contains the AboutView class.
"""

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from view.aboutWindow import Ui_Dialog


class AboutView(QtWidgets.QMainWindow, Ui_Dialog):
    """An AboutView which shows the aboutWindow."""

    def __init__(self):
        """Inits the AboutView."""
        super(AboutView, self).__init__()
        self.setupUi(self)
        pixmap = QPixmap('resources/images/icon.png')
        smaller_icon = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.label_image.setPixmap(smaller_icon)
        self.label_version.setText("Version: 1.0")

    def change_lang(self):
        """Changes the language of the window."""
        self.retranslateUi(self)
