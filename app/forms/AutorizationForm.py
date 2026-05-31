from PyQt6.QtCore import Qt
from PyQt6 import QtCore
from PyQt6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QLabel, QLineEdit, QWidget, QPushButton, QHBoxLayout
from PyQt6.QtGui import QFont, QIcon
import sys

from app.database.Requests import return_taken_books
from app.forms.BaseClassAuthRegist import BaseAuthForm, Fonts


# Часть кода отвечающая за форму авторизации

# Класс формы авторизации, наследник базового класса BaseAuthForm
class AuthWindow(BaseAuthForm):

    # Инициализация экземпляра класса
    def __init__(self):
        super().__init__('Окно авторизации')
        self.label_registration = None
        self.hl_label = None

        # Устанавливаем специфичный текст для кнопки
        self.set_button_text('Войти')
        self.setup_specific_ui()

    def setup_specific_ui(self):
        # Добавляем элемент для регистрации (ссылку)
        self.label_registration = QLabel()
        self.label_registration.setFont(Fonts.get_label_main_font())
        self.label_registration.setOpenExternalLinks(False)
        self.label_registration.setTextFormat(Qt.TextFormat.RichText)
        self.label_registration.setText('<a href="register">Зарегистрироваться</a>')
        self.label_registration.setStyleSheet('QLabel:hover { text-decoration: underline }')

        # Горизонтальный layout для ссылки регистрации
        self.hl_label = QHBoxLayout()
        self.hl_label.addWidget(self.label_registration)
        self.hl_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Вставляем в основной layout после кнопки
        self.main_layout.addLayout(self.hl_label)
