from PyQt5.Qtwidgets import QAplication , QMainWindow , QWidget, QTextEdit, QStackWidget, QLineEdit, QPushButton, QGridLayout, QHBoxLayout, QVBoxLayout , QFrame, QLabel, QSizePolicy
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
    Path = rf"{GraphicsDirPath}/{Filename}"     
    return Path

def TempDirectoryPath(Filename):
    Path = rf"{TempDirPath}/{Filename}"     
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
        self.gix_label.setStyleSheet("border: none;")
        movie = QMovie(rf"{GraphicsDirPath}/jarvis.gif")
        max_gif_size_W = 480
        max_gif_size_H = 270 
                
    