from PyQt5.QtWidgets import QApplication , QMainWindow , QWidget, QTextEdit, QStackedWidget, QLineEdit, QPushButton, QGridLayout, QHBoxLayout, QVBoxLayout , QFrame, QLabel, QSizePolicy
from PyQt5.QtGui import QIcon, QPainter , QMovie, QColor , QTextCharFormat , QFont, QPixmap , QTextBlockFormat
from PyQt5.QtCore import Qt , QSize , QTimer
from dotenv import dotenv_values # import dotenv to load environment variables from a .env file
import os
import sys

env_vars = dotenv_values(".env")
Assistantname = env_vars.get("Assistantname")
current_dir = os.getcwd()
old_chat_message = ""
TempDirPath = rf"{current_dir}/Frontend/Files"
GraphicsDirPath = rf"{current_dir}/Frontend/Graphics"

def AnswerModifier(Answer):
    lines = Answer.split("\n") #split the answer into lines
    non_empty_lines = [line for line in lines if line.strip()] #remove empty lines
    modified_answer = "\n".join(non_empty_lines) #join the non-empty lines into a single string
    return modified_answer

def QueryModifier(Query):
    
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "when", "where", "who", "why", "which", "whom", "whose","can you","what's","where's", "how's","can you"]
    
    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in [".", "!", "?"]:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in [".", "!", "?"]: 
            new_query = new_query[:-1] + "."
        else:
            new_query += "."
    return new_query.capitalize()

def SetMicrophoneStatus(command):
    with open(rf'{TempDirPath}\Mic.data', 'w', encoding='utf-8') as file:
        file.write(command)
def GetMicrophoneStatus():
    with open(rf'{TempDirPath}\Mic.data', 'r', encoding='utf-8') as file:
        Status = file.read()
    return Status

def SetAssistantStatus(Status):
    with open(rf'{TempDirPath}\Status.data', 'w', encoding='utf-8') as file:
        file.write(Status)

def GetAssistantStatus():
    with open(rf'{TempDirPath}\Status.data', 'r', encoding='utf-8') as file:
        Status = file.read()
    return Status

def MicButtonInitialed():
    SetMicrophoneStatus("False")

def MicButtonClosed():
    SetMicrophoneStatus("True")
 
def GraphicsDirectoryPath(Filename):
    Path = rf"{GraphicsDirPath}\{Filename}"     
    return Path

def TempDirectoryPath(Filename):
    Path = rf"{TempDirPath}\{Filename}"     
    return Path

def ShowTextToScreen(Text):
    with open(rf'{TempDirPath}\Responses.data', 'w', encoding='utf-8') as file:
        file.write(Text)
        

