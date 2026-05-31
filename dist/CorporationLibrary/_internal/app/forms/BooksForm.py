import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QScrollArea, \
    QPushButton, QCheckBox
from PyQt6 import QtCore

from app.database.Requests import load_default_books, search_books_by_name, search_books_by_author
from app.forms.BookCard import BookCard


# Класс шрифтов для формы библиотеки
class Fonts:
    @staticmethod
    def get_search_bar_font():
        return QFont("Calibri", 14, QFont.Weight.Normal)

    @staticmethod
    def get_signal_author_font():
        return QFont('Calibri', 16)


# Форма библиотеки, на которой отображается список книг
class BooksWindow(QMainWindow):

    # Инициализация экземпляра класса
    def __init__(self, user_login):
        super(BooksWindow, self).__init__()
        self.user_login = user_login
        self.central_widget = None
        self.search_bar = None
        self.to_profile = None
        self.signal_author = None
        self.books_layout = None
        self.main_layout = None
        self.search_container = None
        self.search_layout = None
        self.scroll_area = None
        self.center_container = None
        self.center_layout = None
        self.books_container = None
        self.setup_ui()

    # Настройка компоновки, размеров, доп. характеристик объектов на форме
    def setup_ui(self):

        screen = QApplication.screens()[0]
        width = screen.size().width()
        self.setFixedSize(screen.size())
        self.setWindowTitle('Библиотека')

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        container_width = int(width * 2 / 3)

        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.search_container = QWidget()

        self.search_layout = QHBoxLayout(self.search_container)
        self.search_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.search_layout.setContentsMargins(20, 20, 20, 10)

        self.search_bar = QLineEdit()
        self.search_bar.returnPressed.connect(self.display_books)
        self.search_bar.setPlaceholderText('Введите название/автора или ссылку на книгу с сайта livelib...')
        self.search_bar.setFixedSize(container_width // 2, 35)

        self.to_profile = QPushButton()

        self.to_profile.setIconSize(QtCore.QSize(50, 50))
        self.to_profile.setToolTip("Вернуться в главную библиотеку")
        self.to_profile.setFixedSize(60, 60)

        self.signal_author = QCheckBox()
        self.signal_author.setText('Поиск по автору')

        self.search_layout.addSpacing(40)
        self.search_layout.addStretch(1)
        self.search_layout.addWidget(self.search_bar, alignment=Qt.AlignmentFlag.AlignCenter)
        self.search_layout.addWidget(self.signal_author)
        self.search_layout.addStretch(1)
        self.search_layout.addWidget(self.to_profile, alignment=Qt.AlignmentFlag.AlignRight)

        self.main_layout.addWidget(self.search_container)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.center_container = QWidget()
        self.center_layout = QHBoxLayout(self.center_container)
        self.center_layout.setContentsMargins(0, 0, 0, 0)
        self.center_layout.setSpacing(0)

        self.books_container = QWidget()
        self.books_container.setFixedWidth(container_width)

        self.books_layout = QVBoxLayout(self.books_container)
        self.books_layout.setContentsMargins(20, 10, 20, 20)
        self.books_layout.setSpacing(25)

        self.center_layout.addStretch(1)
        self.center_layout.addWidget(self.books_container, alignment=Qt.AlignmentFlag.AlignCenter)
        self.center_layout.addStretch(1)

        self.scroll_area.setWidget(self.center_container)

        self.main_layout.addWidget(self.scroll_area, 1)

        books = load_default_books()
        self.set_fonts()
        self.set_stylesheet_for_all()
        self.set_icons()
        self.display_default(books, self.user_login)

    # Функция, для отображения книг по умолчанию, при создании формы
    def display_default(self, books, user_login):
        for i in reversed(range(self.books_layout.count())):
            widget = self.books_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        if not books:
            print("Список книг пуст!")
            return

        for book in books:
            book_card = BookCard(
                name=book.book_name,
                author=book.book_author,
                genres=book.book_genres,
                photo_path=book.photo_path,
                description=book.book_description,
                ISBN=book.book_barcode,
                data="11.01.2005",
                user_login=user_login
            )
            self.books_layout.addWidget(book_card)

        self.books_layout.addStretch()

    # Функция для отображения книг, при повторном открытии формы, в соответствии со строкой поиска
    def display_books(self):
        if self.search_bar.text() != "":
            for i in reversed(range(self.books_layout.count())):
                widget = self.books_layout.itemAt(i).widget()
                if widget:
                    widget.deleteLater()

            if self.signal_author.isChecked():
                author = self.search_bar.text()
                books = search_books_by_author(author)
            else:
                book_name = self.search_bar.text()
                books = search_books_by_name(book_name)

            for book in books:
                book_card = BookCard(
                    name=book.book_name,
                    author=book.book_author,
                    genres=book.book_genres,
                    photo_path=book.photo_path,
                    description=book.book_description,
                    ISBN=book.book_barcode,
                    data="11.01.2005",
                    user_login=self.user_login
                )
                self.books_layout.addWidget(book_card)

            self.books_layout.addStretch()
        else:
            books = load_default_books()
            self.display_default(books, self.user_login)

    # Установка шрифтов
    def set_fonts(self):
        self.search_bar.setFont(Fonts.get_search_bar_font())
        self.signal_author.setFont(Fonts.get_signal_author_font())

    # Установка таблиц стилей
    def set_stylesheet_for_all(self):
        self.signal_author.setStyleSheet("""
            QCheckBox {
                color: white;
            }
            QCheckBox::indicator {
                width: 31px;
                height: 31px;
                border: 2px solid #eee;
                background-color: white;
                border-radius: 4px;
            }
            QCheckBox::indicator:checked {
                background-color: black;
            } 
            """)

        self.to_profile.setStyleSheet("""
                   QPushButton {
                       background-color: #f0f0f0;
                       color: white;
                       border: none;
                       box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                   }
                   QPushButton:hover {
                       background-color: rgba(0, 0, 0, 0.1);
                       border-radius: 4px;
                       box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
                   }
                   QPushButton:pressed {
                       /* Сдвигаем кнопку вниз и вправо при нажатии */
                       padding: 17px 32px 13px 28px;
                       /* Уменьшаем тень — имитирует нажатие */
                       box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
                       /* Тёмный фон при нажатии */
                       background-color: #eee;
               """)

        self.search_bar.setStyleSheet("background-color: white; border: 2px solid #eee; border-radius: 4px")

        self.search_container.setStyleSheet("background-color: #5B3A29")

    # Установка иконок
    def set_icons(self):
        working_dir = os.getcwd()
        image_window_path = os.path.join(working_dir, "_internal", "icons", "main_picture.png")
        image_to_profile_path = os.path.join(working_dir, "_internal", "icons", "to_profile.png")
        self.to_profile.setIcon(QIcon(image_to_profile_path))
        self.setWindowIcon(QIcon(image_window_path))
