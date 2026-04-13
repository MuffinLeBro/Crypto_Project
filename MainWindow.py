import PyQt6
import os
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QPushButton, QMainWindow, QTextEdit, QLabel, QCheckBox, QPlainTextEdit, QTextBrowser
class MainWindow (QMainWindow):
    def __init__(self):
        super().__init__()

        ui_path = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(ui_path, "CryptoInterface.ui"), self)
        #Init Button
        self.btnRSA = self.findChild(QPushButton, 'btnRSA')
        self.btnDifHel = self.findChild(QPushButton, 'btnDiffieHellman')
        self.btnVigenere = self.findChild(QPushButton, 'btnVigenere')
        self.btnShift = self.findChild(QPushButton, 'btnShift')
        self.btnHashing = self.findChild(QPushButton, 'btnHashing')
        self.btnDecode = self.findChild(QPushButton, 'btnDecode')
        self.btnKeyFind = self.findChild(QPushButton, 'btnKeyFind')
        self.btnEncode = self.findChild(QPushButton, 'btnEncode')
        #Init TextBox
        self.txtMessage = self.findChild(QPlainTextEdit, 'txtMessage')
        self.txtKey = self.findChild(QPlainTextEdit, 'txtKey')
        self.txtSolution = self.findChild(QPlainTextEdit, 'txtSolution')
        self.txtServerBox = self.findChild(QTextBrowser, 'txtServerBox')
        

        #Inite Check Box
        self.cbServerOnly = self.findChild(QCheckBox, 'cbServerOnly')

        #Init Label
        self.lblKeyDisplay = self.findChild(QLabel, 'lblKeyDisplay')





    