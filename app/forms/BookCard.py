from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame

from app.forms.BookCardOpen import BookCardOpen


# Класс шрифтов для закрытой карточки книги на форме библиотеки
class Fonts:

    @staticmethod
    def get_name_font():
        return QFont("Arial", 14, QFont.Weight.Bold)

    @staticmethod
    def get_author_font():
        return QFont("Arial", 12)

    @staticmethod
    def get_genre_font():
        return QFont("Arial", 9)


# Форма закрытой карточка книги, экземпляры данного класса располагаются в виде списка на форме библиотеки
class BookCard(QWidget):

    # Обработчик клика мыши на любой объект формы карточки книги
    def mousePressEvent(self, event):
        self.book_card.close()
        self.book_card.show()
        super(BookCard, self).mousePressEvent(event)

    # Инициализация объекта карточка книги
    def __init__(self, name, author, genres, photo_path, description, ISBN, data, user_login):
        super().__init__()
        self.frame = None
        self.main_layout = None
        self.label_photo = None
        self.label_name = None
        self.label_author = None
        self.label_genre = None
        self.text_layout = None
        self.photo_path = photo_path
        self.book_card = BookCardOpen(photo_path, name, author, genres, description, str(ISBN), data, user_login)
        self.setup_ui(name, author, genres)

    # Настройка компоновки, размеров, доп. характеристик объектов на форме
    def setup_ui(self, name, author, genres):
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setLineWidth(2)

        self.main_layout = QHBoxLayout(self.frame)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.frame)

        self.label_photo = QLabel()
        self.label_photo.setFixedSize(120, 180)

        self.label_photo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.set_pixmap_photo()

        self.text_layout = QVBoxLayout()
        self.text_layout.setSpacing(8)

        self.label_name = QLabel(name)
        self.label_name.setWordWrap(True)

        self.label_author = QLabel(author)

        self.label_genre = QLabel(genres)

        self.text_layout.addWidget(self.label_name)
        self.text_layout.addWidget(self.label_author)
        self.text_layout.addWidget(self.label_genre)

        self.main_layout.addWidget(self.label_photo)
        self.main_layout.addLayout(self.text_layout)

        self.set_fonts()
        self.set_stylesheets()

    # Установка обложки
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

    # Установка шрифтов
    def set_fonts(self):
        self.label_name.setFont(Fonts.get_name_font())
        self.label_author.setFont(Fonts.get_author_font())
        self.label_genre.setFont(Fonts.get_genre_font())

    # Установка таблиц стилей
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
        self.label_genre.setStyleSheet("border: 0px;")

        self.setStyleSheet("""
            QWidget {
                margin: 5px;
            }
        """)
