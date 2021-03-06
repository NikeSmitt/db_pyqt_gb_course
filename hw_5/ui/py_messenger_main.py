# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ui_messenger_main.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Messenger(object):
    def setupUi(self, Messenger):
        Messenger.setObjectName("Messenger")
        Messenger.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(Messenger)
        self.centralwidget.setObjectName("centralwidget")
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(10, 40, 311, 431))
        self.listView.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        self.listView.setObjectName("listView")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 141, 16))
        self.label.setObjectName("label")
        self.addContactButton = QtWidgets.QPushButton(self.centralwidget)
        self.addContactButton.setGeometry(QtCore.QRect(10, 490, 151, 41))
        self.addContactButton.setObjectName("addContactButton")
        self.delContactButton = QtWidgets.QPushButton(self.centralwidget)
        self.delContactButton.setGeometry(QtCore.QRect(170, 490, 151, 41))
        self.delContactButton.setObjectName("delContactButton")
        self.allMessagesTextEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.allMessagesTextEdit.setGeometry(QtCore.QRect(350, 40, 441, 301))
        self.allMessagesTextEdit.setReadOnly(True)
        self.allMessagesTextEdit.setProperty("markdown", "")
        self.allMessagesTextEdit.setObjectName("allMessagesTextEdit")
        self.messageTextEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.messageTextEdit.setGeometry(QtCore.QRect(350, 370, 441, 91))
        self.messageTextEdit.setObjectName("messageTextEdit")
        self.sendMessageButton = QtWidgets.QPushButton(self.centralwidget)
        self.sendMessageButton.setGeometry(QtCore.QRect(630, 490, 151, 41))
        self.sendMessageButton.setObjectName("sendMessageButton")
        self.clearMessageButton = QtWidgets.QPushButton(self.centralwidget)
        self.clearMessageButton.setGeometry(QtCore.QRect(470, 490, 151, 41))
        self.clearMessageButton.setObjectName("clearMessageButton")
        Messenger.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Messenger)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        Messenger.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Messenger)
        self.statusbar.setObjectName("statusbar")
        Messenger.setStatusBar(self.statusbar)
        self.action_Quit = QtWidgets.QAction(Messenger)
        self.action_Quit.setObjectName("action_Quit")
        self.menu_File.addAction(self.action_Quit)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(Messenger)
        self.listView.doubleClicked['QModelIndex'].connect(Messenger.update)
        self.sendMessageButton.clicked.connect(Messenger.update)
        QtCore.QMetaObject.connectSlotsByName(Messenger)

    def retranslateUi(self, Messenger):
        _translate = QtCore.QCoreApplication.translate
        Messenger.setWindowTitle(_translate("Messenger", "MainWindow"))
        self.label.setText(_translate("Messenger", "???????????? ??????????????????"))
        self.addContactButton.setText(_translate("Messenger", "???????????????? ??????????????"))
        self.delContactButton.setText(_translate("Messenger", "?????????????? ??????????????"))
        self.allMessagesTextEdit.setHtml(_translate("Messenger", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.AppleSystemUIFont\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.allMessagesTextEdit.setPlaceholderText(_translate("Messenger", "??????????????????..."))
        self.sendMessageButton.setText(_translate("Messenger", "??????????????????"))
        self.clearMessageButton.setText(_translate("Messenger", "????????????????"))
        self.menu_File.setTitle(_translate("Messenger", "&File"))
        self.menu.setTitle(_translate("Messenger", "????????????"))
        self.action_Quit.setText(_translate("Messenger", "&Quit"))
