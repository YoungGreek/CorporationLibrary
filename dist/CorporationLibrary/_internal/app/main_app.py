import datetime
from datetime import date
import sys
import re

import requests as requests
from PyQt6.QtWidgets import QApplication, QMessageBox, QDialog, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from bs4 import BeautifulSoup

from app.forms.AutorizationForm import AuthWindow
from app.forms.RegistrationForm import RegistWindow
from app.forms.BooksForm import BooksWindow
from app.forms.Profile import ProfileWindow
from app.forms.ProfileAdmin import ProfileAdmin

from app.database.Models import sync_main
from app.database.Requests import regist_user, check_login_password, search_book, add_book, add_category, \
    add_relationship, search_category, get_last_index, delete_book, load_default_books, get_reminders, return_book, \
    send_message, return_broadcast_message, search_book_with_new_session


# 1. Всплывающие уведомления
class CustomMessageBox(QDialog):
    def __init__(self, message):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.Window)
        self.setWindowTitle('Уведомление')
        self.setFixedSize(400, 200)

        self.setWindowIcon(QIcon('C:\\Users\\YoungGreek\\PycharmProjects\\OpPIMain\\app\\forms\\book_icon.png'))

        layout = QVBoxLayout()
        label = QLabel(message)
        label.setWordWrap(True)
        button = QPushButton('OK')
        button.clicked.connect(self.accept)

        layout.addWidget(label)
        layout.addWidget(button)
        self.setLayout(layout)

    @staticmethod
    def show_message(message):
        mes = CustomMessageBox(message)
        mes.exec()


# 2. Все для работы с пользователем: регистрация, проверка логина и пароля
class UserService:
    @staticmethod
    def register_user(login: str, password: str) -> bool:
        curr_date = str(date.today())
        return regist_user(login, password, curr_date)

    @staticmethod
    def authenticate_user(login: str, password: str) -> str | None:
        return check_login_password(login, password)

    @staticmethod
    def validate_login(login: str) -> bool:
        if login == '' or not login.isalnum():
            return False
        return True

    @staticmethod
    def validate_password(password: str) -> bool:
        if not password.isalnum() and not password == '':
            return False
        return True


# 3. Парсинг книг с сайта
class BookParser:
    @staticmethod
    def validate_url_format(url: str) -> bool:
        pattern = r'https?://www\.livelib\.ru/book/(\d+)-([\w-]+)'
        return re.match(pattern, url) is not None

    @staticmethod
    def fetch_page_content(url: str) -> str | None:
        try:
            response = requests.get(url)
            return response.text
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def extract_book_name(soup: BeautifulSoup) -> str:
        try:
            return soup.find("h1", class_="bc-header__book-title").text
        except Exception as e:
            print(e)
            return "Без названия"

    @staticmethod
    def extract_book_author(soup: BeautifulSoup) -> str:
        try:
            return soup.find("a", class_="bc-header__book-author-link").text
        except Exception as e:
            print(e)
            return 'Без автора'

    @staticmethod
    def extract_description(soup: BeautifulSoup) -> str:
        try:
            description = soup.find("div", class_="bc-about__annotation").text
            description = description.replace("\n\n", "")
            description = description.replace("  ", "")
            return description
        except Exception as e:
            print(e)
            return 'Описания к данной книге нет.'

    @staticmethod
    def extract_isbn(soup: BeautifulSoup) -> int | None:
        tags_p = soup.find_all("p", class_="bc-info__txt")
        try:
            tag_p = ''
            for tag in tags_p:
                if tag.next == 'ISBN: ':
                    tag_p = tag
                    break
            return int(tag_p.contents[1].text.replace('-', ''))
        except Exception as e:
            print("Не получилось достать штрихкод" + str(e))
            return None

    @staticmethod
    def extract_image_url(soup: BeautifulSoup) -> str | None:
        try:
            return soup.find("img", class_="book-cover__image").attrs.get('src')
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def extract_categories(soup: BeautifulSoup) -> list[str]:
        book_categories = soup.find_all("a", class_="bc-info__link bc-info__link_type_category")
        categories = []
        for category_elem in book_categories:
            curr_book = category_elem.text.replace('\n', '')
            categories.append(curr_book)
        return categories


