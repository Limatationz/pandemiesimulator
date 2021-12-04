"""
    Element of the view.
    Contains the AnimatedToggle class.
    Creates an animated Toggle instead of a Checkbox.
    Source: https://www.learnpyqt.com/tutorials/qpropertyanimation/
"""

from PyQt5.QtCore import (
    QSize, QPoint, QPointF, QRectF,
    QEasingCurve, QPropertyAnimation,
    pyqtSlot, pyqtProperty)
from PyQt5.QtGui import QBrush, QPaintEvent, QPen, QPainter
from PyQt5.QtWidgets import QCheckBox

from constants import *


class AnimatedToggle(QCheckBox):
    """
        An AnimatedToggle which replaces a QCheckbox.

        Attributes
        ----------
        _bar_brush: QBrush
            contains the brush for the bar
        _bar_checked_brush: QBrush
            contains the brush for the bar when the toggle is checked
        _bar_disabled_brush: QBrush
            contains the brush for the bar when the toggle is disabled
        _bar_disabled_checked_brush: QBrush
            contains the brush for the bar when the toggle is checked and disabled
        _handle_brush: QBrush
            contains the brush for the handle
        _handle_checked_brush: QBrush
            contains the brush for the handle when the toggle is checked
        _handle_disabled_brush: QBrush
            contains the brush for the handle when the toggle is disabled
        _handle_disabled_checked_brush: QBrush
            contains the brush for the handle when the toggle is checked and disabled
        _handle_position: int
            contains the position of the handle
        animation: QPropertyAnimation
            contains the animation of the toggle
    """
    _transparent_pen = QPen(COLOR_TOGGLE_HANDLE)
    _light_grey_pen = QPen(COLOR_TOGGLE_HANDLE_DISABLED)
    _dark_grey_pen = QPen(COLOR_TOGGLE_HANDLE)

    def __init__(self, parent=None) -> None:
        """Inits the AnimatedToggle.

        Parameters
        ----------
        parent: QCheckBox
            parent of the toggle
        """
        super().__init__(parent)

        self._bar_brush = QBrush(COLOR_TOGGLE_NOT_CHECKED)
        self._bar_checked_brush = QBrush(COLOR_TOGGLE_CHECKED)
        self._bar_disabled_brush = QBrush(COLOR_TOGGLE_DISABLED)
        self._bar_disabled_checked_brush = QBrush(COLOR_TOGGLE_CHECKED_DISABLED)

        self._handle_brush = QBrush(COLOR_TOGGLE_HANDLE)
        self._handle_checked_brush = QBrush(COLOR_TOGGLE_HANDLE)
        self._handle_disabled_brush = QBrush(COLOR_TOGGLE_HANDLE_DISABLED)
        self._handle_disabled_checked_brush = QBrush(COLOR_TOGGLE_HANDLE_DISABLED)

        self.setContentsMargins(0, 0, 0, 0)
        self._handle_position = 0

        self.animation = QPropertyAnimation(self, b"handle_position", self)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.animation.setDuration(200)

        self.stateChanged.connect(self.setup_animation)

    def sizeHint(self) -> None:
        """Returns the size of the hint"""
        return QSize(58, 18)

    def hitButton(self, pos: QPoint):
        """Returns the position of the handle

        Returns
        -------
            contentsRect().contains(pos)
        """
        return self.contentsRect().contains(pos)

    @pyqtSlot(int)
    def setup_animation(self, value: int) -> None:
        """Setup the animation

        Parameters
        ----------
        value: int
            position of the handle
        """
        self.animation.stop()
        if value:
            self.animation.setEndValue(1)
        else:
            self.animation.setEndValue(0)
        self.animation.start()

    def paintEvent(self, e: QPaintEvent) -> None:
        """ Paints the AnimatedToggle.

        Parameters
        ----------
        e: QPaintEvent
            Paintevent

        """

        contRect = self.contentsRect()
        handleRadius = round(0.30 * contRect.height())

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        p.setPen(self._transparent_pen)
        barRect = QRectF(
            0, 0,
            contRect.width() - handleRadius, 0.90 * contRect.height()
        )
        barRect.moveCenter(contRect.center())
        rounding = barRect.height() / 2

        # the handle will move along this line
        trailLength = contRect.width() - 4 * handleRadius

        xPos = contRect.x() + handleRadius + trailLength * self._handle_position + 0.9 * handleRadius

        if self.isEnabled():
            if self.isChecked():
                p.setBrush(self._bar_checked_brush)
                p.drawRoundedRect(barRect, rounding, rounding)
                p.setBrush(self._handle_checked_brush)

            else:
                p.setBrush(self._bar_brush)
                p.drawRoundedRect(barRect, rounding, rounding)
                p.setPen(self._dark_grey_pen)
                p.setBrush(self._handle_brush)
        else:
            p.setPen(self._light_grey_pen)
            if self.isChecked():
                p.setBrush(self._bar_disabled_checked_brush)
                p.drawRoundedRect(barRect, rounding, rounding)
                p.setBrush(self._handle_disabled_brush)

            else:
                p.setBrush(self._bar_disabled_brush)
                p.drawRoundedRect(barRect, rounding, rounding)
                p.setBrush(self._handle_disabled_brush)

        p.drawEllipse(
            QPointF(xPos, barRect.center().y()),
            handleRadius, handleRadius)

        p.end()

    @pyqtProperty(float)
    def handle_position(self) -> int:
        """ Returns the position of the handle

        Returns
        -------
        int:
            position of the handle
        """
        return self._handle_position

    @handle_position.setter
    def handle_position(self, pos: int) -> None:
        """Sets the position of the handle and updates the AnimatedToggle

        Parameters
        ----------
        pos: int
            new position of the handle
        """
        self._handle_position = pos
        self.update()
