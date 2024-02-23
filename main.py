import sys
import os
from functools import partial

from PySide6.QtCore import QStandardPaths, QSize
from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QStyle, QFileDialog
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget

NOM_QSS = "" #entrer le nom du fichier QSS à appliquer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("PyPlayer")
        
        self.open_icon = self.style().standardPixmap(QStyle.StandardPixmap.SP_DriveDVDIcon)
        self.play_icon = self.style().standardPixmap(QStyle.StandardPixmap.SP_MediaPlay)
        self.previous_icon = self.style().standardPixmap(QStyle.StandardPixmap.SP_MediaSkipBackward)
        self.pause_icon = self.style().standardPixmap(QStyle.StandardPixmap.SP_MediaPause)
        self.stop_icon = self.style().standardPixmap(QStyle.StandardPixmap.SP_MediaStop)
        
        self.setup_ui()
        
    def setup_ui(self):
        self.create_widgets()
        self.create_layouts()
        self.modify_widgets()
        self.add_widgets_to_layouts()
        self.setup_connections()
            
    def create_widgets(self):
        self.video_widget = QVideoWidget()
        self.audio_widget = QAudioOutput()
        self.player = QMediaPlayer()
        self.tool_bar = QToolBar()
        self.file_menu = self.menuBar().addMenu("Fichier")
        
        #ACTIONS
        self.act_open = self.file_menu.addAction(self.open_icon, "Ouvrir")
        self.act_open.setShortcut("Ctrl+O")
        self.act_play = self.tool_bar.addAction(self.play_icon, "Lire")
        self.act_pause = self.tool_bar.addAction(self.pause_icon, "Pause")
        self.act_previous = self.tool_bar.addAction(self.previous_icon, "Revenir au début")
        self.act_stop= self.tool_bar.addAction(self.stop_icon, "Stop")
        
    def create_layouts(self):
        pass
        
    def modify_widgets(self):
        if NOM_QSS:
            dos_pars = os.path.dirname(__file__)
            fichier_qss = os.path.join(dos_pars, NOM_QSS)
            with open(fichier_qss ,"r") as f:
                qss = f.read()
                self.setStyleSheet(qss)
    
    def add_widgets_to_layouts(self):
        self.addToolBar(self.tool_bar)
        self.setCentralWidget(self.video_widget)
        self.player.setAudioOutput(self.audio_widget)
        self.player.setVideoOutput(self.video_widget)
    
    def setup_connections(self):
        self.act_open.triggered.connect(self.open)
        self.act_play.triggered.connect(self.player.play)
        self.act_pause.triggered.connect(self.player.pause)
        self.act_stop.triggered.connect(self.player.stop)
        self.act_previous.triggered.connect(partial(self.player.setPosition, 0))
        self.player.playbackStateChanged.connect(self.update_buttons)
        
        
    # à partir d'ici les autres fonctions du programme
    def update_buttons(self,state):
        self.act_play.setDisabled(state == QMediaPlayer.PlaybackState.PlayingState)
        self.act_pause.setDisabled(state == QMediaPlayer.PlaybackState.PausedState)
        self.act_stop.setDisabled(state == QMediaPlayer.PlaybackState.StoppedState)
        
    def play(self):
        self.player.play()
        self.video_widget.resize(QSize(1, 1))
           
    def open(self):
        file_dialog = QFileDialog(self)
        file_dialog.setMimeTypeFilters(["video/mp4"])
        movies_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.MoviesLocation)
        file_dialog.setDirectory(movies_dir)
        if file_dialog.exec() and file_dialog.selectedUrls():
            movie = file_dialog.selectedUrls()[0]
            self.player.setSource(movie)
            self.player.play()
       
app = QApplication(sys.argv)
win = MainWindow()
win.show()
app.exec()