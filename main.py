from logging import exception
import sys
from urllib import request
from urllib.parse import urlparse, parse_qs
import requests
import time

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QMessageBox
)

from PyQt5 import QtGui
from MainWindow import Ui_MainWindow
from pytube import YouTube

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()

    def connectSignalsSlots(self):
        # self.URLLine
        self.PathButton.clicked.connect(self.selectFolder)
        self.URLButton.clicked.connect(self.validate_url)
        # self.PathLine
        self.DownloadButton.clicked.connect(self.download_mp4)
        self.DownloadMP3Button.clicked.connect(self.download_mp3)
        
    def selectFolder(self):
        target_folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        print(target_folder)
        if target_folder == "":
            return
        else:
            self.PathLine.setText(target_folder)
            self.URLLine.setEnabled(True)
            self.URLButton.setEnabled(True)
    
    def get_link_id(self, url):
        url_data = urlparse(url)
        video_id = parse_qs(url_data.query)['v'][0]
        print(video_id)
        return video_id
        
    def url_to_thumbnail(self, video_id):
        url = "https://img.youtube.com/vi/{}/maxresdefault.jpg".format(video_id)
        print(f"Thumbnail URL: {url}")
        data = request.urlopen(url).read()

        image = QtGui.QImage()
        image.loadFromData(data)

        lbl = self.ThumbnailPlaceholder
        lbl.setPixmap(QtGui.QPixmap(image))
    
    def validate_url(self):
        try:
            # check that the youtube url is valid
            url = self.URLLine.text()
            url_id = self.get_link_id(url)
            if requests.get(url).status_code != 200:
                pass
            else:
                self.url_to_thumbnail(url_id)  # put vids thumbnail in window
                
                video = YouTube(url)
                self.ThumbLabel.setText(f"Thumbnail preview ({video.title})")

                # always get both streams for simplicity
                self.DownloadButton.setEnabled(True)
                self.DownloadMP3Button.setEnabled(True)
        except Exception as e:
            return    
            
    def download_mp4(self):
        url = self.URLLine.text()
        video = YouTube(url).streams.filter(file_extension="mp4")
        video = video.get_by_itag(video[0].itag)
        video.download()
        self.DownloadButton.setEnabled(False)
    
    def download_mp3(self):
        url = self.URLLine.text()
        audio = YouTube(url).streams.filter(only_audio=True)
        print(audio)
        audio = audio.get_by_itag(audio[0].itag)
        audio.download(filename=f"{audio.title}.mp3")
        self.DownloadMP3Button.setEnabled(False)
                
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())