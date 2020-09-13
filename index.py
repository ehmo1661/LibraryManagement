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

        self.show_category()
        self.show_author()
        self.show_publisher()

        self.show_category_combobox()
        self.show_author_combobox()
        self.show_publisher_combobox()



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

        self.addbook_save.clicked.connect(self.add_new_book)

        self.add_category_Button.clicked.connect(self.add_category)
        self.add_author_Button.clicked.connect(self.add_author)
        self.add_publisher_Button.clicked.connect(self.add_publisher)

        self.search_button.clicked.connect(self.search_book)


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
        self.db = pymysql.connect(host='localhost', user='root', password='89412317', db='library')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_2.text()
        book_description = self.textEdit.toPlainText()
        book_code = self.lineEdit_3.text()
        book_category = self.category_comboBox.currentIndex()
        book_author = self.author_comboBox.currentIndex()
        book_publisher = self.publisher_comboBox.currentIndex()
        book_price = self.lineEdit_4.text()

        self.cur.execute('''
            INSERT INTO library.book (`book_name`, `book_description`, `book_code`, `book_category`, `book_author`,
             `book_publisher`, `book_price`)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (book_title, book_description, book_code, book_category, book_author, book_publisher, book_price))
        self.db.commit()
        self.statusBar().showMessage('New book added')

        self.lineEdit_2.setText('')
        self.textEdit.setText('')
        self.lineEdit_3.setText('')
        self.lineEdit_4.setText('')
        self.category_comboBox.setCurrentIndex(0)
        self.author_comboBox.setCurrentIndex(0)
        self.publisher_comboBox.setCurrentIndex(0)

    def search_book(self):
        book_title = self.booktitle_search.text()

        self.cur.execute('''select * from library.book where book_name = %s''', book_title)
        data = self.cur.fetchone()  # if I use fetchall method, the setText method on book title face a crash because in
                                    # this way, fetchall results in a tuple like ((data......),) this mean that our result
                                    # is first element of a tuple. but, what if the query returs more that one output?
        self.lineEdit_5.setText(data[1])
        self.textEdit_2.setText(data[2])
        self.lineEdit_15.setText(data[3])
        self.comboBox_17.setCurrentIndex(data[4])
        self.comboBox_15.setCurrentIndex(data[5])
        self.comboBox_16.setCurrentIndex(data[6])
        self.lineEdit_14.setText(str(data[7]))


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
        self.db = pymysql.connect(host='localhost', user='root', password='89412317', db='library')
        self.cur = self.db.cursor()

        category_name_field = self.lineEdit_new_cat.text()

        self.cur.execute('''
            INSERT INTO library.category (`category_name`) VALUES (%s)
        ''', category_name_field)

        self.db.commit()
        self.statusBar().showMessage('New category added')
        self.lineEdit_new_cat.setText('')
        self.show_category()
        self.show_category_combobox()

    def show_category(self):
        self.db = pymysql.connect(host='localhost', user='root', password='89412317', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''select category_name from library.category''')
        data = self.cur.fetchall()

        if data:   # I think this part of code can be written better by making a list from data and iterate
            self.category_table.setRowCount(0)
            self.category_table.insertRow(0)
            for row, form in enumerate(data):
                #print('first loop', row, form)
                for column, item in enumerate(form):
                    #print('second loop', row, column, item)
                    self.category_table.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_position = self.category_table.rowCount()
                self.category_table.insertRow(row_position)

    def add_author(self):
        self.db = pymysql.connect(host='localhost', user='root', password='89412317', db='library')
        self.cur = self.db.cursor()

        author_name_field = self.lineEdit_new_author.text()

        self.cur.execute('''
            INSERT INTO library.authors (`author_name`) VALUES (%s)
        ''', author_name_field)

        self.db.commit()
        self.statusBar().showMessage('New author added')
        self.lineEdit_new_author.setText('')
        self.show_author()
        self.show_author_combobox()

    def show_author(self):
        self.db = pymysql.connect(host='localhost', user='root', password='89412317', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''select author_name from library.authors''')
        data = self.cur.fetchall()

        if data:  # I think this part of code can be written better by making a list from data and iterate
            self.author_table.setRowCount(0)
            self.author_table.insertRow(0)
            for row, form in enumerate(data):
                # print('first loop', row, form)
                for column, item in enumerate(form):
                    # print('second loop', row, column, item)
                    self.author_table.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_position = self.author_table.rowCount()
                self.author_table.insertRow(row_position)

    def add_publisher(self):
        self.db = pymysql.connect(host='localhost', user='root', password='89412317', db='library')
        self.cur = self.db.cursor()

        publisher_name_field = self.lineEdit_new_publisher.text()

        self.cur.execute('''
            INSERT INTO library.publisher (`publisher_name`) VALUES (%s)
        ''', publisher_name_field)

        self.db.commit()
        self.statusBar().showMessage('New publisher added')
        self.lineEdit_new_publisher.setText('')
        self.show_publisher()
        self.show_publisher_combobox()

    def show_publisher(self):
        self.db = pymysql.connect(host='localhost', user='root', password='89412317', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''select publisher_name from library.publisher''')
        data = self.cur.fetchall()

        if data:  # I think this part of code can be written better by making a list from data and iterate
            self.publisher_table.setRowCount(0)
            self.publisher_table.insertRow(0)
            for row, form in enumerate(data):
                # print('first loop', row, form)
                for column, item in enumerate(form):
                    # print('second loop', row, column, item)
                    self.publisher_table.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_position = self.publisher_table.rowCount()
                self.publisher_table.insertRow(row_position)

    ########################################################################
    ################### show settings data in UI ###########################
    def show_category_combobox(self):
        self.db = pymysql.connect(host='localhost', user='root', password='89412317', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''select category_name from library.category''')
        data = self.cur.fetchall()

        self.category_comboBox.clear()
        for category in data:
            self.category_comboBox.addItem(category[0])
            self.comboBox_17.addItem(category[0])

    def show_author_combobox(self):
        self.db = pymysql.connect(host='localhost', user='root', password='89412317', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''select author_name from library.authors''')
        data = self.cur.fetchall()

        self.author_comboBox.clear()
        for author in data:
            self.author_comboBox.addItem(author[0])
            self.comboBox_15.addItem(author[0])

    def show_publisher_combobox(self):
        self.db = pymysql.connect(host='localhost', user='root', password='89412317', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''select publisher_name from library.publisher''')
        data = self.cur.fetchall()

        self.publisher_comboBox.clear()
        for publisher in data:
            self.publisher_comboBox.addItem(publisher[0])
            self.comboBox_16.addItem(publisher[0])


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
