"""
    Element of the view.
    Contains the DocView class.
"""

import os

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QMainWindow


class DocView(QMainWindow):
    """A DocView which shows the documentation inside a WebEngine."""

    def __init__(self):
        """Inits the DocView."""
        super(DocView, self).__init__()

        from PyQt5.QtWebEngineWidgets import QWebEngineView
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('file://' + os.path.realpath('doc/Pandemic-Simulator/index.html')))
        self.setCentralWidget(self.browser)
