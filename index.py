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
        self.lineEdit_6.setText(str(os.path.join(os.path.expanduser('~'), 'Downloads')))
        pass

    def handleButtons(self):
        # handle all buttons in the app
        self.pushButton.clicked.connect(self.handleDownload)
        self.pushButton_2.clicked.connect(self.handleBrowse)
        self.pushButton_3.clicked.connect(self.getVideoData)
        self.pushButton_4.clicked.connect(self.saveBrowse)
        self.pushButton_5.clicked.connect(self.downloadVideo)
        self.pushButton_6.clicked.connect(self.playlistSaveBrowse)        
        self.pushButton_7.clicked.connect(self.playlistDownlaod)

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
                return True
        QMessageBox.information(
            self, "Download Completed", "The Download Completed Successfully")
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.progressBar.setValue(0)    

    #####################################
    ### Download Youtube Single Video ###
    #####################################

    def getVideoData(self):
        # https://youtu.be/Olhn7eEBnL8
        video_url = self.lineEdit_3.text()
        if video_url == "":
            QMessageBox.warning(self, "Data Error",
                                "Provide a valid video URL")
        else:
            video = pafy.new(video_url)
            # print(video.title)
            # print(video.duration)
            # print(video.author)
            # print(video.length)
            # print(video.viewcount)
            # print(video.likes)
            # print(video.dislikes)

            video_streams = video.videostreams
            for stream in video_streams:
                size = humanize.naturalsize(stream.get_filesize())
                data = "{} {} {} {}".format(
                    stream.mediatype, stream.extension, stream.quality, size)
                self.comboBox.addItem(data)

    def saveBrowse(self):
        # enable browser to our os, pick save location
        save_location = QFileDialog.getSaveFileName(
            self, caption="Save as", directory=".", filter="All Files(*.*)")
        print(save_location)
        self.lineEdit_4.setText(save_location[0])

    def downloadVideo(self):
        video_url = self.lineEdit_3.text()
        save_location = self.lineEdit_4.text()

        if video_url == "" or save_location == "":
            QMessageBox.warning(self, "Data Error",
                                "Provide a valid URL or save location")
        else:
            video = pafy.new(video_url)
            video_stream = video.videostreams
            # video_stream = video.streams
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
            current_video_stream = current_video.videostreams
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
def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
