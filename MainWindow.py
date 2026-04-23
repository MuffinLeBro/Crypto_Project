import os
import math
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMainWindow, QPushButton, QPlainTextEdit, QTextBrowser, QCheckBox, QLabel
from CLI import CLI
from Command import Command
from MessageHandler import MessageHandler
from Client import Client
from DiffieHellman import DiffieHellman
class MainWindow (QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(ui_path, "GUI/CryptoInterface.ui"), self)

        #init Serveur
        self.crypto = Command()
        self.handler = MessageHandler()
        self.client = Client()
        self.dh = DiffieHellman()
        self.client.connect("vlbelintrocrypto.hevs.ch", 6000)
        self.client.start_receiving(self.on_message_received)

        #Init Button
        self.btnRSA = self.findChild(QPushButton, 'btnRSA')
        self.btnDifHel = self.findChild(QPushButton, 'btnDiffieHellman')
        self.btnVigenere = self.findChild(QPushButton, 'btnVigenere')
        self.btnShift = self.findChild(QPushButton, 'btnShift')
        self.btnHashing = self.findChild(QPushButton, 'btnHashing')
        self.btnDecode = self.findChild(QPushButton, 'btnDecode')
        self.btnKeyFind = self.findChild(QPushButton, 'btnKeyFind')
        self.btnEncode = self.findChild(QPushButton, 'btnEncode')
        self.btnSendServer = self.findChild(QPushButton, 'btnSendServer')
        self.btnClea = self.findChild(QPushButton, 'btnClear')

        #Init TextBox
        self.txtMessage = self.findChild(QPlainTextEdit, 'txtMessage')
        self.txtKey = self.findChild(QPlainTextEdit, 'txtKey')
        self.txtPrivateKey = self.findChild(QPlainTextEdit, 'txtPrivateKey')
        self.txtPublicKey = self.findChild(QPlainTextEdit, 'txtPublicKey')
        self.txtSolution = self.findChild(QPlainTextEdit, 'txtSolution')
        self.txtServerBox = self.findChild(QPlainTextEdit, 'txtServerBox')
        self.txtModulo = self.findChild(QPlainTextEdit, 'txtModulo')
        self.txtLog = self.findChild(QTextBrowser, 'txtLog')
    
        #Inite Check Box
        self.cbServerOnly = self.findChild(QCheckBox, 'cbServerOnly')

        #Init Label
        self.lblKeyDisplay = self.findChild(QLabel, 'lblKeyDisplay')

        #Init ButtonEvent
        self.btnShift.clicked.connect(self.btnShift_Clicked)
        self.btnVigenere.clicked.connect(self.btnVigenere_Clicked)
        self.btnRSA.clicked.connect(self.btnRsa_Clicked)
        self.btnDifHel.clicked.connect(self.btnDifHel_Clicked)
        self.btnHashing.clicked.connect(self.btnHashing_Clicked)
        self.btnSendServer.clicked.connect(self.btnSendServer_Clicked)
        self.btnClear.clicked.connect(self.btnClear_Clicked)

    def on_message_received(self, message):
        self.txtServerBox.appendPlainText(message.decode("utf-32-be") + "\n\n")
  
    def btnShift_Clicked(self):
        msg = self.txtMessage.toPlainText()
        key = self.txtKey.toPlainText()
        if key.isdigit():
            res = self.crypto.encode_shift(msg, int(key))
            self.txtSolution.setPlainText(res)
            self.client.send(self.handler.build_message('s', res))
        else :
            self.txtSolution.setPlainText("La clé doit être un nombre")

    def btnVigenere_Clicked(self):
        msg = self.txtMessage.toPlainText()
        key = self.txtKey.toPlainText()
        res = self.crypto.encode_vigenere(msg, key)
        self.txtSolution.setPlainText(res)
        self.client.send(self.handler.build_message('s', res))
        
    def btnRsa_Clicked(self):
        msg = self.txtMessage.toPlainText()
        publicKey = self.txtPublicKey.toPlainText()
        modulo = self.txtModulo.toPlainText()
        if publicKey.isdigit and modulo.isdigit:
            numList = self.crypto.encode_rsa(msg, int(publicKey), int(modulo))
            self.txtSolution.setPlainText(str(numList))
            self.client.send(b"ISC" + b"s" + int.to_bytes((len(numList) // 4), length=2) + numList)
        else:
            self.txtLog.toPlainText("La clé privée ou la clé publique doit être un entier")
        
    def btnDifHel_Clicked(self): 
        p, g = self.dh.generate(max_mod=1000)
        A, self.priv_a = self.dh.halfkey(p, g)
        result_text = f"p: {p}, g: {g}, Public A: {A}"
        self.txtSolution.setPlainText(result_text)
        payload = f"{p},{g},{A}"
        res = self.handler.build_message('d', payload)
        self.client.send(res)

    def btnHashing_Clicked(self):
        msg = self.txtMessage.toPlainText()
        if msg == "":
            self.txtSolution.setPlainText("Veuillez entrez un message")
        else:
            res = self.crypto.sha256(msg)
            self.txtSolution.setPlainText(res)
            self.client.send(self.handler.build_message('s',res))

    def btnSendServer_Clicked(self) :
        message = self.txtMessage.toPlainText()
        
        if message == "":
            self.txtLog.setPlainText("Le message ne doit pas être vide")
            return  
        words = message.split()

        if self.cbServerOnly.isChecked:
            msg_type = 's'
        else: 
            msg_type = 't'         

        self.client.send(self.handler.build_message(msg_type, message))

    def btnClear_Clicked(self):
        self.txtServerBox.clear()