# 4. Работа с изображениями
class ImageService:
    @staticmethod
    def download_and_save_image(image_url: str, book_id: int) -> str:
        working_dir = os.getcwd()
        photo_path = os.path.join(working_dir, "_internal", "books_photos", f"{book_id}.png")
        try:
            photo = requests.get(image_url)
            if photo.status_code == 200:
                with open(photo_path, 'wb') as f:
                    f.write(photo.content)
            return photo_path
        except Exception as e:
            print(e)
            return ""


# 5. Взаимодействие с БД
class BookDatabaseService:
    @staticmethod
    def is_book_already_in_db(book_id: int) -> bool:
        try:
            book = search_book_with_new_session(book_id)
            return book is not None
        except Exception as e:
            print(e)
            CustomMessageBox.show_message('Не получилось обратиться к базе данных для проверки наличия книги...')
            return True

    @staticmethod
    def process_categories(categories: list[str]):
        for curr_book in categories:
            flg = search_category(curr_book)
            if flg is None:
                db_category = add_category(curr_book)
                last_id = get_last_index()
                add_relationship(last_id + 1, db_category.id)
            else:
                db_category = search_category(curr_book)
                last_id = get_last_index()
                add_relationship(last_id + 1, db_category.id)

    @staticmethod
    def save_book_to_db(photo_path: str, book_name: str, book_author: str, book_id: int, description: str,
                        categories: list[str], source_url: str):
        genres = ', '.join(categories)
        add_book(photo_path=photo_path, name=book_name, author=book_author, barcode=book_id, description=description,
                 genres=genres, url=source_url)

    @staticmethod
    def delete_book(barcode: int) -> bool:
        return delete_book(barcode)

    @staticmethod
    def return_book(barcode: int) -> str | None:
        return return_book(barcode)


# 6. Напоминания о возврате книг
class NotificationService:
    @staticmethod
    def check_date(date_message: str) -> bool:
        mes_date = date_message.split('.')
        year = int(mes_date[0])
        month = int(mes_date[1])
        day = int(mes_date[2])

        curr_date = datetime.datetime.now()
        formatted_curr_date = curr_date.strftime("%Y.%m.%d")
        mas_curr_date = formatted_curr_date.split('.')
        curr_y = int(mas_curr_date[0])
        curr_m = int(mas_curr_date[1])
        curr_d = int(mas_curr_date[2])

        difference = (curr_y - year) * 365 + (curr_m - month) * 30 + (curr_d - day)
        difference = abs(difference)
        if difference % 14 == 0 and difference > 0:
            return True
        return False

    @staticmethod
    def check_reminders(user_login: str) -> list[str]:
        messages = get_reminders(user_login)
        reminder_texts = []
        for message in messages:
            if NotificationService.check_date(message.date):
                reminder_texts.append(message.message)
        return reminder_texts


# 7. Менеджер форм
class WindowManager:
    def __init__(self):
        self.auth_form = AuthWindow()
        self.regist_form = RegistWindow()
        self.books_form = BooksWindow("")
        self.profile_form = None

    def show_auth(self):
        self.hide_all_windows()
        self.auth_form.showMaximized()

    def show_regist(self):
        self.hide_all_windows()
        self.regist_form.showMaximized()

    def show_books(self, user_login: str):
        if self.books_form.user_login == "":
            self.books_form.user_login = user_login
        if self.books_form.search_bar.text() == "":
            books = load_default_books()
            self.books_form.display_default(books, user_login)
        self.hide_all_windows()
        self.books_form.showMaximized()

    def show_profile(self, profile_form, user_login: str):
        self.hide_all_windows()
        if user_login != 'Admin':
            profile_form.user_login = user_login
            profile_form.display_stats()
            profile_form.display_books()

            # Проверка напоминаний о возврате книги
            reminders = NotificationService.check_reminders(user_login)
            for reminder in reminders:
                CustomMessageBox.show_message(reminder)

        profile_form.showMaximized()

    def hide_all_windows(self):
        self.auth_form.hide()
        self.regist_form.hide()
        self.books_form.hide()
        if self.profile_form is not None:
            self.profile_form.hide()


