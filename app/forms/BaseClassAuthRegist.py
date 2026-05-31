import os

from PyQt6.QtCore import Qt
from PyQt6 import QtCore
from PyQt6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QLabel, QLineEdit, QWidget, QPushButton, QHBoxLayout
from PyQt6.QtGui import QFont, QIcon
import sys


# Общий класс шрифтов для форм авторизации и регистрации
class Fonts:
    @staticmethod
    def get_main_font():
        font = QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(20)
        font.setWeight(QFont.Weight.Normal)
        return font

    @staticmethod
    def get_login_or_password_font():
        font = QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        font.setWeight(QFont.Weight.Bold)
        return font

    @staticmethod
    def get_label_main_font():
        font = QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setWeight(QFont.Weight.Normal)
        return font

    @staticmethod
    def get_button_font():
        font = QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setWeight(QFont.Weight.Bold)
        return font

    @staticmethod
    def get_back_button_font():
        font = QFont("Calibri", 10, QFont.Weight.Medium)
        return font


# Базовый класс для форм авторизации и регистрации
class BaseAuthForm(QMainWindow):

    # Инициализация экземпляра объекта
    def __init__(self, title_text):
        super().__init__()
        self.title_text = title_text
        self.available_size = None
        self.central_widget = None
        self.vl_image = None
        self.verticalLayoutWidget = None
        self.main_layout = None
        self.label_authorization = None
        self.label_login = None
        self.line_login = None
        self.label_password = None
        self.line_password = None
        self.button_login = None
        self.hl_button = None

        self._setup_common_ui()

    # Настройка компоновки, размеров, доп. характеристик объектов на форме
    def _setup_common_ui(self):
        screen = QApplication.screens()[0]
        self.available_size = screen.availableSize()
        width = screen.size().width()
        height = screen.size().height()
        self.setFixedSize(screen.size())
        self.setWindowTitle(self.title_text)

        container_width = width // 3
        self.container_height = height // 3

        x = (width - container_width) // 2
        y = (height - self.container_height) // 2

        self.central_widget = QWidget(self)

        vl_image_width = width // 2
        vl_image_height = height // 2
        vl_image_x = (width - vl_image_width) // 2
        vl_image_y = (height - vl_image_height) // 2

        self.vl_image = QWidget(self.central_widget)
        self.vl_image.setObjectName('vl_image')
        self.vl_image.setGeometry(
            QtCore.QRect(vl_image_x, vl_image_y, vl_image_width, vl_image_height)
        )

        self.verticalLayoutWidget = QWidget(self)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(
            QtCore.QRect(x, y, container_width, self.container_height)
        )

        self.main_layout = QVBoxLayout(self.verticalLayoutWidget)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Общий заголовок
        self.label_authorization = QLabel(self.title_text)

        self.label_authorization.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Поле логина
        self.label_login = QLabel('Логин: ')

        width_login = self.available_size.width() // 3
        height_login = self.available_size.height() // 30

        self.line_login = QLineEdit()
        self.line_login.setPlaceholderText('Введите логин')
        self.line_login.setFixedSize(width_login, height_login)

        # Поле пароля
        self.label_password = QLabel('Пароль: ')

        self.line_password = QLineEdit()
        self.line_password.setFixedSize(width_login, height_login)
        self.line_password.setPlaceholderText('Введите пароль')

        # Кнопка действия (будет переопределена в наследниках)
        button_width = self.available_size.width() // 8
        self.button_height = self.available_size.height() // 25

        self.button_login = QPushButton()
        self.button_login.setFixedSize(button_width, self.button_height)

        # Горизонтальный layout для кнопки
        self.hl_button = QHBoxLayout()
        self.hl_button.addWidget(self.button_login)

        # Добавляем общие элементы в layout
        self.main_layout.addWidget(self.label_authorization)
        self.main_layout.addSpacing(50)
        self.main_layout.addWidget(self.label_login)
        self.main_layout.addWidget(self.line_login)
        self.main_layout.addSpacing(15)
        self.main_layout.addWidget(self.label_password)
        self.main_layout.addWidget(self.line_password)
        self.main_layout.addSpacing(self.line_password.height() // 2)
        self.main_layout.addLayout(self.hl_button)
        self.main_layout.addSpacing(self.line_password.height() // 2)

        self.set_fonts()
        self.set_stylesheets()
        self.set_icons()
        self.setCentralWidget(self.central_widget)

    # Метод для установки текса на кнопку действия
    def set_button_text(self, text):
        self.button_login.setText(text)

    # Абстрактный метод для настройки специфичных элементов — должен быть переопределён в наследниках
    def setup_specific_ui(self):
        raise NotImplementedError

    def set_fonts(self):
        self.label_authorization.setFont(Fonts.get_main_font())
        self.label_login.setFont(Fonts.get_login_or_password_font())
        self.line_login.setFont(Fonts.get_label_main_font())
        self.label_password.setFont(Fonts.get_login_or_password_font())
        self.line_password.setFont(Fonts.get_label_main_font())

    def set_stylesheets(self):
        self.vl_image.setStyleSheet(f"""
            QWidget#vl_image {{
                background-color: white;
                border-radius: {self.container_height // 5}px;
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
                padding: 30px;
            }}
        """)

        self.button_login.setStyleSheet(f"""
            QPushButton {{
                background-color: #333333;
                color: white;
                border-radius: {self.button_height // 2}px;
                border: none;
                font-size: 18px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #4730f5;
            }}
            QPushButton:pressed {{
                background-color: #333333;
            }}
        """)

    def set_icons(self):
        working_dir = os.getcwd()
        image_window_path = os.path.join(working_dir, "_internal", "icons", "main_picture.png")
        self.setWindowIcon(QIcon(image_window_path))
