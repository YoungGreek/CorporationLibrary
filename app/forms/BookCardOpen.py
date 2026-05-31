import os

import datetime
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap, QPainter, QPainterPath, QIcon
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QApplication, QPushButton, \
    QMessageBox

from app.database.Requests import change_status_book


# Класс всех шрифтов для открытой карточки книги на форме библиотеки
class Fonts:

    @staticmethod
    def get_name_font():
        return QFont("Georgia", 20, QFont.Weight.Bold)

    @staticmethod
    def get_author_font():
        return QFont("Georgia", 14, QFont.Weight.Normal, True)

    @staticmethod
    def get_genre_font():
        return QFont("Georgia", 13, QFont.Weight.Normal)

    @staticmethod
    def get_title_characters_label_font():
        return QFont("Georgia", 14, QFont.Weight.Normal, True)

    @staticmethod
    def get_description_font():
        return QFont("Georgia", 11, QFont.Weight.Normal)

    @staticmethod
    def get_ISBN_data_font():
        return QFont("Courier New", 11, QFont.Weight.Normal)


# Форма открытой карточки книги, на форме библиотеки
class BookCardOpen(QMainWindow):

    # Инициализация экземпляра класса
    def __init__(self, photo_path, name, author, genres, description, ISBN, data, user_login):
        super().__init__()
        self.user_login = user_login
        self.photo_path = photo_path
        self.name = name
        self.author = author
        self.description = description
        self.genres = genres
        self.ISBN = ISBN
        self.data = data

        self.central_widget = None
        self.main_layout = None
        self.first_level_layout = None
        self.photo_label = None
        self.main_stats_layout = None
        self.main_stats_widget = None
        self.name_label = None
        self.author_label = None
        self.genres_label = None
        self.description_label = None
        self.button_layout = None
        self.take_button = None
        self.second_level_layout = None
        self.second_stats_layout = None
        self.second_stats_widget = None
        self.data_label = None
        self.title_characters_label = None
        self.ISBN_label = None

        self.setup_ui()

    # Настройка компоновки, размеров, доп. характеристик объектов на форме
    def setup_ui(self):
        self.setWindowTitle('Карточка книги')

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)
        self.first_level_layout = QHBoxLayout()
        self.main_layout.addLayout(self.first_level_layout)

        self.photo_label = QLabel()
        self.photo_label.setFixedSize(350, 450)
        self.photo_label.setScaledContents(True)

        self.set_pixmap_photo()
        self.photo_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.first_level_layout.addSpacing(20)
        self.first_level_layout.addWidget(self.photo_label)
        self.first_level_layout.addSpacing(20)
        self.main_stats_layout = QVBoxLayout()

        self.main_stats_widget = QWidget()
        self.main_stats_widget.setLayout(self.main_stats_layout)

        self.first_level_layout.addWidget(self.main_stats_widget)

        self.name_label = QLabel(self.name)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.name_label.setWordWrap(True)
        self.main_stats_layout.addWidget(self.name_label)
        self.author_label = QLabel(self.author)
        self.author_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.author_label.setWordWrap(True)
        self.main_stats_layout.addWidget(self.author_label)
        self.genres_label = QLabel(self.genres)
        self.genres_label.setWordWrap(True)
        self.genres_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_stats_layout.addWidget(self.genres_label)
        self.description_label = QLabel(self.description)
        self.description_label.setWordWrap(True)
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_stats_layout.addWidget(self.description_label)
        self.first_level_layout.addLayout(self.main_stats_layout)
        self.first_level_layout.addSpacing(20)

        self.main_layout.setSpacing(20)
        self.button_layout = QHBoxLayout()
        self.button_layout.addSpacing(20)
        self.take_button = QPushButton('Взять')
        self.take_button.clicked.connect(self.take_book)

        self.take_button.setFixedWidth(self.photo_label.width())
        self.button_layout.addWidget(self.take_button)
        self.button_layout.addStretch(1)
        self.main_layout.addLayout(self.button_layout)

        self.second_level_layout = QHBoxLayout()
        self.main_layout.addLayout(self.second_level_layout)
        self.second_stats_layout = QVBoxLayout()
        self.second_level_layout.addSpacing(20)

        self.second_stats_widget = QWidget()
        self.second_stats_widget.setFixedWidth(self.photo_label.width())
        self.second_stats_widget.setLayout(self.second_stats_layout)

        self.second_level_layout.addWidget(self.second_stats_widget)

        self.second_level_layout.addSpacing(20)

        self.title_characters_label = QLabel('Характеристики')
        self.title_characters_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.second_stats_layout.addWidget(self.title_characters_label)
        self.data_label = QLabel('Год издания: ' + self.data)
        self.data_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.second_stats_layout.addWidget(self.data_label)
        self.ISBN_label = QLabel('ISBN: ' + self.ISBN)
        self.ISBN_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.second_stats_layout.addWidget(self.ISBN_label)
        self.second_level_layout.addLayout(self.second_stats_layout)
        self.second_level_layout.addStretch(1)

        self.set_fonts()
        self.set_stylesheets()
        self.set_icons()
        self.center_on_screen()

    # Создание округлой картинки
    @staticmethod
    def create_rounded_pixmap(original_pixmap, radius):
        rounded_pixmap = QPixmap(original_pixmap.size())
        rounded_pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(rounded_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        path = QPainterPath()
        path.addRoundedRect(0, 0, original_pixmap.width(), original_pixmap.height(), radius, radius)

        painter.setClipPath(path)
        painter.drawPixmap(0, 0, original_pixmap)

        painter.end()
        return rounded_pixmap

    # Установка обложки книги
    def set_pixmap_photo(self):
        if self.photo_path:
            pixmap = QPixmap(self.photo_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    self.photo_label.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                rounded_pixmap = self.create_rounded_pixmap(scaled_pixmap, 15)
                self.photo_label.setPixmap(rounded_pixmap)
            else:
                self.photo_label.setText("Без обложки")
        else:
            self.photo_label.setText("Без обложки")

    # Установка шрифтов для каждого объекта на форме
    def set_fonts(self):
        self.name_label.setFont(Fonts.get_name_font())
        self.author_label.setFont(Fonts.get_author_font())
        self.genres_label.setFont(Fonts.get_genre_font())
        self.description_label.setFont(Fonts.get_description_font())
        self.title_characters_label.setFont(Fonts.get_title_characters_label_font())
        self.ISBN_label.setFont(Fonts.get_ISBN_data_font())
        self.data_label.setFont(Fonts.get_ISBN_data_font())

    # Установка таблиц стилей для каждого объекта на форме
    def set_stylesheets(self):
        self.photo_label.setStyleSheet("""
                    QLabel {
                        background-color: #f9f9f9;
                        border: 2px solid #e0e0e0;
                        border-radius: 15px;
                        padding: 15px;
                    }
                """)

        self.main_stats_widget.setStyleSheet("""
            QWidget {
                background-color: #f9f9f9;
                border: 2px solid #e0e0e0;
                border-radius: 15px;
                padding: 15px;
            }
        """)

        self.take_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 15px;  /* Закруглённые углы */
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)

        self.second_stats_widget.setStyleSheet("""
                    QWidget {
                        background-color: #f9f9f9;
                        border: 2px solid #e0e0e0;
                        border-radius: 15px;
                        padding: 15px;
                    }
                """)

    def set_icons(self):
        working_dir = os.getcwd()
        image_book_window_path = os.path.join(working_dir, "_internal", "icons", "book_icon.png")
        self.setWindowIcon(QIcon(image_book_window_path))

    # Центрирование открытой карточки книги
    def center_on_screen(self):
        self.adjustSize()

        screen = QApplication.primaryScreen()
        available_geometry = screen.availableGeometry()

        window_geometry = self.frameGeometry()

        x = (available_geometry.width() // 2) - (window_geometry.width() // 2)
        y = (available_geometry.height() // 2) - (window_geometry.height() // 2)

        self.move(x, y)

    # Обработчик нажатия кнопки "Взять"
    def take_book(self):
        signal = change_status_book(self.user_login, self.ISBN)
        mes = QMessageBox()
        if signal == "Взять можно не более трёх книг!":
            mes.setText("Взять можно не более трёх книг!")
        elif signal:
            mes.setText("Книга успешно взята.")
        else:
            mes.setText("Книга уже взята.")
        mes.setWindowTitle('Уведомление')
        mes.exec()
