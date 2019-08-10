from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.uic import loadUiType
import pafy
import humanize
import urllib.request
import os
from os import path
# import mainUI as ui
ui, _ = loadUiType('main.ui')



# class MainApp(QMainWindow, ui.Ui_MainWindow):
class MainApp(QMainWindow, ui):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.initUI()
        self.handleButtons()

    def initUI(self):
        # contain all ui change in loading
        if os.name == 'nt':
            pass
        else:
            self.lineEdit_6.setText(str(os.path.join(os.path.expanduser('~'), 'Downloads')))                    
        self.tabWidget.tabBar().setVisible(False)        
        self.moveBox1()
        self.moveBox2()
        self.moveBox3()
        self.moveBox4()

    def handleButtons(self):
        # handle all buttons in the app
        self.pushButton.clicked.connect(self.handleDownload)
        self.pushButton_2.clicked.connect(self.handleBrowse)
        self.pushButton_3.clicked.connect(self.getVideoData)
        self.pushButton_4.clicked.connect(self.saveBrowse)        
        self.pushButton_5.clicked.connect(self.downloadVideo)
        self.pushButton_6.clicked.connect(self.playlistSaveBrowse)        
        self.pushButton_7.clicked.connect(self.playlistDownlaod)

        self.pushButton_8.clicked.connect(self.openHome)        
        self.pushButton_9.clicked.connect(self.openDownload)        
        self.pushButton_10.clicked.connect(self.openYoutube)        
        self.pushButton_11.clicked.connect(self.openSettings)
        self.pushButton_12.clicked.connect(self.applyBlueTheme)        
        self.pushButton_13.clicked.connect(self.applyQDarkTheme)        
        self.pushButton_14.clicked.connect(self.applyDarkOrangeTheme)                
        self.pushButton_15.clicked.connect(self.resetTheme)        


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
                return None
        QMessageBox.information(
            self, "Download Completed", "The Download Completed Successfully")
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.progressBar.setValue(0)    

    #####################################
    ### Download Youtube Single Video ###
    #####################################

    def getVideoData(self,metadata):        
        video_url = self.lineEdit_3.text()
        if video_url == "":
            QMessageBox.warning(self, "Data Error",
                                "Provide a valid video URL")            
            return False
        else:
            video = pafy.new(video_url)            
            if metadata == True:                
                return "/{}.mp4".format(video.title)
            else:                
                video_streams = video.streams
                for stream in video_streams:
                    size = humanize.naturalsize(stream.get_filesize())
                    data = "{} {} {} {}".format(
                        stream.mediatype, stream.extension, stream.quality, size)
                    self.comboBox.addItem(data)            

    def saveBrowse(self):
        # enable browser to our os, pick save location        
        save_location = QFileDialog.getExistingDirectory(self, "Select Download Directory")        
        video_title = self.getVideoData(metadata=True)
        if(video_title != False):
            self.lineEdit_4.setText(save_location+video_title)        

    def downloadVideo(self):
        video_url = self.lineEdit_3.text()
        save_location = self.lineEdit_4.text()

        if video_url == "" or save_location == "":
            QMessageBox.warning(self, "Data Error",
                                "Provide a valid URL or save location")
        else:
            video = pafy.new(video_url)
            # video_stream = video.videostreams
            video_stream = video.streams
            video_quality = self.comboBox.currentIndex()
            # print(video_stream)
            download = video_stream[video_quality].download(
                filepath=save_location, callback=self.videoProgress)            

    def videoProgress(self, total, received, ratio, rate, time):
        read_data = received
        if total > 0:
            download_percentage = read_data * 100 / total
            self.progressBar_2.setValue(download_percentage)
            remaining_time = round(time/60, 2)
            self.label_5.setText(str("{} minutes remaining".format(remaining_time)))                                
            QApplication.processEvents()
            
    #########################################
    ### End Download Youtube Single Video ###
    #########################################

    ########################################
    ### Download Youtube Playlist Video ###
    ########################################

    def playlistDownlaod(self):
        playlist_url = self.lineEdit_5.text()
        save_location = self.lineEdit_6.text()

        if playlist_url == "" or save_location == "":        
            QMessageBox.warning(self, "Data Error",
                                "Provide a valid Playlist URL or save location")
        else:
            playlist = pafy.get_playlist(playlist_url)
            playlist_videos = playlist['items']
            self.lcdNumber_2.display(len(playlist_videos))
        os.chdir(save_location)
        if os.path.exists(playlist["title"]):
            os.chdir(str(playlist["title"]))
        else:
            os.mkdir(str(playlist["title"]))
            os.chdir(str(playlist["title"]))
        current_videos_in_download = 1
        quality = self.comboBox_2.currentIndex()                

        for video in playlist_videos:
            current_video = video['pafy']
            # current_video_stream = current_video.videostreams
            current_video_stream = current_video.streams
            download = current_video_stream[quality].download(callback=self.palylistProgress)
            self.lcdNumber.display(current_videos_in_download)            
            current_videos_in_download+=1
            QApplication.processEvents()
    
    def palylistProgress(self, total, received, ratio, rate, time):        
        read_data = received
        if total > 0:
            download_percentage = read_data * 100 / total
            self.progressBar_3.setValue(download_percentage)
            remaining_time = round(time/60, 2)
            self.label_6.setText(str("{} minutes remaining".format(remaining_time)))                                
            QApplication.processEvents()        
    
    def playlistSaveBrowse(self):
        playlist_save_location = QFileDialog.getExistingDirectory(self, "Select Download Directory")
        self.lineEdit_6.setText(playlist_save_location)
    ###########################################
    ### End Download Youtube Playlist Video ###
    ###########################################

    ###########################################
    ###      UI Navigation Method           ###
    ###########################################
    def openHome(self):
        self.tabWidget.setCurrentIndex(0)

    def openDownload(self):
        self.tabWidget.setCurrentIndex(1)

    def openYoutube(self):
        self.tabWidget.setCurrentIndex(2)

    def openSettings(self):
        self.tabWidget.setCurrentIndex(3)
    
    ###########################################
    ###      Theme Changes Method           ###
    ###########################################
    # Themes
    def resetTheme(self):
        self.setStyleSheet("")

    def applyBlueTheme(self):    
        self.resetTheme()
        styleFile = open("themes/blue.css")
        style = styleFile.read()
        self.setStyleSheet(style)

    def applyQDarkTheme(self):        
        self.resetTheme()
        styleFile = open("themes/qdark.css")
        style = styleFile.read()
        self.setStyleSheet(style)
    
    def applyDarkOrangeTheme(self):        
        self.resetTheme()
        styleFile = open("themes/dark_orange.css")
        style = styleFile.read()
        self.setStyleSheet(style)
    ###########################################
    ###     End Theme Changes Method        ###
    ###########################################

    ###########################################
    ###         App Animation               ###
    ###########################################

    def moveBox1(self):
        box_animation1 = QPropertyAnimation(self.groupBox, b'geometry')
        box_animation1.setDuration(1000)
        box_animation1.setStartValue(QRect(0,0,0,0))
        box_animation1.setEndValue(QRect(20,30,241,151))
        box_animation1.start()
        self.box_animation1 = box_animation1

    def moveBox2(self):
        box_animation2 = QPropertyAnimation(self.groupBox_2, b'geometry')
        box_animation2.setDuration(1000)
        box_animation2.setStartValue(QRect(0,0,0,0))
        box_animation2.setEndValue(QRect(330,30,231,151))
        box_animation2.start()
        self.box_animation2 = box_animation2

    def moveBox3(self):
        box_animation3 = QPropertyAnimation(self.groupBox_3, b'geometry')
        box_animation3.setDuration(1000)
        box_animation3.setStartValue(QRect(0,0,0,0))
        box_animation3.setEndValue(QRect(20,200,241,151))
        box_animation3.start()        
        self.box_animation3 = box_animation3

    def moveBox4(self):
        box_animation4 = QPropertyAnimation(self.groupBox_4, b'geometry')
        box_animation4.setDuration(1000)
        box_animation4.setStartValue(QRect(0,0,0,0))
        box_animation4.setEndValue(QRect(330,200,241,151))
        box_animation4.start()
        self.box_animation4 = box_animation4

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
