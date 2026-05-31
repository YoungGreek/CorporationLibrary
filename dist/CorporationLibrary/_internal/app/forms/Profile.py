import os

from PyQt6.QtCore import Qt
from PyQt6 import QtCore
from PyQt6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QLabel, QWidget, QPushButton, \
    QHBoxLayout, QFrame, QScrollArea
from PyQt6.QtGui import QFont, QPixmap, QIcon

from app.database.Requests import return_taken_books, get_stats

from app.forms.BookCardInProfile import BookCardOpenInProfile


# Все шрифты для формы профиля
class Fonts:
    @staticmethod
    def get_back_button_font():
        return QFont("Calibri", 10, QFont.Weight.Medium)

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
    def get_stats_font():
        return QFont("Calibri", 14)


# Форма профиля пользователя
class ProfileWindow(QMainWindow):

    # Инициализация экземпляра объекта
    def __init__(self):
        super(ProfileWindow, self).__init__()

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
        self.reg_data_title = None
        self.reg_data = None
        self.exit_button = None
        self.scroll_area = None
        self.right_widget_top = None
        self.right_top_layout = None
        self.books_title = None
        self.books_widget = None
        self.books_layout = None
        self.right_widget_bottom = None
        self.right_bottom_layout = None
        self.stats_title = None
        self.first_level_layout = None
        self.count_taken_books = None
        self.first_level_layout = None
        self.second_level_layout = None
        self.count_books_to_return = None
        self.size = 1
        self.left_widget_width = 1
        self.left_widget_height = 1
        self.left_widget_x = 0
        self.left_widget_y = 0
        self.setup_ui()

    # Настройка компоновки, размеров, доп. характеристик объектов на форме
    def setup_ui(self):
        self.setup_ui_left()
        self.setup_ui_right()

    # Настройка компоновки правой части формы профиля
    def setup_ui_right(self):
        self.top_right_widget = QWidget(self.central_widget)
        self.top_right_layout = QHBoxLayout()
        self.top_right_widget.setLayout(self.top_right_layout)

        size = self.central_widget.size()
        right_widgets_width = size.width() // 2
        right_widgets_height = self.left_widget_height

        const_back_button_height = int(0.075 * right_widgets_height)

        tr_widget_width = self.available_size.width() // 20
        tr_widget_height = tr_widget_width
        tr_widget_x = 0
        tr_widget_y = 0

        self.top_right_widget.setObjectName('top_right')
        self.top_right_widget.setGeometry(QtCore.QRect(
            tr_widget_x, tr_widget_y, tr_widget_width + 20, tr_widget_height + 20
        ))
        self.top_right_widget.setContentsMargins(0, 0, 0, 0)

        self.back_button = QPushButton()
        self.back_button.setIconSize(QtCore.QSize(const_back_button_height, const_back_button_height))
        self.back_button.setToolTip("Вернуться в главную библиотеку")

        self.back_button.setFixedSize(tr_widget_width, tr_widget_height)

        self.top_right_layout.addWidget(self.back_button)
        right_widgets_width = self.size.width() // 2
        right_widgets_height = self.left_widget_height // 2 - 10

        right_widget_top_x = (self.size.width() - self.left_widget_width) // 2 + 50
        right_widget_top_y = (self.size.height() - self.left_widget_height) // 2

        right_widget_bottom_x = (self.size.width() - self.left_widget_width) // 2 + 50
        right_widget_bottom_y = right_widget_top_y + right_widgets_height + 20

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.right_widget_top = QWidget(self.central_widget)
        self.right_top_layout = QVBoxLayout()
        self.right_widget_top.setLayout(self.right_top_layout)
        self.right_widget_top.setObjectName('right_widget_top')
        self.right_widget_top.setGeometry(
            QtCore.QRect(right_widget_top_x, right_widget_top_y, right_widgets_width, right_widgets_height)
        )

        self.right_top_layout.addSpacing(10)
        self.books_title = QLabel('Взятые книги')

        self.books_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.right_top_layout.addWidget(self.books_title)

        self.books_widget = QWidget()
        self.books_layout = QVBoxLayout()
        self.books_widget.setLayout(self.books_layout)
        self.scroll_area.setWidget(self.books_widget)
        self.scroll_area.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.scroll_area.setFixedHeight(right_widgets_height // 2 + 40)
        self.right_top_layout.addWidget(self.scroll_area)
        self.right_top_layout.addStretch(1)

        self.right_widget_bottom = QWidget(self.central_widget)
        self.right_bottom_layout = QVBoxLayout()
        self.right_widget_bottom.setLayout(self.right_bottom_layout)

        self.right_widget_bottom.setObjectName('right_widget_bottom')
        self.right_widget_bottom.setGeometry(
            QtCore.QRect(right_widget_bottom_x, right_widget_bottom_y, right_widgets_width, right_widgets_height)
        )

        self.right_bottom_layout.addSpacing(10)
        self.stats_title = QLabel('Статистика')
        self.stats_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.first_level_layout = QHBoxLayout()
        self.first_level_layout.addSpacing(20)
        self.count_taken_books = QLabel('Количество взятых книг: ')
        self.count_taken_books.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.first_level_layout.addWidget(self.count_taken_books)
        self.first_level_layout.addStretch(1)

        self.second_level_layout = QHBoxLayout()
        self.second_level_layout.addSpacing(20)
        self.count_books_to_return = QLabel('Нужно вернуть книг: ')
        self.count_books_to_return.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.second_level_layout.addWidget(self.count_books_to_return)
        self.second_level_layout.addStretch(1)

        self.right_bottom_layout.addWidget(self.stats_title)
        self.right_bottom_layout.addLayout(self.first_level_layout)
        self.right_bottom_layout.addLayout(self.second_level_layout)
        self.right_bottom_layout.addStretch(1)

        self.set_fonts()
        self.set_stylesheets()
        self.set_icons()

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

        self.left_widget_height = int(self.size.height() // 3 * 2)
        self.left_widget_x = (self.size.width() // 2 - self.left_widget_width) // 2
        self.left_widget_y = (self.size.height() - self.left_widget_height) // 2

        self.left_widget.setObjectName('left_widget')
        self.left_widget.setGeometry(
            QtCore.QRect(self.left_widget_x, self.left_widget_y, self.left_widget_width, self.left_widget_height)
        )

        small_spacing = int(0.014 * self.left_widget_height)
        big_spacing = int(0.03 * self.left_widget_height)

        self.left_layout.addSpacing(big_spacing)
        self.user_icon = QLabel()
        self.user_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.set_pixmap_image()

        self.left_layout.addSpacing(small_spacing)

        self.profile_title = QLabel("Профиль пользователя")
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

        self.reg_data_title = QLabel("Дата регистрации:")
        self.left_layout.addWidget(self.reg_data_title)

        self.reg_data = QLabel("")
        self.left_layout.addWidget(self.reg_data)

        self.exit_button = QPushButton("Выйти")
        self.left_layout.addWidget(self.exit_button)
        self.left_layout.addStretch()

    # Установка логина и пароля
    def set_login_password(self, login, password, data):
        self.label_password.setText(password)
        self.label_login.setText(login)
        self.reg_data.setText(data)

    # Отображение книг, которые были взяты
    def display_books(self):
        for i in reversed(range(self.books_layout.count())):
            widget = self.books_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        books = return_taken_books(self.user_login)
        for book in books:
            book_card = BookCardOpenInProfile(book.book_name, book.book_author, book.photo_path,
                                              book.book_barcode, self.user_login)
            book_card.book_returned.connect(self.handle_book_return)
            self.books_layout.addWidget(book_card)

    # Отображение статистики
    def display_stats(self):
        stats = get_stats(self.user_login)
        self.count_taken_books.setText('Количество книг, которые были взяты: ' + str(stats[0]))
        self.count_books_to_return.setText('Нужно вернуть книг: ' + str(stats[1]))

    # Вспомогательная функция для отображения статистики
    def handle_book_return(self):
        self.display_books()
        self.display_stats()

    # Установка шрифтов
    def set_fonts(self):
        self.back_button.setFont(Fonts.get_back_button_font())
        self.profile_title.setFont(Fonts.get_title_font())
        self.label_login_title.setFont(Fonts.get_profile_objects_font())
        self.label_login.setFont(Fonts.get_profile_objects_font())
        self.label_password_title.setFont(Fonts.get_profile_objects_font())
        self.label_password.setFont(Fonts.get_profile_objects_font())
        self.reg_data_title.setFont(Fonts.get_profile_objects_font())
        self.reg_data.setFont(Fonts.get_profile_objects_font())
        self.exit_button.setFont(Fonts.get_exit_button_font())
        self.books_title.setFont(Fonts.get_title_font())
        self.stats_title.setFont(Fonts.get_title_font())
        self.count_taken_books.setFont(Fonts.get_stats_font())
        self.count_books_to_return.setFont(Fonts.get_stats_font())

    # Установка таблиц стилей
    def set_stylesheets(self):
        self.top_right_widget.setStyleSheet(f"""
                    QWidget#top_right {{
                    background-color: #f0f0f0;}}    
        """)

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

        self.left_widget.setStyleSheet(f"""
                    QWidget#left_widget {{
                    background-color: white;
                    border-radius: {self.left_widget_height // 8}px; /* Скруглённые углы */
                    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1); /* Тень для объёма */
                    padding: 30px; /* Отступы внутри формы */ }}    
        """)

        self.profile_title.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
        self.separator.setStyleSheet("color: #bdc3c7; margin: 10px 0px;")
        self.label_login_title.setStyleSheet("color: #2c3e50; margin-top: 10px;")
        self.label_login.setStyleSheet("color: #7f8c8d; margin-top: 10px;")
        self.label_password_title.setStyleSheet("color: #2c3e50; margin-top: 15px;")
        self.label_password.setStyleSheet("color: #7f8c8d; margin-top: 10px;")
        self.reg_data_title.setStyleSheet("color: #2c3e50; margin-top: 15px;")
        self.reg_data.setStyleSheet("color: #7f8c8d; margin-top: 10px;")

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

        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: white;
            }

            QScrollBar:vertical {
                background: #f8f9fa;
                width: 12px;
                margin: 0px;
                border-radius: 6px;
            }

            QScrollBar::handle:vertical {
                background: #6c757d;
                min-height: 30px;
                border-radius: 6px;
                margin: 2px;
            }

            QScrollBar::handle:vertical:hover {
                background: #495057;
            }

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }

            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

        self.right_widget_top.setStyleSheet(f"""
                    QWidget#right_widget_top {{
                    background-color: white;
                    border-radius: {self.left_widget_height // 8}px; /* Скруглённые углы */
                    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1); /* Тень для объёма */
                    padding: 30px; /* Отступы внутри формы */ }}    
        """)

        self.books_title.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")

        self.right_widget_bottom.setStyleSheet(f"""
                            QWidget#right_widget_bottom {{
                            background-color: white;
                            border-radius: {self.left_widget_height // 8}px; /* Скруглённые углы */
                            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1); /* Тень для объёма */
                            padding: 30px; /* Отступы внутри формы */ }}    
                """)

        self.books_widget.setStyleSheet("background-color: white;")
        self.stats_title.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")

    # Установка иконок
    def set_icons(self):
        working_dir = os.getcwd()
        image_window_path = os.path.join(working_dir, "_internal", "icons", "main_picture.png")
        image_back_button_path = os.path.join(working_dir, "_internal", "icons", "back.png")
        self.setWindowIcon(QIcon(image_window_path))
        self.back_button.setIcon(QIcon(image_back_button_path))

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
