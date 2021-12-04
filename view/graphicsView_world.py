"""
    Element of the view.
    Contains the GraphicsViewWorld class.
    Emits a signal when the view is resized with the old and new size.
"""

from PyQt5 import QtCore
from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QGraphicsView


class GraphicsViewWorld(QGraphicsView):
    """ A GraphicsViewWorld Widget which replaces a QGraphicsView."""
    sizeChanged = QtCore.pyqtSignal(int, int, int, int)  # is emitted when the size changed

    def __init__(self, parent=None) -> None:
        """Inits the GraphicsViewWorld

        Parameters
        ----------
        parent: QGraphicsView
            parent
        """
        QGraphicsView.__init__(self, parent)

    def resizeEvent(self, event: QEvent) -> None:
        """Custom resizeEvent which is called when the view is resized and emits a QSignal.

        Parameters
        ----------
        event: QEvent
        """
        self.sizeChanged.emit(event.oldSize().width(), event.oldSize().height(), event.size().width(),
                              event.size().height())
