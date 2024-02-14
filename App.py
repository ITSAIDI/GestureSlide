import sys
from PyQt5 import  QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QStackedWidget,QLabel
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap,QMovie,QColor,QDesktopServices,QFont
from Stream import Present,Is_Blank
from PyQt5.QtCore import QTimer,QUrl
import cv2



class SplashScreen(QDialog):
    finished = QtCore.pyqtSignal()
    

    def __init__(self):
        super(SplashScreen, self).__init__()
        loadUi("Splash.ui", self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.addImage()
        self.addGIF()
        
    def Show(self):
        self.show()
        
    def addImage(self):
        image_pxmap = QPixmap('In_Progress.png')
        self.Background_Label.setPixmap(image_pxmap)

    def progress(self):
        self.ProgressBar.setValue(0)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(30)

    def update_progress(self):
        value = self.ProgressBar.value()
        if value < 100:
            value += 1
            self.ProgressBar.setValue(value)
        else:
            self.timer.stop()
            self.finish()
    
    def addGIF(self):
            gif_movie = QMovie('Message.gif')
            gif_label = self.Gif_Label
            gif_label.setMovie(gif_movie)
            gif_movie.start()
            
    def finish(self):
        self.close()
        self.finished.emit()
#######################################################################################
#######################################################################################
class Device_Selection(QDialog):
    
    PC_Camera_Signal = QtCore.pyqtSignal()
    Externel_Camera_Signal = QtCore.pyqtSignal()

    def __init__(self):
        super(Device_Selection, self).__init__()
        loadUi("Select_Device.ui", self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.addImage()
        
        self.PC_Box.stateChanged.connect(self.handle_PC_Box)
        self.Externel_Box.stateChanged.connect(self.handle_Externel_Box)
        
    def handle_PC_Box(self):
        # Emit the finished signal when the QCheckBox state changes
        self.PC_Camera_Signal.emit()
        self.close()
        
    def handle_Externel_Box(self):
        self.Externel_Camera_Signal.emit()
        self.close()
        
    def Show(self):
        self.show()
        
    def addImage(self):
        image_pxmap = QPixmap('Device_Selection.png')
        self.Background_Label.setPixmap(image_pxmap)
         
#######################################################################################
#######################################################################################

class Steps_Iriun(QDialog):
    
    Forward_Signal = QtCore.pyqtSignal()
    Back_signal    = QtCore.pyqtSignal()
    #Change_Signal  = QtCore.pyqtSignal()
    
    def __init__(self):
        super(Steps_Iriun, self).__init__()
        loadUi("Steps_iriun.ui", self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.addImage()
        self.Continue_Button.clicked.connect(self.Continue)
        self.Back_Button.clicked.connect(self.Back)
        self.Forward_Button.clicked.connect(self.Forward)
        self.addGIF()
        
    def Show(self):
        self.show()
        
    def addImage(self):
        image_pxmap = QPixmap('Steps_Iriun.png')
        self.Background_Label.setPixmap(image_pxmap)
   
    def addGIF(self):
            gif_movie = QMovie('Wifi.gif')
            gif_label = self.Label_Gif
            gif_label.setMovie(gif_movie)
            gif_movie.start()
     
    def start_writing_Explain(self, texts_to_write):
        self.Explain_Browser.clear()
        current_text_index = 0
        current_letter_index = 0

        def write_letter():
            nonlocal current_text_index, current_letter_index

            # Check if all letters in the current text have been written
            if current_letter_index < len(texts_to_write[current_text_index]):
                # Append the next letter to the text browser
                self.Explain_Browser.insertPlainText(texts_to_write[current_text_index][current_letter_index])

                # Move to the next letter
                current_letter_index += 1
            else:
                # Move to the next line
                self.Explain_Browser.append("")

                # Move to the next text
                current_text_index += 1
                current_letter_index = 0

                # Check if all texts have been written
                if current_text_index == len(texts_to_write):
                    # Stop the timer when all texts are written
                    timer.stop()

        # Set up the interval between letters (in milliseconds)
        interval = 50
        timer = QTimer()
        timer.timeout.connect(write_letter)
        timer.start(interval)

        # Store the timer in the instance to prevent it from being garbage-collected
        self.timer = timer
    
    def showEvent(self, event):
        # Override the showEvent method to start writing when the window is shown
        super().showEvent(event)
        # Clear the text browser before starting to write
        self.Explain_Browser.clear()
        self.Message_Label.setText("")
        self.Forward_Button.setVisible(False)
        
        # Set the text to be written
        texts_Explain = [
                            '1) Install iriun app on your PC from this link : https://iriun.com/',
                            '',
                            '2) Install iriun app on your phone and run it.','',
                            '3) Follow the installation instructions.','',
                            '4) Open the iriun app.','',
                            '5) Ensure that your PC and the outher device are connected to the same Wifi.','',
                            '6) If everything is done  click on Continue.'
           
        ]
        self.start_writing_Explain(texts_Explain)
          
    def Continue(self):
        Index = 1
        Camera = cv2.VideoCapture(Index)
        _,Image_Test = Camera.read()
        
        if Is_Blank(Image_Test) == False:
            self.Forward_Button.setVisible(True)
          
            # Set the text color to red
            green_color = QColor(0,255, 0)  # RGB values for red
            self.Message_Label.setStyleSheet(f"color: {green_color.name()}")

            self.Message_Label.setText("Externel device was selected succesfully !")
            #self.Change_Signal.emit()
            global Camera_Index
            Camera_Index = Index
        else:
            self.Forward_Button.setVisible(False)
            red_color = QColor(255, 0, 0)  # RGB values for red
            self.Message_Label.setStyleSheet(f"color: {red_color.name()}")
            
            self.Message_Label.setText("Externel device is not available!")
            
        Camera.release()
     
    
    def Back(self):
        # Emit the finished signal 
        self.Back_signal.emit()
        self.close() 
        
    def Forward(self):
        # Emit the finished signal 
        self.Forward_Signal.emit()
        self.close() 
        
#######################################################################################
#######################################################################################
class Welcome_Window(QDialog):
    def __init__(self):
        super(Welcome_Window, self).__init__()
        loadUi('Welcome_Window.ui', self)
        self.addImage()
        self.Home_Button.clicked.connect(self.Home)
        self.AboutUs_Button.clicked.connect(self.AboutUs)
        self.Tutorial_Button.clicked.connect(self.Tutorial)
        
        self.GC_Button.clicked.connect(self.GC)
        self.text_writer = None  # Initialize text_writer attribute

        self.Message_Icon_Label_1.hide()
    
    def addImage(self):
        # Function to load and display the image
        image_pxmap = QPixmap('Welcome_Image.png')
        self.Background_Label.setPixmap(image_pxmap)
        image_pxmap = QPixmap('Message_Icon.png')
        self.Message_Icon_Label_1.setPixmap(image_pxmap)
        
        
    def GC(self):
        self.Message_Icon_Label_1.show()
        Show = Present(Camera_Index)
        Value = Show.SDPE()
        if Value :
            self.Message_Icon_Label_1.hide()
    
    def Home(self):
        self.showFullScreen()
        widget.setCurrentIndex(0)  
    
    def AboutUs(self):
       widget.setCurrentIndex(2)
    
    def Tutorial(self):
        widget.setCurrentIndex(1)
              
    def start_writing(self, texts_to_write):
        current_text_index = 0
        current_letter_index = 0

        def write_letter():
            nonlocal current_text_index, current_letter_index

            # Check if all letters in the current text have been written
            if current_letter_index < len(texts_to_write[current_text_index]):
                # Append the next letter to the text browser
                self.Explain_Browser.insertPlainText(texts_to_write[current_text_index][current_letter_index])

                # Move to the next letter
                current_letter_index += 1
            else:
                # Move to the next line
                self.Explain_Browser.append("")

                # Move to the next text
                current_text_index += 1
                current_letter_index = 0

                # Check if all texts have been written
                if current_text_index == len(texts_to_write):
                    # Stop the timer when all texts are written
                    timer.stop()

        # Set up the interval between letters (in milliseconds)
        interval = 50
        timer = QTimer()
        timer.timeout.connect(write_letter)
        timer.start(interval)

        # Store the timer in the instance to prevent it from being garbage-collected
        self.timer = timer

    def showEvent(self, event):
        # Override the showEvent method to start writing when the window is shown
        super().showEvent(event)
        # Clear the text browser before starting to write
        self.Explain_Browser.clear()
        # Set the text to be written
        texts_to_write = [
           "1.Please check the tutorial section before using the app.",
            "2.Open your PowerPoint, VideoReader, Documents viewer...",
            "3.Click on the button below.",
            "Enjoy..."
           
        ]
        self.start_writing(texts_to_write)

#######################################################################################       
####################################################################################### 

class Tutoriel_Window(QDialog):
    def __init__(self):
        super(Tutoriel_Window, self).__init__()
        loadUi('Tutoriel_Window.ui', self)
    
        
        self.addImage()
        
        
        self.Home_Button.clicked.connect(self.Home)
        self.AboutUs_Button.clicked.connect(self.AboutUs)
        self.Tutorial_Button.clicked.connect(self.Tutorial)
        
        self.lbl_link = QLabel('<a href="https://drive.google.com/file/d/1wDQoICmT-XNY5lbf-gpGcVhw9rq6uL0B/view?usp=drive_link">Click here for the tutorial video</a>', self)
        self.lbl_link.setOpenExternalLinks(True)
        self.lbl_link.setGeometry(480, 680,500, 30)
        self.lbl_link.linkActivated.connect(self.open_link)
        
        # Adjust font
        font = QFont()
        font.setBold(True)
        font.setPointSize(9)  # Increase font size
        self.lbl_link.setFont(font)

    def open_link(self, url):
        QDesktopServices.openUrl(QUrl(url))
        
      
    def addImage(self):
        # Function to load and display the image
        image_pxmap = QPixmap('Tutoriel_Window.png')
        self.Background_Label.setPixmap(image_pxmap)
        
    def Home(self):
        self.showFullScreen()
        widget.setCurrentIndex(0)  
    
    def AboutUs(self):
        widget.setCurrentIndex(2)
    
    def Tutorial(self):
       widget.setCurrentIndex(1)

#######################################################################################       
#######################################################################################     
class AboutUS_Window(QDialog):
    def __init__(self):
        super(AboutUS_Window, self).__init__()
        loadUi('Tutoriel_Window.ui', self)
    
        
        self.addImage()
        
        
        self.Home_Button.clicked.connect(self.Home)
        self.AboutUs_Button.clicked.connect(self.AboutUs)
        self.Tutorial_Button.clicked.connect(self.Tutorial)
        
      
    def addImage(self):
        # Function to load and display the image
        image_pxmap = QPixmap('AboutUS_Window.png')
        self.Background_Label.setPixmap(image_pxmap)
        
    def Home(self):
        self.showFullScreen()
        widget.setCurrentIndex(0)  
    
    def AboutUs(self):
        widget.setCurrentIndex(2)
    
    def Tutorial(self):
        widget.setCurrentIndex(1)
            
#######################################################################################
#######################################################################################      
def Show_main_interface():
    widget.setFixedWidth(1600)
    widget.setFixedHeight(800)
    widget.show()

def Show_Select_Device():
    Device_Select.PC_Box.setChecked(False)
    Device_Select.Externel_Box.setChecked(False)
    Device_Select.Show()

def Show_Steps_Iriun():
    Steps.show()
    
def Show_About_US():
    AboutUS_window.show()
     
if __name__ == "__main__":
    
    Camera_Index = 0
    
    app = QApplication(sys.argv)

    splash = SplashScreen()
    splash.Show()
    splash.progress()
    splash.finished.connect(lambda: Show_Select_Device())
    
    # Handle signals and slots :
    
    Device_Select = Device_Selection()
    Steps = Steps_Iriun()
    Device_Select.PC_Camera_Signal.connect(lambda: Show_main_interface())
    Device_Select.Externel_Camera_Signal.connect(lambda: Show_Steps_Iriun())
    Steps.Forward_Signal.connect(lambda: Show_main_interface())
    Steps.Back_signal.connect(lambda: Show_Select_Device())

    widget          = QStackedWidget()
    Welcome_window  = Welcome_Window()

    Tutoriel_window = Tutoriel_Window()
    AboutUS_window  = AboutUS_Window()
    
    widget.addWidget(Welcome_window)
    widget.addWidget(Tutoriel_window)
    widget.addWidget(AboutUS_window)


    sys.exit(app.exec_())

