from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame, QPushButton

from app.database.Requests import return_book_to_library


# Класс шрифтов для карточки книги на форме профиля
class Fonts:

    @staticmethod
    def get_name_font():
        return QFont("Arial", 12, QFont.Weight.Bold)

    @staticmethod
    def get_author_font():
        return QFont("Arial", 9)

    @staticmethod
    def get_button_font():
        return QFont("Arial", 12)


# Форма карточки книги на форме профиля
class BookCardOpenInProfile(QWidget):
    # Используется для сигнала о том, что на форме карточки книги на форме профиля нажата кнопка вернуть
    book_returned = pyqtSignal()

    # Инициализация экземпляра класса
    def __init__(self, name, author, photo_path, book_barcode, user_login):
        super().__init__()
        self.main_layout = None
        self.label_photo = None
        self.text_layout = None
        self.label_name = None
        self.label_author = None
        self.return_button = None
        self.book_barcode = book_barcode
        self.user_login = user_login
        self.photo_path = photo_path
        self.setup_ui(name, author)

    # Настройка компоновки, размеров, доп. характеристик объектов на форме
    def setup_ui(self, name, author):
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setLineWidth(2)

        self.main_layout = QHBoxLayout(self.frame)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.frame)

        self.label_photo = QLabel()
        self.label_photo.setFixedSize(80, 120)

        self.label_photo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.set_pixmap_photo()

        self.text_layout = QVBoxLayout()
        self.text_layout.setSpacing(8)

        self.label_name = QLabel(name)
        self.label_name.setWordWrap(True)

        self.label_author = QLabel(author)

        self.return_button = QPushButton('Вернуть книгу в библиотеку')
        self.return_button.clicked.connect(self.return_book)

        self.return_button.setFixedHeight(40)

        self.text_layout.addWidget(self.label_name)
        self.text_layout.addWidget(self.label_author)
        self.text_layout.addWidget(self.return_button)

        self.main_layout.addWidget(self.label_photo)
        self.main_layout.addLayout(self.text_layout)

        self.set_fonts()
        self.set_stylesheets()

    # Установка обложки книги
    def set_pixmap_photo(self):
        if self.photo_path:
            pixmap = QPixmap(self.photo_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    self.label_photo.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.label_photo.setPixmap(scaled_pixmap)
            else:
                self.label_photo.setText("Без обложки")
        else:
            self.label_photo.setText("Без обложки")

    # Установка шрифтов для каждого объекта на форме
    def set_fonts(self):
        self.label_name.setFont(Fonts.get_name_font())
        self.label_author.setFont(Fonts.get_author_font())
        self.return_button.setFont(Fonts.get_button_font())

    # Установка таблиц стилей для каждого объекта на форме
    def set_stylesheets(self):
        self.frame.setStyleSheet("""
                    QFrame {
                        border: 2px solid #333;
                        border-radius: 8px;
                        background-color: white;
                        margin: 5px;
                        padding: 4px;
                    }
                    QFrame:hover {
                        border: 2px solid #5B3A29;
                        background-color: #eee;
                    }
                """)
        self.label_photo.setStyleSheet("border: 0px;")
        self.label_name.setStyleSheet("border: 0px;")
        self.label_author.setStyleSheet("border: 0px; color: #555;")

        self.return_button.setStyleSheet("""
                   QPushButton {
                       background-color: #ff4a4a;
                       color: black;
                       border: none;
                       border-radius: 4px;
                       box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                   }
                    QPushButton:hover {
                        background-color: #d63a3a;
                    }
                    QPushButton:pressed {
                        background-color: #ab3030;
                    }
               """)

        self.setStyleSheet("""
            QWidget {
                margin: 5px;
            }
        """)

    # Обработчик события: нажата кнопка "Вернуть" напротив книги, в форме профиля
    def return_book(self):
        return_book_to_library(self.user_login, self.book_barcode)
        self.book_returned.emit()
