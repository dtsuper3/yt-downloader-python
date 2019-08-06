from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.uic import loadUiType
import urllib.request

ui, _ = loadUiType('main.ui')


class MainApp(QMainWindow, ui):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.initUI()
        self.handleButtons()

    def initUI(self):
        # contain all ui change in loading
        pass

    def handleButtons(self):
        # handle all buttons in the app
        self.pushButton.clicked.connect(self.handleDownload)
        self.pushButton_2.clicked.connect(self.handleBrowse)

    def handleProgress(self, blocknum, blocksize, totalsize):
        # calculate the progress
        readed_data = blocknum * blocksize
        if totalsize > 0:
            download_percentage = readed_data * 100 / totalsize
            self.progressBar.setValue(download_percentage)
            QApplication.processEvents()

    def handleBrowse(self):
        # enable browser to our os, pick save location
        save_location = QFileDialog.getSaveFileName(
            self, caption="Save as", directory=".", filter="All Files(*.*)")
        print(save_location)
        self.lineEdit_2.setText(save_location[0])

    def handleDownload(self):
        # downloading any file
        download_url = self.lineEdit.text()
        save_location = self.lineEdit_2.text()

        if download_url == "" or save_location == "":
            QMessageBox.warning(self, "Data Error",
                                "Provide a valid URL or save location")
        else:
            try:
                urllib.request.urlretrieve(
                    download_url, save_location, self.handleProgress)
            except Exception:
                QMessageBox.warning(self, "Download Error",
                                    "Provide a valid URL or save location")
                return
        QMessageBox.information(
            self, "Download Completed", "The Download Completed Successfully")
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.progressBar.setValue(0)

    def saveBrowse(self):
        # save location in the line edit
        pass


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
