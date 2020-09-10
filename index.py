import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import pymysql
#pymysql.install_as_MySQLdb()

ui, _ = loadUiType('MainPage.ui')


class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_UI_Changes()
        self.Handle_Buttons()

    def Handle_UI_Changes(self):
        self.hiding_themes()
        self.tabWidget.tabBar().setVisible(False)
        self.tabWidget.setCurrentIndex(0)       # start the program at the first page

    def Handle_Buttons(self):
        self.themebutton.clicked.connect(self.show_themes)
        self.theme_close.clicked.connect(self.hiding_themes)

        self.day_tabs_button.clicked.connect(self.open_day_tab)
        self.books_tab_button.clicked.connect(self.open_books_tab)
        self.users_tab_button.clicked.connect(self.open_users_tab)
        self.settings_tab_button.clicked.connect(self.open_settings_tab)


    def show_themes(self):
        self.themes_window.show()

    def hiding_themes(self):
        self.themes_window.hide()

    ########################################################################
    ########################### openning tabs ##############################

    def open_day_tab(self):
        self.tabWidget.setCurrentIndex(0)

    def open_books_tab(self):
        self.tabWidget.setCurrentIndex(1)

    def open_users_tab(self):
        self.tabWidget.setCurrentIndex(2)

    def open_settings_tab(self):
        self.tabWidget.setCurrentIndex(3)

    ########################################################################
    ########################### Books tabs #################################
    def add_new_book(self):
        pass

    def search_book(self):
        pass

    def edit_book(self):
        pass

    def delete_book(self):
        pass

    ########################################################################
    ########################### users tabs #################################
    def add_new_user(self):
        pass

    def login(self):
        pass

    def edit_user(self):
        pass

    ########################################################################
    ########################### settings tabs ##############################
    def add_category(self):
        pass

    def add_author(self):
        pass

    def add_publisher(self):
        pass
    

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
