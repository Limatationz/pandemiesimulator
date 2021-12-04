# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/about.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(406, 240)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(0, 0, 401, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 180, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_image = QtWidgets.QLabel(Dialog)
        self.label_image.setGeometry(QtCore.QRect(20, 70, 100, 100))
        self.label_image.setAutoFillBackground(False)
        self.label_image.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_image.setText("")
        self.label_image.setObjectName("label_image")
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(140, 50, 241, 171))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_version = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_version.setText("")
        self.label_version.setObjectName("label_version")
        self.verticalLayout.addWidget(self.label_version)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setTextFormat(QtCore.Qt.RichText)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.label_7 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_7.setTextFormat(QtCore.Qt.RichText)
        self.label_7.setWordWrap(True)
        self.label_7.setOpenExternalLinks(True)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_6.setTextFormat(QtCore.Qt.RichText)
        self.label_6.setOpenExternalLinks(True)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Über"))
        self.label.setText(_translate("Dialog", "Pandemiesimulator"))
        self.label_2.setText(_translate("Dialog",
                                        "<html><head/><body><p><span style=\" font-size:9pt;\">Icon made by </span><a href=\"https://www.freepik.com\"><span style=\" font-size:9pt; text-decoration: underline; color:#00afef;\">Freepik<br/></span></a><span style=\" font-size:9pt;\">from </span><a href=\"https://www.flaticon.com/\"><span style=\" font-size:9pt; text-decoration: underline; color:#00afef;\">www.flaticon.com</span></a></p></body></html>"))
        self.label_4.setText(_translate("Dialog",
                                        "Dieser Simulator soll den Verlauf einer Pandemie anhand ausgewählter Parameter darstellen."))
        self.label_5.setText(_translate("Dialog", "Autor: Erik Rill"))
        self.label_7.setText(_translate("Dialog",
                                        "<html><head/><body><p>Der Simulator wurde im Rahmen eines Bachelor-Praktikums an der <a href=\"https://uni-bayreuth.de\"><span style=\" text-decoration: underline; color:#00afef;\">Universität Bayreuth</span></a> erstellt.</p></body></html>"))
        self.label_6.setText(_translate("Dialog",
                                        "<html><head/><body><p>Betreuerin: <a href=\"http://www.ai1.uni-bayreuth.de/en/team/Greiner_Sandra/index.php\"><span style=\" text-decoration: underline; color:#00afef;\">Sandra Greiner</span></a></p></body></html>"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
