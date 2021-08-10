import os
import sys
import youtube_dl
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QThread, QDir
from PyQt6.QtWidgets import QApplication, QWidget, QFileDialog
from PyQt6.QtWidgets import QPushButton, QLabel, QLineEdit, QComboBox, QProgressBar, QVBoxLayout, QHBoxLayout

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.thread = QThread()
        self.thread.started.connect(self.download)

        self.createWindow()
        self.createWidgetsAndSetLayout()
    # end __init__()

    def createWindow(self):
        global app

        self.setWindowTitle('PyQt Youtube DL')
        self.setWindowIcon(QIcon('icons:youtube-icon-16.png'))

        width = int(app.primaryScreen().size().width() * 0.42)
        height = int(app.primaryScreen().size().height() * 0.069)
        self.setFixedSize(width, height)

        frame = self.frameGeometry()
        frame.moveCenter(app.primaryScreen().availableGeometry().center())
        self.move(frame.topLeft())
    # end createWindow()

    def createWidgetsAndSetLayout(self): # create widgets and set layout
        global application_path

        # v box init
        v_box = QVBoxLayout()

        # line 1
        label_url = QLabel('URL', self)
        self.le_url = QLineEdit()

        btn_file_path = QPushButton()
        btn_file_path.setIcon(QIcon('icons:choose-file-icon-16.png'))
        btn_file_path.clicked.connect(self.chooseFilePath)
        self.le_file_path = QLineEdit(application_path)
        self.le_file_path.setMaximumWidth(200)
        
        self.btn_download = QPushButton('Download', self)
        self.btn_download.clicked.connect(self.onClickDownloadButton)
        
        self.combo_box_file_type = QComboBox()
        self.combo_box_file_type.addItem('MP3')
        self.combo_box_file_type.addItem('MP4')

        h_box = QHBoxLayout()
        h_box.addWidget(label_url)
        h_box.addWidget(self.le_url)
        h_box.addWidget(btn_file_path)
        h_box.addWidget(self.le_file_path)
        h_box.addWidget(self.btn_download)
        h_box.addWidget(self.combo_box_file_type)
        
        v_box.addLayout(h_box)

        # line 2
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        v_box.addWidget(self.progress_bar)
        
        # set layout
        self.setLayout(v_box)
    # end createWidgetsAndSetLayout()

    def chooseFilePath(self):
        file_path = QFileDialog.getExistingDirectory()
        self.le_file_path.setText(file_path)
    # end chooseFilePath()

    def onClickDownloadButton(self):
        self.thread.start()
    # end onClickDownloadButton()

    def download(self):
        ydl_opts = {
            'outtmpl': self.le_file_path.text() + '/%(title)s.%(ext)s',
            'progress_hooks': [self.pHook],
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True
        }

        if self.combo_box_file_type.currentText() == 'MP3':
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3'
            }]
        else: ydl_opts['format'] = 'best' # MP4

        try: 
            print(f'download {self.combo_box_file_type.currentText()} from {self.le_url.text()}')
            self.btn_download.setEnabled(False)
            with youtube_dl.YoutubeDL(ydl_opts) as ydl: ydl.download([self.le_url.text()])
        except youtube_dl.utils.DownloadError or Exception as e:
            self.progress_bar.setValue(0)
        finally:
            self.btn_download.setEnabled(True)
            self.thread.terminate()
        # end try-except-finally
    # end download()

    def pHook(self, d):
        if d['status'] == 'downloading':
            percentage = int(float(d['_percent_str'].strip()[:-1]))
            self.progress_bar.setValue(percentage)
        elif d['status'] == 'finished':
            self.progress_bar.setValue(100)
            print('download completed')
        # end if-elif
    # end pHook()

# end class Window

if __name__ == '__main__':
    try:
        os.chdir(os.path.dirname(__file__))
        QDir.addSearchPath('icons', 'icons/')

        if getattr(sys, 'frozen', False): # for pyinstaller
            application_path = os.path.dirname(sys.executable)
            os.environ['QT_PLUGIN_PATH'] = os.path.dirname(__file__) + r'\plugins'
            os.environ['path'] += ';' + os.path.dirname(__file__) + r'\ffmpeg'
        else:
            application_path = os.path.dirname(__file__)

        app = QApplication([])
        window = Window()
        window.show()
        sys.exit(app.exec())
    except SystemExit as e:
        print(f'Exit with return code: {e}')
# end if