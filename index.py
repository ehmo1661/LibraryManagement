import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import pymysql
import datetime
import jdatetime
#pymysql.install_as_MySQLdb()

ui, _ = loadUiType('MainPage.ui')
login, _ = loadUiType('login.ui')


class Login(QWidget, login):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.handle_login)
        style = open(r'Themes/ManjaroMix.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def handle_login(self):
        self.db = pymysql.connect(host='localhost', user='root', password='89412317', db='library')
        self.cur = self.db.cursor()

        username = self.user_edit.text()
        password = self.pass_edit.text()

        sql = '''select * from library.users'''
        self.cur.execute(sql)
        all_users = self.cur.fetchall()
        for user in all_users:
            if username == user[1] and password == user[3]:
                print('Valid user information')
                self.window2 = MainApp()
                self.close()
                self.window2.show()


        # else:
        #     msgbox = QMessageBox()
        #     msgbox.setIcon(QMessageBox.Warning)
        #     msgbox.setText('Please make sure passwords are the same')
        #     msgbox.setWindowTitle("Password error")
        #     msgbox.setStandardButtons(QMessageBox.Ok)
        #     msgbox.exec()
        #
        # self.user_edit.setText('')
        # self.email_edit.setText('')
        # self.pass_edit.setText('')
        # self.conf_edit.setText('')



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

        self.show_day_operation()
        self.show_all_books()

        self.manjaromix_theme()



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

        self.day_add_button.clicked.connect(self.handle_day_operations)

        self.addbook_save.clicked.connect(self.add_new_book)
        self.search_button.clicked.connect(self.search_book)
        self.save_button.clicked.connect(self.edit_book)
        self.delete_button.clicked.connect(self.delete_book)

        self.add_category_Button.clicked.connect(self.add_category)
        self.add_author_Button.clicked.connect(self.add_author)
        self.add_publisher_Button.clicked.connect(self.add_publisher)

        self.user_add_button.clicked.connect(self.add_new_user)
        self.user_login_button.clicked.connect(self.login)
        self.user_edit_button.clicked.connect(self.edit_user)

        self.ubuntu_theme_button.clicked.connect(self.ubuntu_theme)
        self.elegantdark_theme_button.clicked.connect(self.elegantdark_theme)
        self.manjaromix_theme_button.clicked.connect(self.manjaromix_theme)
        self.materialdark_theme_button.clicked.connect(self.materialdark_theme)




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
    ######################## day to day operations #########################
    def handle_day_operations(self):
        book_title = self.lineEdit.text()
        book_type = self.rent_comboBox.currentText()
        days = self.days_comboBox.currentIndex()+1
        date = datetime.date.today()
        due_date = date + datetime.timedelta(days=days)


        self.db = pymysql.connect(host='localhost', user='root', password='89412317', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''
            insert into library.dayoperations (`book_name`, `type`, `days`, `Date`, `To`) values (%s, %s, %s, %s, %s)
        ''', (book_title, book_type, days, date, due_date))

        self.db.commit()
        self.statusBar().showMessage('New operation added')
        self.show_day_operation()

    def show_day_operation(self):
        self.db = pymysql.connect(host='localhost', user='root', password='89412317', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''select `book_name`, `type`, `days`, `Date`, `To` from library.dayoperations ''')
        data = self.cur.fetchall()

        self.day_table.setRowCount(0)
        self.day_table.insertRow(0)

        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.day_table.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1
            row_position = self.day_table.rowCount()
            self.day_table.insertRow(row_position)

        self.db.close()


    ########################################################################
    ########################### Books tabs #################################
    def show_all_books(self):
        self.db = pymysql.connect(host='localhost', user='root', password='89412317', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''select `book_code`, `book_name`, `book_description`, `book_category`,
            `book_author`, `book_publisher`, `book_price` from library.book ''')
        data = self.cur.fetchall()

        self.all_book_table.setRowCount(0)
        self.all_book_table.insertRow(0)

        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.all_book_table.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1
            row_position = self.all_book_table.rowCount()
            self.all_book_table.insertRow(row_position)

        self.db.close()

    def add_new_book(self):
        self.db = pymysql.connect(host='localhost', user='root', password='89412317', db='library')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_2.text()
        book_description = self.textEdit.toPlainText()
        book_code = self.lineEdit_3.text()
        book_category = self.category_comboBox.currentText()
        book_author = self.author_comboBox.currentText()
        book_publisher = self.publisher_comboBox.currentText()
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

        self.show_all_books()

    def search_book(self):
        self.db = pymysql.connect(host='localhost', user='root', password='89412317', db='library')
        self.cur = self.db.cursor()

        book_title = self.booktitle_search.text()

        self.cur.execute('''select * from library.book where book_name = %s''', book_title)
        data = self.cur.fetchone()  # if I use fetchall method, the setText method on book title face a crash because in
                                    # this way, fetchall results in a tuple like ((data......),) this mean that our result
                                    # is first element of a tuple. but, what if the query returs more that one output?
        self.lineEdit_5.setText(data[1])
        self.textEdit_2.setText(data[2])
        self.lineEdit_15.setText(data[3])
        self.comboBox_17.setCurrentText(data[4])
        self.comboBox_15.setCurrentText(data[5])
        self.comboBox_16.setCurrentText(data[6])
        self.lineEdit_14.setText(str(data[7]))

    def edit_book(self):
        self.db = pymysql.connect(host='localhost', user='root', password='89412317', db='library')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_5.text()
        book_description = self.textEdit_2.toPlainText()
        book_code = self.lineEdit_15.text()
        book_category = self.comboBox_17.currentText()
        book_author = self.comboBox_15.currentText()
        book_publisher = self.comboBox_16.currentText()
        book_price = self.lineEdit_14.text()

        searched_title = self.booktitle_search.text()

        self.cur.execute('''update library.book set 
            book_name = %s, book_description = %s, book_code = %s, book_category = %s, book_author = %s, 
            book_publisher = %s, book_price = %s
            where book_name = %s '''
            , (book_title, book_description, book_code, book_category, book_author, book_publisher, book_price, searched_title))
        self.db.commit()
        self.statusBar().showMessage('book updated')

        self.show_all_books()

    def delete_book(self):
        self.db = pymysql.connect(host='localhost', user='root', password='89412317', db='library')
        self.cur = self.db.cursor()

        searched_title = self.booktitle_search.text()

        warning = QMessageBox.warning(self, 'Delete Book', 'Are you sure?', QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes:
            self.cur.execute('''delete from library.book where book_name = %s''', searched_title)
            self.db.commit()
            self.statusBar().showMessage('book deleted')

        self.show_all_books()

    ########################################################################
    ########################### users tabs #################################
    def add_new_user(self):
        self.db = pymysql.connect(host='localhost', user='root', password='89412317', db='library')
        self.cur = self.db.cursor()

        user_name = self.user_add.text()
        email = self.email_add.text()
        password = self.pass_add.text()
        conf_password = self.conf_add.text()

        if password == conf_password:
            self.cur.execute('''
                insert into library.users (user_name, user_email, user_password)
                values (%s, %s, %s) 
                ''', (user_name, email, password))
            self.db.commit()
            self.statusBar().showMessage('new user added')
        else:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Warning)
            msgbox.setText('Please make sure passwords are the same')
            msgbox.setWindowTitle("Password error")
            msgbox.setStandardButtons(QMessageBox.Ok)
            msgbox.exec()

        self.user_add.setText('')
        self.email_add.setText('')
        self.pass_add.setText('')
        self.conf_add.setText('')

    def login(self):
        self.db = pymysql.connect(host='localhost', user='root', password='89412317', db='library')
        self.cur = self.db.cursor()

        user_name = self.user_login.text()
        password = self.pass_login.text()

        sql = '''select * from library.users'''
        self.cur.execute(sql)
        all_users = self.cur.fetchall()
        for user in all_users:
            if user_name == user[1] and password == user[3]:
                self.statusBar().showMessage('Valid user information')
                self.edit_user_box.setEnabled(True)

                self.user_edit.setText(user[1])
                self.email_edit.setText(user[2])
                self.pass_edit.setText(user[3])

    def edit_user(self):
        self.db = pymysql.connect(host='localhost', user='root', password='89412317', db='library')
        self.cur = self.db.cursor()

        user_name = self.user_edit.text()
        email = self.email_edit.text()
        password = self.pass_edit.text()
        conf_password = self.conf_edit.text()

        old_user_name = self.user_login.text()

        if password == conf_password:
            self.cur.execute('''
                        update library.users set user_name = %s, user_email = %s, user_password = %s
                        where user_name = %s
                        ''', (user_name, email, password, old_user_name))
            self.db.commit()
            self.statusBar().showMessage('user information updated')
        else:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Warning)
            msgbox.setText('Please make sure passwords are the same')
            msgbox.setWindowTitle("Password error")
            msgbox.setStandardButtons(QMessageBox.Ok)
            msgbox.exec()

        self.user_edit.setText('')
        self.email_edit.setText('')
        self.pass_edit.setText('')
        self.conf_edit.setText('')

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

    ########################################################################
    ########################## UI Theme ####################################

    def ubuntu_theme(self):
        style = open(r'Themes/Ubuntu.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def elegantdark_theme(self):
        style = open(r'Themes/ElegantDark.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def manjaromix_theme(self):
        style = open(r'Themes/ManjaroMix.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def materialdark_theme(self):
        style = open(r'Themes/MaterialDark.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

def main():
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
