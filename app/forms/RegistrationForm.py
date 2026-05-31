import os

from PyQt6.QtCore import Qt
from PyQt6 import QtCore
from PyQt6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QLabel, QLineEdit, QWidget, QPushButton, QHBoxLayout
from PyQt6.QtGui import QFont, QIcon
import sys

from app.forms.BaseClassAuthRegist import BaseAuthForm, Fonts


# Класс формы регистрации, наследник базового класса BaseAuthForm
class RegistWindow(BaseAuthForm):
    def __init__(self):
        super().__init__('Окно регистрации')
        self.back_button = None

        # Устанавливаем специфичный текст для кнопки
        self.set_button_text('Зарегистрироваться')

        # Настраиваем специфичные элементы, относительно базового класса
        self.setup_specific_ui()

    def setup_specific_ui(self):
        # Добавляем кнопку «Назад» в форму регистрации
        back_button_width = self.available_size.width() // 20
        back_button_height = back_button_width

        self.back_button = QPushButton(self.central_widget)
        working_dir = os.getcwd()
        image_back_button_path = os.path.join(working_dir, "_internal", "icons", "back.png")
        self.back_button.setIcon(QIcon(image_back_button_path))
        self.back_button.setIconSize(QtCore.QSize(50, 50))
        self.back_button.setToolTip("Вернуться в меню авторизации")
        self.back_button.setFont(Fonts.get_back_button_font())
        self.back_button.setFixedSize(back_button_width, back_button_height)
        self.back_button.setStyleSheet("""
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
                padding: 17px 32px 13px 28px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
                background-color: #21618c;
            }
        """)

        # Размещаем кнопку «Назад» на форме
        self.back_button.move(10, 10)