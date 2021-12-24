import sys

from PyQt5 import QtWidgets, QtCore, QtGui

import crud
from client import Client
from common.variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT
from ui.py_messenger_main import Ui_Messenger



class MessengerMain(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Messenger()
        self.ui.setupUi(self)
        self.client = Client(DEFAULT_IP_ADDRESS, DEFAULT_PORT, 'test1')
        self.update_contact_list()

    def update(self) -> None:
        print('Work')

    def update_contact_list(self):
        contact_names = crud.get_user_contacts(self.client.name)
        model = QtGui.QStandardItemModel()
        self.ui.listView.setModel(model)

        for name in contact_names:
            item = QtGui.QStandardItem(name)
            model.appendRow(item)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MessengerMain()
    window.show()
    sys.exit(app.exec())
