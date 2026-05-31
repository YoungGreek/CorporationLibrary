from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
from sqlalchemy import create_engine, BigInteger, String, Integer, ForeignKey, Boolean

from typing import List

# В этой части кода я создаю движок и подключение к БД. Здесь же описываются все таблицы БД.

engine = create_engine(url='sqlite:///db.sqlite3')

Session = sessionmaker(engine)


# Базовый класс
class Base(DeclarativeBase):
    pass


# Таблица с данными о книгах
class Book(Base):
    __tablename__ = 'Book'

    id: Mapped[int] = mapped_column(primary_key=True)
    book_author: Mapped[str] = mapped_column(String(50))
    book_author_to_search: Mapped[str] = mapped_column(String(50))
    book_barcode = mapped_column(BigInteger)
    book_name_to_search: Mapped[str] = mapped_column(String(50))
    book_name: Mapped[str] = mapped_column(String(50))
    photo_path: Mapped[str] = mapped_column(String(100))
    book_description: Mapped[str] = mapped_column(String(300))
    book_href: Mapped[str] = mapped_column(String(100))
    book_genres: Mapped[str] = mapped_column(String(150))

    book_status: Mapped[bool] = mapped_column(Boolean)
    book_owner: Mapped[int] = mapped_column(Integer, ForeignKey('Users.id'), nullable=True)

    owner: Mapped["Users"] = relationship(back_populates="taken_books")
    categories: Mapped[List["Categories"]] = relationship(secondary='BooksCategories', back_populates='books')


# Таблица книжных категорий
class Categories(Base):
    __tablename__ = 'Categories'
    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(String(50))

    books: Mapped[List["Book"]] = relationship(secondary='BooksCategories', back_populates='categories')


# Таблица связи между книгами и категориями
class BooksCategories(Base):
    __tablename__ = 'BooksCategories'
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey('Book.id'), primary_key=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('Categories.id'), primary_key=True)


# Таблица с данными о пользователях
class Users(Base):
    __tablename__ = 'Users'
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(50))
    date: Mapped[str] = mapped_column(String(10))
    count_taken_books: Mapped[int] = mapped_column(Integer)
    count_books_to_return: Mapped[int] = mapped_column(Integer)

    taken_books: Mapped[List["Book"]] = relationship(back_populates="owner")


# Таблица, хранящая все напоминания о возврате книг, всплывают раз в 14 дней
class Messages(Base):
    __tablename__ = 'Messages'
    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str] = mapped_column(String(500))
    date: Mapped[str] = mapped_column(String(10))
    book_id: Mapped[int] = mapped_column(Integer)
    user_login: Mapped[str] = mapped_column(String(50))


# Таблица, хранящая сообщения отправленные администратором, сообщения всплывают 1 раз
class BroadcastMessages(Base):
    __tablename__ = 'BroadcastMessages'
    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str] = mapped_column(String(500))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('Users.id'))
    is_show: Mapped[bool] = mapped_column(Boolean)


# Создание подключения к БД
def sync_main():
    Base.metadata.create_all(engine)