# 8. Основной класс приложения, выполняет функцию контроллера, через который все проходит
class LibraryApp:
    def __init__(self):
        self.user_login = ""
        self.window_manager = WindowManager()
        self.user_service = UserService()
        self.book_parser = BookParser()
        self.image_service = ImageService()
        self.book_db_service = BookDatabaseService()
        self.notification_service = NotificationService()

        self.setup_connectors_auth_regist()
        self.window_manager.auth_form.showMaximized()

    # Подключение обработчиков событий для форм регистрации, авторизации, библиотеки
    def setup_connectors_auth_regist(self):
        # Окно регистрации
        self.window_manager.regist_form.back_button.clicked.connect(self.show_auth)
        self.window_manager.regist_form.line_login.returnPressed.connect(self.registration)
        self.window_manager.regist_form.line_password.returnPressed.connect(self.registration)
        self.window_manager.regist_form.button_login.clicked.connect(self.registration)

        # Окно авторизации
        self.window_manager.auth_form.label_registration.linkActivated.connect(self.show_regist)
        self.window_manager.auth_form.line_login.returnPressed.connect(self.login_in_system)
        self.window_manager.auth_form.line_password.returnPressed.connect(self.login_in_system)
        self.window_manager.auth_form.button_login.clicked.connect(self.login_in_system)

        # Окно библиотеки
        self.window_manager.books_form.to_profile.clicked.connect(self.show_profile)

    # Подключение обработчиков событий для формы профиля
    def setup_connectors_profile(self, admin: bool):
        if admin:
            self.window_manager.profile_form = ProfileAdmin()
            self.window_manager.profile_form.add_button.clicked.connect(self.add_book)
            self.window_manager.profile_form.del_button.clicked.connect(self.del_book)
            self.window_manager.profile_form.return_book.clicked.connect(self.return_book)
            self.window_manager.profile_form.button_of_send_message.clicked.connect(self.send_message)
        else:
            self.window_manager.profile_form = ProfileWindow()
            self.window_manager.profile_form.back_button.clicked.connect(self.show_books)

        self.window_manager.profile_form.exit_button.clicked.connect(self.exit)

    # Открытие форм
    def show_auth(self):
        self.window_manager.show_auth()

    def show_regist(self):
        self.window_manager.show_regist()

    def show_books(self):
        self.window_manager.show_books(self.user_login)

    def show_profile(self):
        self.window_manager.show_profile(self.window_manager.profile_form, self.user_login)

    # Логика регистрации
    def registration(self):

        self.setup_connectors_profile(False)

        login = self.window_manager.regist_form.line_login.text()
        password = self.window_manager.regist_form.line_password.text()

        if self.user_service.validate_login(login) and self.user_service.validate_password(password):
            if login == 'Admin':
                self.setup_connectors_profile(True)
                self.window_manager.profile_form.set_login_password(login, password)
                self.user_login = login
                self.window_manager.books_form.user_login = login
                self.show_profile()
                return

            login_is_unique = self.user_service.register_user(login, password)
            if login_is_unique:
                CustomMessageBox.show_message(f'Вы успешно зарегистрированы!\n'
                                              f'Ваш логин: {login}\n'
                                              f'Ваш пароль: {password}')
                curr_date = str(date.today())
                self.window_manager.profile_form.set_login_password(login, password, curr_date)
                self.user_login = login
                self.window_manager.books_form.user_login = login
                self.show_profile()
            else:
                CustomMessageBox.show_message('Пользователь с таким логином уже существует!')
        else:
            CustomMessageBox.show_message('Проверьте правильность заполнения:\n'
                                          'Логин может содержать только буквы и цифры и не может быть пустым.\n'
                                          'Пароль может содержать только буквы и цифры и не может быть пустым.')

            # Функция, срабатывающая при нажатии кнопки "Войти"

    def login_in_system(self):
        login = self.window_manager.auth_form.line_login.text()
        password = self.window_manager.auth_form.line_password.text()

        if self.user_service.validate_login(login) and self.user_service.validate_password(password):
            if login == 'Admin':
                self.setup_connectors_profile(True)
                self.window_manager.profile_form.set_login_password(login, password)
                self.user_login = login
                self.window_manager.books_form.user_login = login
                self.show_profile()
            else:
                date_of_regist = self.user_service.authenticate_user(login, password)
                if date_of_regist:
                    self.setup_connectors_profile(False)
                    self.window_manager.profile_form.set_login_password(login, password, date_of_regist)
                    self.user_login = login
                    self.show_profile()
                    broadcast_messages = return_broadcast_message(self.user_login)
                    for mes in broadcast_messages:
                        CustomMessageBox.show_message(mes)
                else:
                    CustomMessageBox.show_message('Логин или пароль введены неверно! Повторите попытку.')
        else:
            CustomMessageBox.show_message('Логин или пароль введены неверно! Повторите попытку.')

        # Функция, срабатывающая при нажатии кнопки "Выйти"

    def exit(self):
        self.window_manager.hide_all_windows()
        self.__init__()

        # Функция добавления книги в БД (вызывается из ProfileAdmin)

    def add_book(self):
        try:
            data = self.window_manager.profile_form.stats_book.text()
            if not self.book_parser.validate_url_format(data):
                CustomMessageBox.show_message('Ссылка была введена неверно. Проверьте ссылку и попробуйте ещё раз.')
                return

            page_content = self.book_parser.fetch_page_content(data)
            if not page_content:
                CustomMessageBox.show_message('Не получилось взять данные с сайта... Попробуйте ещё раз.')
                return

            soup = BeautifulSoup(page_content, "lxml")

            book_name = self.book_parser.extract_book_name(soup)
            book_author = self.book_parser.extract_book_author(soup)
            description = self.book_parser.extract_description(soup)
            book_id = self.book_parser.extract_isbn(soup)

            if self.book_db_service.is_book_already_in_db(book_id):
                CustomMessageBox.show_message('Такая книга уже добавлена в базу данных.')
                self.window_manager.profile_form.stats_book.setText("")
                return

            image_url = self.book_parser.extract_image_url(soup)
            photo_path = self.image_service.download_and_save_image(image_url, book_id)

            categories = self.book_parser.extract_categories(soup)
            self.book_db_service.process_categories(categories)

            self.book_db_service.save_book_to_db(
                photo_path, book_name, book_author, book_id, description, categories, data
            )

            CustomMessageBox.show_message('Книга была успешно добавлена!')
            self.window_manager.profile_form.stats_book.setText("")

        except Exception as e:
            print(e)
            CustomMessageBox.show_message(f'Произошла ошибка в функции добавления новой книги: {e}')
            self.window_manager.profile_form.stats_book.setText("")

        # Функция, срабатывающая при нажатии кнопки "Удалить книгу"

    def del_book(self):
        if not self.window_manager.profile_form.stats_book_to_delete.text().isdigit():
            CustomMessageBox.show_message("Штрихкод должен состоять только из цифр!")
            return
        barcode = int(self.window_manager.profile_form.stats_book_to_delete.text())
        try:
            result = self.book_db_service.delete_book(barcode)
            if result:
                CustomMessageBox.show_message("Книга успешно удалена.")
            else:
                CustomMessageBox.show_message(
                    "Ошибка! Не удалось удалить книгу. Возможно книги с таким штрихкодом нет в библиотеке.")
        except Exception as e:
            print(e)
            CustomMessageBox.show_message("Непредвиденная ошибка! Не получилось удалить книгу.")
        self.window_manager.profile_form.stats_book_to_delete.setText('')

        # Функция, срабатывающая при нажатии кнопки "Вернуть книгу"

    def return_book(self):
        if not self.window_manager.profile_form.stats_book_to_delete.text().isdigit():
            CustomMessageBox.show_message("Штрихкод должен состоять только из цифр!")
            return
        barcode = int(self.window_manager.profile_form.stats_book_to_delete.text())
        answer = self.book_db_service.return_book(barcode)
        if answer:
            CustomMessageBox.show_message(answer)
        else:
            CustomMessageBox.show_message(
                "Ошибка! Не удалось вернуть книгу. Возможно книги с таким штрихкодом нет в библиотеке.")
        self.window_manager.profile_form.stats_book_to_delete.setText('')

        # Срабатывает при нажатии кнопки "Отправить сообщение"

    def send_message(self):
        message = self.window_manager.profile_form.line_of_send_message.toPlainText()
        if message:
            send_message(message)
            CustomMessageBox.show_message("Сообщение успешно отправлено всем пользователям!")
        else:
            CustomMessageBox.show_message("Ошибка! Не удалось отправить сообщение.")
        self.window_manager.profile_form.line_of_send_message.setText('')


# Запуск кода
if __name__ == '__main__':
    sync_main()
    app = QApplication(sys.argv)
    library_app = LibraryApp()
    app.exec()
