from PyQt6.QtWidgets import QApplication, QMainWindow, QFormLayout, QLabel, QLineEdit, QWidget, QPushButton
from PyQt6 import QtCore, QtGui
from UIgen import Ui_MainWindow
from madlibui import Ui_MainWindow as UI_MainWindow
from nltk.tag import pos_tag
from nltk import download
from nltk.tokenize import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
import random

download('punkt')
download('averaged_perceptron_tagger')

def resource_path(relative_path): #use this for resource path for auto-py-to-exe
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def get_tokenized():
    global token_story
    f=open("stories.biz","r",encoding="utf-8")
    num=random.randint(1,50)
    str=""
    for i in range(num):
        str=f.readline()
    token_story=word_tokenize(str)
    lst= pos_tag(token_story)
    return lst


class StartWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(StartWindow, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(play_now)

class MadLibWindow(QMainWindow, UI_MainWindow):
    def __init__(self):
        super(MadLibWindow, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(restart)

class ChoiceWindow(QMainWindow):
    def __init__(self):
        super(ChoiceWindow, self).__init__()
        self.setWindowTitle("MadLibs")
        self.resize(800, 600)
        self.setMinimumSize(QtCore.QSize(100, 100))
        form= QFormLayout()

        self.labels=[]
        self.textFields=[]

        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(8)

        for i in range(15):
            self.labels.append(QLabel())
            self.textFields.append(QLineEdit())
            self.labels[i].setFont(font)
            form.addRow(self.labels[i],self.textFields[i])

        font.setPointSize(10)
        self.getStoryButton=QPushButton("Get MadLib")
        self.getStoryButton.clicked.connect(self.getMadLib)
        self.getStoryButton.setFont(font)
        form.addRow(self.getStoryButton)

        wid= QWidget()
        wid.setLayout(form)
        self.setCentralWidget(wid)

    def getMadLib(self):
        global str_tokens, detokenizer, story

        for i in range(15):
            token_story[str_choices[i][1]]=self.textFields[i].text()
        story= detokenizer.detokenize(token_story)
        showMadLib()

def showMadLib():
    global window
    window= MadLibWindow()
    window.label.setText(story)
    window.show()


def play_now():
    global window, str_tokens, str_choices, tag_name
    window= ChoiceWindow()

    str_tokens= get_tokenized()
    str_choices= get_choices(str_tokens)

    for i in range(15):
        window.labels[i].setText(tag_name[str_choices[i][0]])
    window.show()

def get_choices(str_tokens):
    global valid_tags
    lst=[]
    for i in range(len(str_tokens)):
        if str_tokens[i][1] in valid_tags:
            lst.append([str_tokens[i][1],i])
    lst=random.sample(lst,15)
    return lst

def restart():
    global window
    window= StartWindow()
    window.show()

if __name__ == "__main__":
    str_tokens=[]
    str_choices=[]
    token_story=[]
    story=""
    detokenizer = TreebankWordDetokenizer()
    valid_tags=['JJ','JJR','JJS','NN','NNS','NNP','NNPS','RB','VB','VBD','VBG']
    tag_name={'JJ':'Adjective',
              'JJR':'Comparative Adjevtive',
              'JJS':'Superlative Adjective',
              'NN':'Common Noun',
              'NNS':'Common Noun Plural',
              'NNP':'Proper Noun',
              'NNPS':'Proper Noun Plural',
              'RB':'Adverb','VB':'Verb Present Tense',
              'VBD':'Verb Past Tense',
              'VBG':'Verb Present Participle'}
    app = QApplication([])

    window = StartWindow()
    window.show()

    app.exec()