class ChatSection(QWidget):
    def __init__(self):
        super(ChatSection, self).__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(-10,40,40,100)
        layout.setSpacing(-100)
        self.chat_text_edit = QTextEdit(self)
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        layout.addWidget(self.chat_text_edit)
        self.setStyleSheet("background-color: black;")
        layout.setSizeConstraint(QVBoxLayout.SetDefaultConstraint)
        layout.setStretch(1,1)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        text_color = QColor(Qt.blue)
        text_color_text = QTextCharFormat()
        text_color_text.setForeground(text_color)
        self.chat_text_edit.setCurrentCharFormat(text_color_text)
        self.gif_label = QLabel()
        self.gif_label.setStyleSheet("border: none;")
        movie = QMovie(rf"{GraphicsDirPath}\Jarvis.gif")
        max_gif_size_W = 480
        max_gif_size_H = 270
        movie.setScaledSize(QSize(max_gif_size_W, max_gif_size_H))
        self.gif_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.gif_label.setMovie(movie)
        movie.start()
        layout.addWidget(self.gif_label)
        self.label = QLabel("")
        self.label.setStyleSheet("color: white; font-size: 16px; margin-right: 195px; border: none; margin-top: -30px;") 
        self.label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.label)
        layout.setSpacing(-10)
        layout.setSpacing(-10)
        font = QFont()
        font.setPointSize(13)
        self.chat_text_edit.setFont(font)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)
        self.chat_text_edit.viewport().installEventFilter(self)
        self.setStyleSheet("""
            QScrollBar:vertical {
                border: none;
                background: black;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: white;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical {
                background: black;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
                height: 10px;
            }
            QScrollBar::sub-line:vertical {
                background: black;
                subcontrol-position: top;
                subcontrol-origin: margin;
                height: 10px;
            }
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                border: none;
                background: none;
                color: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        
        # Fixed QLabel style
        self.label.setStyleSheet("color: white; font-size: 16px; margin-right: 195px; border: none; margin-top: -30px;")
    def loadMessages(self):    
            global old_chat_message
            with open(TempDirectoryPath("Responses.data"), 'r', encoding='utf-8') as file:
               messages = file.read()
               if None == messages:
                   pass
               elif len(messages)<=1:
                   pass
               elif str(old_chat_message)== str(messages):
                   pass
               else:
                   self.addMessage(messages=messages , color = "white")
                   old_chat_message = messages
    def SpeechRecogText(self):
            with open(TempDirectoryPath("Status.data"), 'r', encoding='utf-8') as file:
                messages = file.read()
                self.label.setText(messages)
                
    def load_icon(self ,  path , width = 60 , height = 60):
         pixmap = QPixmap(path)
         new_pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
         self.icon_label.setPixmap(new_pixmap)
        
    def toggle_icon(self, event = None):
            if self.toggled:
                self.load_icon(GraphicsDirectoryPath('voice.png'),60,60)
                MicButtonInitialed()
            else:
                self.load_icon(GraphicsDirectoryPath('mic.png'),60,60)
                MicButtonClosed()
            
            self.toggled = not self.toggled
    def addMessage(self, messages, color):    
             cursor = self.chat_text_edit.textCursor()
             format = QTextCharFormat()
             formatm = QTextBlockFormat()
             formatm.setTopMargin(10)
             formatm.setLeftMargin(10)
             format.setForeground(QColor(color))
             cursor.setCharFormat(format)
             cursor.setBlockFormat(formatm)
             cursor.insertText(messages + "\n")
             self.chat_text_edit.setTextCursor(cursor)
             
class InitialScreen(QWidget):
    
    def __init__(self, parent = None):
        super().__init__(parent)
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        gif_label = QLabel()
        movie = QMovie(GraphicsDirectoryPath("Jarvis.gif"))
        gif_label.setMovie(movie)
        max_gif_size_H = int(screen_width / 16 * 9)
        movie.setScaledSize(QSize(screen_width, max_gif_size_H))
        gif_label.setAlignment(Qt.AlignCenter)
        movie.start()
        gif_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.icon_label = QLabel()  
        pixmap = QPixmap(GraphicsDirectoryPath('Mic_on.png'))
        new_pixmap = pixmap.scaled(60, 60)
        self.icon_label.setPixmap(new_pixmap)
        self.icon_label.setFixedSize(150 ,150)
        self.icon_label.setAlignment(Qt.AlignCenter) 
        self.toggled = True
        self.toggle_icon()
        self.icon_label.mousePressEvent = self.toggle_icon 
        self.label = QLabel("")
        self.label.setStyleSheet("color:white; font-size:16px;margin-bottom:0;")
        content_layout.addWidget(gif_label, alignment=Qt.AlignCenter)
        content_layout.addWidget(self.label, alignment=Qt.AlignCenter)
        content_layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
        content_layout.setContentsMargins(0, 0, 0, 150)
        self.setLayout(content_layout)
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)
        self.setStyleSheet("background-color: black;")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)
    
    def SpeechRecogText(self):
        with open(TempDirectoryPath("Status.data"), 'r', encoding='utf-8') as file:
            messages = file.read()
            self.label.setText(messages)
     
    def load_icon(self, path, width = 60 , height = 60):
        print(f"Attempting to load icon from: {path}")
        pixmap = QPixmap(path)
        if pixmap.isNull():
           print(f"Error: Could not load pixmap from {path}")
        new_pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.icon_label.setPixmap(new_pixmap)
        
    def toggle_icon(self, event = None):
        if self.toggled:
            self.load_icon(GraphicsDirectoryPath('Mic_on.png'),60,60)
            MicButtonInitialed()
        else:
            self.load_icon(GraphicsDirectoryPath('Mic_off.png'),60,60)
            MicButtonClosed()
        
        self.toggled = not self.toggled

class MessageScreen(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        layout = QVBoxLayout()
        label = QLabel("")
        layout.addWidget(label)
        chat_section = ChatSection()
        layout.addWidget(chat_section)
        self.setLayout(layout)
        self.setStyleSheet("background-color: black;")
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)    
    
class CustomTopBar(QWidget):
    def __init__(self, parent , stacked_widget):
     super().__init__(parent)
     self.draggable = True  # Initialize draggable attribute
     self.offset = None     # Initialize offset attribute
     self.current_screen = None
     self.stacked_widget = stacked_widget   
     self.initUI()

    def initUI(self):
     self.setFixedHeight(50)
     layout = QHBoxLayout()
     layout.setAlignment(Qt.AlignRight)
     
     # Set white background for the top bar
     self.setStyleSheet("background-color: white;")
     
     # Title label
     title_label = QLabel(f"{str(Assistantname).capitalize()} AI")
     title_label.setStyleSheet("color:black; font-size:18px; background-color:white;")
     layout.addWidget(title_label)
    
     layout.addStretch(1)
    
    # Home button with fixed icon loading
     home_button = QPushButton()
     home_icon = QIcon(GraphicsDirectoryPath('Home.png'))
     home_button.setIcon(home_icon)
     home_button.setIconSize(QSize(24, 24))  # Set icon size
     home_button.setText(" Home")
     home_button.setStyleSheet("""
         height:40px; 
         line-height:40px; 
         background-color:white; 
         color:black;
         padding: 5px;
     """)
    
    # Message button with fixed icon loading
     message_button = QPushButton()
     message_icon = QIcon(GraphicsDirectoryPath('Chats.png'))
     message_button.setIcon(message_icon)
     message_button.setIconSize(QSize(24, 24))  # Set icon size
     message_button.setText(" Chats")
     message_button.setStyleSheet("""
        height:40px; 
        line-height:40px; 
        background-color:white; 
        color:black;
        padding: 5px;
     """)
    
    # Window control buttons with fixed icon loading
     minimize_button = QPushButton()
     minimize_icon = QIcon(GraphicsDirectoryPath('Minimize2.png'))
     minimize_button.setIcon(minimize_icon)
     minimize_button.setIconSize(QSize(24, 24))  # Set icon size
     minimize_button.setStyleSheet("""
        background-color:white;
        padding: 5px;
    """)  
     minimize_button.clicked.connect(self.minimizeWindow)
    
     self.maximize_button = QPushButton()
     self.maximize_icon = QIcon(GraphicsDirectoryPath('Maximize.png'))
     self.restore_icon = QIcon(GraphicsDirectoryPath('Minimize.png'))
     self.maximize_button.setIcon(self.maximize_icon)
     self.maximize_button.setIconSize(QSize(24, 24))  # Set icon size
     self.maximize_button.setFlat(True)
     self.maximize_button.setStyleSheet("""
        background-color:white;
        padding: 5px;
    """)
     self.maximize_button.clicked.connect(self.maximizeWindow)
    
     close_button = QPushButton()
     close_icon = QIcon(GraphicsDirectoryPath('Close.png'))
     close_button.setIcon(close_icon)
     close_button.setIconSize(QSize(24, 24))  # Set icon size
     close_button.setStyleSheet("""
        background-color:white;
        padding: 5px;
    """)
     close_button.clicked.connect(self.closeWindow)
    
     line_frame = QFrame()
     line_frame.setFixedHeight(1)
     line_frame.setFrameShape(QFrame.HLine) 
     line_frame.setFrameShadow(QFrame.Sunken)
     line_frame.setStyleSheet("border-color: black;")
    
    # Connect signals
     home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
     message_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
    
    # Add widgets to layout
     layout.addWidget(title_label)
     layout.addStretch(1)
     layout.addWidget(home_button)
     layout.addWidget(message_button)
     layout.addStretch(1)
     layout.addWidget(minimize_button)
     layout.addWidget(self.maximize_button)
     layout.addWidget(close_button)
     layout.addWidget(line_frame)
    
     self.setLayout(layout)

    def paintEvent(self,event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.white)
        super().paintEvent(event)

    def minimizeWindow(self):
        self.parent().showMinimized()

    def maximizeWindow(self):
        if self.parent().isMaximized():
            self.parent().showNormal()
            self.maximize_button.setIcon(self.maximize_icon)
        else:
            self.parent().showMaximized()
            self.maximize_button.setIcon(self.restore_icon)

    def closeWindow(self):
        self.parent().close()

    def mousePressEvent(self, event):
        if self.draggable:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.draggable and self.offset:
            new_pos = event.globalPos() - self.offset
            self.parent().move(new_pos)

    def showMessageScreen(self):
        if self.current_screen is not None:
            self.current_screen.hide()

        message_screen = MessageScreen(self)
        layout = self.parent().layout()
        if layout is not None:
            layout.addWidget(message_screen)
        self.current_screen = message_screen

    def showInitialScreen(self):
        if self.current_screen is not None:
            self.current_screen.hide()

        initial_screen = InitialScreen(self)
        layout = self.parent().layout()
        if layout is not None:
            layout.addWidget(initial_screen)
        self.current_screen = initial_screen
        
       
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()
        
    def initUI(self):
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        stacked_widget = QStackedWidget(self)  
        initial_screen = InitialScreen()
        message_screen = MessageScreen()
        stacked_widget.addWidget(initial_screen)
        stacked_widget.addWidget(message_screen)
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setStyleSheet("background-color: black;")
        top_bar = CustomTopBar(self, stacked_widget)
        self.setMenuWidget(top_bar)
        self.setCentralWidget(stacked_widget)
        
def GraphicalUserInterface():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    GraphicalUserInterface()