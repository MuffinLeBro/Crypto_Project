import os
import math
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMainWindow, QPushButton, QPlainTextEdit, QTextBrowser, QCheckBox, QLabel
from CLI import CLI
from Command import Command
from MessageHandler import MessageHandler
from Client import Client
class MainWindow (QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(ui_path, "GUI/CryptoInterface.ui"), self)

        #init Serveur
        self.crypto = Command()
        self.handler = MessageHandler()
        self.client = Client()
        self.client.connect("vlbelintrocrypto.hevs.ch", 6000)
        self.cli = CLI()

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
        #Init TextBox
        self.txtMessage = self.findChild(QPlainTextEdit, 'txtMessage')
        self.txtKey = self.findChild(QPlainTextEdit, 'txtKey')
        self.txtPrivateKey = self.findChild(QPlainTextEdit, 'txtPrivateKey')
        self.txtPublicKey = self.findChild(QPlainTextEdit, 'txtPublicKey')
        self.txtSolution = self.findChild(QPlainTextEdit, 'txtSolution')
        self.txtServerBox = self.findChild(QTextBrowser, 'txtServerBox')
    
        #Inite Check Box
        self.cbServerOnly = self.findChild(QCheckBox, 'cbServerOnly')

        #Init Label
        self.lblKeyDisplay = self.findChild(QLabel, 'lblKeyDisplay')

        #Init ButtonEvent
        self.btnShift.clicked.connect(self.btnShift_Clicked)
        self.btnVigenere.clicked.connect(self.btnVigenere_Clicked)
        self.btnRSA.clicked.connect(self.btnRsa_Clicked)
        self.btnDifHel.clicked.connect(self.btnDifHel_Clicked)
        self.btnSendServer.clicked.connect(self.btnSendServer_Clicked)

  
    def btnShift_Clicked(self):
        # Récupère le message et la clé
        msg = self.txtMessage.toPlainText()
        key = self.txtKey.toPlainText()
        if key.isdigit() :
            # Envoie du message au serveur
            self.client.send(msg)
            res = self.crypto.encode_shift(msg, int(key))
            self.txtSolution.setPlainText(res)
        else :
            self.txtSolution.setPlainText("La clé doit être un nombre")

    def btnVigenere_Clicked(self):
        msg = self.txtMessage.toPlainText()
        key = self.txtKey.toPlainText()
        self.client.send(msg)
        res = self.crypto.encode_vigenere(msg, key)
        self.txtSolution.setPlainText(res)
    def btnRsa_Clicked(self):
        msg = self.txtMessage.toPlainText()
        publicKey = self.txtPublicKey.toPlainText()
        privateKey = self.txtPrivateKey.toPlainText()
        if publicKey.isdigit and privateKey.isdigit:
            self.client.send(msg)
            res = self.crypto.encode_rsa(msg, publicKey, privateKey)
            self.txtSolution.toPlainText(res)
        else:
            self.txtSolution.toPlainText("La clé privée ou la clé publique doit être un entier")
        
    def btnDifHel_Clicked(self): 
        ...
    def btnSendServer_Clicked(self) :
        # Récupère la le message 
        message = self.txtMessage.toPlainText()
        
        # Verifier que le message n'est pas vide
        if message == "":
            print("Le message ne doit pas être vide")
            return
        
        # Découper le message en mots
        words = message.split()

        # Verfier que la commande est une tache valide
        if words[0] != "task" :
            print("Le 1er élement doit contenir le mot task")
            return

        # Verifier que la commande est bien formé 
        if len(words) != 4 :
            print("La commande doit contenir 4 élements")
            return
        
        if words[1] != "shift" and words[1] != "vigenere" and words[1] != "rsa" and words[1] != "diffiehellman" and words[1] != "hashing" :
            print("Le 2ème élement doit être shift, vigenere, rsa, diffiehellman ou hashing")
            return
        if not words[3].isdigit() :
            print("Le 4ème élement doit être un nombre")
            return
        
        # Récupérer le type de message à envoyer au serveur depuis la checkbox
        if self.cbServerOnly.isChecked:
            msg_type = 's'
        else: 
            msg_type = 't' 
        
        content = " ".join(words[1:])
        
            
        
        # Envoie du message au serveur
        self.client.send(self.handler.build_message(msg_type, content))
        
        # Recupérer la réponse du serveur
        
        # Décoder la réponse du serveur
        
        # Afficher la réponse du serveur 
    def isPrime(n):
        if n < 2 :
            return False
        for i in range(2, math.sqrt(n) + 1):
            if n % i == 0:
                return False
        return True    