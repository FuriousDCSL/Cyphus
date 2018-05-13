import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from mainWindow import Ui_MainWindow

class AppWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

if __name__ == "__main__":

    QtCore.QCoreApplication.setApplicationName("Cyphus")
    QtCore.QCoreApplication.setApplicationVersion("0.01pa")
    QtCore.QCoreApplication.setOrganizationName("DCSL")
    QtCore.QCoreApplication.setOrganizationDomain("http://dcsl.me")

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = AppWindow()
    ui.show()
    sys.exit(app.exec_())
