import os

from PyQt6.QtCore import Qt
from PyQt6 import QtCore
from PyQt6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QLabel, QLineEdit, QWidget, QPushButton, \
    QHBoxLayout, QFrame, QTextEdit
from PyQt6.QtGui import QFont, QPixmap, QIcon, QTextOption


# Все шрифты для формы профиля администратора
class Fonts:

    @staticmethod
    def get_profile_objects_font():
        font_profile = QFont()
        font_profile.setFamily("Calibri")
        font_profile.setPointSize(20)
        font_profile.setWeight(QFont.Weight.Normal)
        return font_profile

    @staticmethod
    def get_title_font():
        return QFont("Calibri", 18, QFont.Weight.Bold)

    @staticmethod
    def get_exit_button_font():
        return QFont("Calibri", 12, QFont.Weight.Medium)

    @staticmethod
    def get_input_font():
        return QFont("Calibri", 14, QFont.Weight.Normal)


# Форма профиля администратора
class ProfileAdmin(QMainWindow):

    # Инициализация экземпляра класса
    def __init__(self):
        super(ProfileAdmin, self).__init__()
        self.user_login = None
        self.available_size = None
        self.central_widget = None
        self.top_right_widget = None
        self.top_right_layout = None
        self.back_button = None
        self.left_layout = None
        self.left_widget = None
        self.user_icon = None
        self.profile_title = None
        self.separator = None
        self.label_login_title = None
        self.label_login = None
        self.label_password_title = None
        self.label_password = None
        self.exit_button = None
        self.right_widget = None
        self.right_top_layout = None
        self.books_title = None
        self.stats_book = None
        self.add_button = None
        self.name_book_to_delete = None
        self.stats_book_to_delete = None
        self.del_button = None
        self.return_book = None
        self.title_function_send_message = None
        self.line_of_send_message = None
        self.button_of_send_message = None
        self.size = None
        self.left_widget_width = None
        self.left_widget_height = None
        self.left_widget_x = None
        self.left_widget_y = None
        self.setup_ui()

    # Настройка компоновки, размеров, доп. характеристик объектов на форме
    def setup_ui(self):
        self.setup_ui_left()
        self.setup_ui_right()

    # Настройка компоновки левой части формы профиля
    def setup_ui_left(self):
        screen = QApplication.screens()[0]
        self.available_size = screen.availableSize()
        self.setFixedSize(screen.size())
        self.setWindowTitle('Профиль')

        self.central_widget = QWidget(self)
        self.central_widget.setFixedSize(self.available_size)
        self.setCentralWidget(self.central_widget)

        self.left_widget = QWidget(self.central_widget)
        self.left_layout = QVBoxLayout()
        self.left_widget.setLayout(self.left_layout)
        self.size = self.central_widget.size()

        self.left_widget_width = self.size.width() // 4
        self.left_widget_height = self.size.height() // 2 + 150
        self.left_widget_x = (self.size.width() // 2 - self.left_widget_width) // 2
        self.left_widget_y = (self.size.height() - self.left_widget_height) // 2

        self.left_widget.setObjectName('left_widget')
        self.left_widget.setGeometry(
            QtCore.QRect(self.left_widget_x, self.left_widget_y, self.left_widget_width, self.left_widget_height)
        )

        self.left_layout.addSpacing(20)
        self.user_icon = QLabel()
        self.user_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.set_pixmap_image()
        self.left_layout.addWidget(self.user_icon)

        self.left_layout.addSpacing(10)
        self.profile_title = QLabel("Профиль администратора")
        self.profile_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_layout.addWidget(self.profile_title)

        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.Shape.HLine)
        self.left_layout.addWidget(self.separator)

        self.label_login_title = QLabel("Логин:")
        self.left_layout.addWidget(self.label_login_title)

        self.label_login = QLabel("")
        self.left_layout.addWidget(self.label_login)

        self.label_password_title = QLabel("Пароль:")
        self.left_layout.addWidget(self.label_password_title)

        self.label_password = QLabel("")
        self.left_layout.addWidget(self.label_password)

        self.exit_button = QPushButton("Выйти")
        self.left_layout.addWidget(self.exit_button)
        self.left_layout.addStretch()

    # Настройка компоновки правой части формы профиля
    def setup_ui_right(self):
        size = self.central_widget.size()
        right_widgets_width = size.width() // 2
        right_widgets_height = self.left_widget_height

        right_widget_top_x = (size.width() - self.left_widget_width) // 2 + 50
        right_widget_top_y = (size.height() - self.left_widget_height) // 2

        self.right_widget = QWidget(self.central_widget)
        self.right_top_layout = QVBoxLayout()
        self.right_widget.setLayout(self.right_top_layout)
        self.right_widget.setObjectName('right_widget_top')
        self.right_widget.setGeometry(
            QtCore.QRect(right_widget_top_x, right_widget_top_y, right_widgets_width, right_widgets_height)
        )

        const_objects_height = int(0.045 * right_widgets_height)
        small_spacing = int(0.0075 * right_widgets_height)
        big_spacing = int(0.03 * right_widgets_height)
        const_text_line_height = int(0.15 * right_widgets_height)

        self.right_top_layout.addSpacing(big_spacing)
        self.books_title = QLabel('Функция добавления книги')
        self.books_title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.right_top_layout.addWidget(self.books_title)

        self.stats_book = QLineEdit()
        self.stats_book.setPlaceholderText('Введите ссылку на книгу с сайта livelib...')
        self.stats_book.setFixedSize(right_widgets_width - 20, const_objects_height)
        self.stats_book.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.right_top_layout.addSpacing(small_spacing)
        self.right_top_layout.addWidget(self.stats_book)

        self.add_button = QPushButton('Добавить книгу')
        self.right_top_layout.addWidget(self.add_button)
        self.right_top_layout.addSpacing(const_objects_height)

        self.name_book_to_delete = QLabel('Функция удаления/принудительного возвращения книги')
        self.name_book_to_delete.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.right_top_layout.addWidget(self.name_book_to_delete)

        self.stats_book_to_delete = QLineEdit()
        self.stats_book_to_delete.setPlaceholderText('Введите штрихкод книги...')
        self.stats_book_to_delete.setFixedSize(right_widgets_width - 20, const_objects_height)
        self.stats_book_to_delete.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.right_top_layout.addSpacing(small_spacing)
        self.right_top_layout.addWidget(self.stats_book_to_delete)

        self.del_button = QPushButton('Удалить книгу')
        self.return_book = QPushButton('Вернуть книгу')
        self.right_top_layout.addWidget(self.del_button)
        self.right_top_layout.addWidget(self.return_book)
        self.right_top_layout.addSpacing(const_objects_height)

        self.title_function_send_message = QLabel('Функция рассылки сообщений для всех пользователей')
        self.title_function_send_message.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.right_top_layout.addWidget(self.title_function_send_message)

        self.right_top_layout.addSpacing(small_spacing)
        self.line_of_send_message = QTextEdit()
        self.line_of_send_message.setWordWrapMode(QTextOption.WrapMode.WrapAnywhere)
        self.line_of_send_message.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self.line_of_send_message.setPlaceholderText('Введите сообщение для пользователей...')
        self.line_of_send_message.setFixedSize(right_widgets_width - 20, const_text_line_height)
        self.line_of_send_message.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.right_top_layout.addWidget(self.line_of_send_message)

        self.button_of_send_message = QPushButton('Отправить сообщение')
        self.right_top_layout.addWidget(self.button_of_send_message)
        self.right_top_layout.addStretch()

        self.set_fonts()
        self.set_stylesheets()
        self.set_icons()

    # Установка шрифтов
    def set_fonts(self):
        self.profile_title.setFont(Fonts.get_title_font())
        self.label_login_title.setFont(Fonts.get_profile_objects_font())
        self.label_login.setFont(Fonts.get_profile_objects_font())
        self.label_password_title.setFont(Fonts.get_profile_objects_font())
        self.label_password.setFont(Fonts.get_profile_objects_font())
        self.exit_button.setFont(Fonts.get_exit_button_font())
        self.books_title.setFont(Fonts.get_title_font())
        self.name_book_to_delete.setFont(Fonts.get_title_font())
        self.title_function_send_message.setFont(Fonts.get_title_font())
        self.stats_book.setFont(Fonts.get_input_font())
        self.stats_book_to_delete.setFont(Fonts.get_input_font())
        self.line_of_send_message.setFont(Fonts.get_input_font())
        self.add_button.setFont(Fonts.get_input_font())
        self.del_button.setFont(Fonts.get_input_font())
        self.return_book.setFont(Fonts.get_input_font())
        self.button_of_send_message.setFont(Fonts.get_input_font())

    # Установка таблиц стилей
    def set_stylesheets(self):

        self.left_widget.setStyleSheet(f"""
            QWidget#left_widget {{
                background-color: white;
                border-radius: {self.left_widget_height // 8}px;
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
                padding: 30px;
            }}
        """)

        self.profile_title.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
        self.separator.setStyleSheet("color: #bdc3c7; margin: 10px 0px;")
        self.label_login_title.setStyleSheet("color: #2c3e50; margin-top: 10px;")
        self.label_login.setStyleSheet("color: #7f8c8d; margin-top: 10px;")
        self.label_password_title.setStyleSheet("color: #2c3e50; margin-top: 15px;")
        self.label_password.setStyleSheet("color: #7f8c8d; margin-top: 10px;")

        self.exit_button.setStyleSheet("""
                QPushButton {
                    background-color: #808080;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 10px 20px;
                    margin-top: 25px;
                    font-weight: 100;
                }
                QPushButton:hover {
                    background-color: #fe0000;
                }
            """)

        self.right_widget.setStyleSheet(f"""
                QWidget#right_widget_top {{
                    background-color: white;
                    border-radius: {self.left_widget_height // 8}px;
                    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
                }}
            """)

        self.stats_book.setStyleSheet('border-radius: 8px; border: 2px solid black;')
        self.stats_book_to_delete.setStyleSheet('border-radius: 8px; border: 2px solid black;')
        self.line_of_send_message.setStyleSheet('border-radius: 4px; border: 2px solid black;')

        # Общие стили для заголовков в правой части
        title_style = "color: #2c3e50; margin-bottom: 15px;"
        self.books_title.setStyleSheet(title_style)
        self.name_book_to_delete.setStyleSheet(title_style)
        self.title_function_send_message.setStyleSheet(title_style)

    # Установка иконок
    def set_icons(self):
        working_dir = os.getcwd()
        image_window_path = os.path.join(working_dir, "_internal", "icons", "main_picture.png")
        self.setWindowIcon(QIcon(image_window_path))

    # Установка фото профиля
    def set_pixmap_image(self):
        working_dir = os.getcwd()
        image_user_path = os.path.join(working_dir, "_internal", "icons", "user.png")
        pixmap = QPixmap(image_user_path)
        if pixmap.isNull():
            self.user_icon.setText("User Icon")
            self.user_icon.setStyleSheet("""
                    QLabel {
                        background-color: #e0e0e0;
                        border-radius: 50px;
                        width: 100px;
                        height: 100px;
                        font-size: 14px;
                    }
                """)
        else:
            scaled_pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            self.user_icon.setPixmap(scaled_pixmap)
        self.left_layout.addWidget(self.user_icon)

    # Установка логина и пароля
    def set_login_password(self, login, password):
        self.label_password.setText(password)
        self.label_login.setText(login)
