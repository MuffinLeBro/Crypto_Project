import os
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMainWindow, QPushButton, QPlainTextEdit, QTextBrowser, QCheckBox, QLabel

from Command import Command
from MessageHandler import MessageHandler
from Client import Client
class MainWindow (QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(ui_path, "CryptoInterface.ui"), self)

        #init Serveur
        self.crypto = Command()
        self.handler = MessageHandler()
        self.client = Client()
        self.client.connect("vlbelintrocrypto.hevs.ch", 6000)
        self.client.start_receiving(self.data_Received)

        #Init Button
        self.btnRSA = self.findChild(QPushButton, 'btnRSA')
        self.btnDifHel = self.findChild(QPushButton, 'btnDiffieHellman')
        self.btnVigenere = self.findChild(QPushButton, 'btnVigenere')
        self.btnShift = self.findChild(QPushButton, 'btnShift')
        self.btnHashing = self.findChild(QPushButton, 'btnHashing')
        self.btnDecode = self.findChild(QPushButton, 'btnDecode')
        self.btnKeyFind = self.findChild(QPushButton, 'btnKeyFind')
        self.btnEncode = self.findChild(QPushButton, 'btnEncode')
        self.btnHelp = self.findChild(QPushButton, 'btnHelp')
        #Init TextBox
        self.txtMessage = self.findChild(QPlainTextEdit, 'txtMessage')
        self.txtKey = self.findChild(QPlainTextEdit, 'txtKey')
        self.txtSolution = self.findChild(QPlainTextEdit, 'txtSolution')
        self.txtServerBox = self.findChild(QTextBrowser, 'txtServerBox')
    
        #Inite Check Box
        self.cbServerOnly = self.findChild(QCheckBox, 'cbServerOnly')

        #Init Label
        self.lblKeyDisplay = self.findChild(QLabel, 'lblKeyDisplay')

        #Init ButtonEvent
        self.btnShift.clicked.connect(self.shift_Clicked)
        self.btnVigenere.clicked.connect(self.vigenere_Clicked)
        self.btnRSA.clicked.connect(self.rsa_Clicked)
        self.btnDifHel.clicked.connect(self.difHel_Clicked)
        self.btnHelp.clicked.connect(self.help_CLicked)

  
    def shift_Clicked(self):
        msg = self.txtMessage.toPlainText()
        key = self.txtKey.toPlainText()
        if key.isdigit() :
            res = self.crypto.encode_shift(msg, int(key))
            self.txtSolution.setPlainText(res)
        else :
            self.txtSolution.setPlainText("La clé doit être un nombre")

    def vigenere_Clicked(self):
        ...

    def rsa_Clicked(self):
        ...

    def difHel_Clicked(self): 
        ...
    def help_CLicked(self):
        ...
    
    def data_Received(self, data):
        msgServer = self.handler.decode_message(data)
        self.txtServerBox.append(f"Serveur : {msgServer}")