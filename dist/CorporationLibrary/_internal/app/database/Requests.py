import datetime

from app.database.Models import Session
from app.database.Models import Book, Users, Categories, BooksCategories, Messages, BroadcastMessages

from sqlalchemy import select, func
import os


# Эта часть кода отвечает за запросы к базе данных


# Регистрация нового пользователя
def regist_user(login, password, date):
    session = Session()
    try:
        existing_user = session.query(Users).filter(Users.login == login).first()
        if existing_user:
            return False
        user = Users(login=login, password=password, date=date, count_taken_books=0, count_books_to_return=0)
        session.add(user)
        session.commit()
        return True

    except Exception as e:
        raise e
    finally:
        session.close()


# Используется для проверки логина и пароля
def check_login_password(login, password):
    session = Session()
    try:
        user = session.query(Users).filter(Users.login == login).first()
        if user:
            if user.password == password:
                return user.date
        return False

    except Exception as e:
        raise e
    finally:
        session.close()


# Используется для загрузки списка книг по умолчанию на форму библиотеки
def load_default_books():
    session = Session()

    try:
        book_connect = session.query(Book).limit(100)
        if book_connect:
            return book_connect.all()
        return False

    except Exception as e:
        raise e
    finally:
        session.close()


# Добавление новой книги
def add_book(photo_path, name, author, barcode, description, genres, url):
    session = Session()
    db_book = Book(book_barcode=barcode, book_name_to_search=name.lower(), book_name=name,
                   book_href=url, book_author=author, book_author_to_search=author.lower(),
                   photo_path=photo_path, book_description=description, book_genres=genres, book_status=False)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    session.close()
    return db_book


# Поиск категории в БД
def search_category(category_name):
    session = Session()
    category = session.query(Categories).where(Categories.category == category_name)
    session.close()
    return category.first()


# Поиск книги с созданием новой сессии (для использования из main_app)
def search_book_with_new_session(book_id):
    session = Session()
    book = session.query(Book).where(Book.book_barcode == book_id).first()
    session.close()
    return book


# Добавление новой категории в таблицу категорий
def add_category(category_name):
    session = Session()
    db_category = Categories(category=category_name)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    session.close()
    return db_category


# Создание отношения между книгой и категорией при добавлении книги
def add_relationship(book_id, category_id):
    session = Session()
    db_relationship = BooksCategories(book_id=book_id, category_id=category_id)
    session.add(db_relationship)
    session.commit()
    session.refresh(db_relationship)
    session.close()
    return db_relationship


def get_last_index():
    session = Session()
    book_id = session.query(Book).order_by(Book.id.desc()).first()

    if book_id:
        session.close()
        return book_id.id

    session.close()
    return 0


# Удаление книги из списка
def delete_book(book_barcode):
    session = Session()
    book = search_book(session, book_barcode)
    if book:
        delete_relationships_and_categories(session, book.id)
        if book.book_owner:
            update_user_on_book_delete(session, book)
        del_photo_of_deleted_book(book)
        session.delete(book)
        session.commit()
        session.close()
        return True
    else:
        print('Не удалось найти книгу.')
        return False


# Вспомогательная функция для удаления книги: удаляет отношения между книгой и категориями
def delete_relationships_and_categories(session, book_id):
    relationships = session.query(BooksCategories).where(BooksCategories.book_id == book_id).all()
    if relationships:
        category_to_delete = []
        for relationship in relationships:
            categories = session.query(BooksCategories).where(
                BooksCategories.category_id == relationship.category_id).all()
            if len(categories) == 1:
                category_to_delete.append(relationship.category_id)

        for rel in relationships:
            session.delete(rel)

        for category_id in category_to_delete:
            category = session.query(Categories).where(Categories.id == category_id).first()
            session.delete(category)
    else:
        print('Не удалось найти отношения между книгой и категориями.')


# Вспомогательная функция для удаления книги: обновляет статистику взятых книг у пользователя
def update_user_on_book_delete(session, book):
    user = session.query(Users).where(Users.id == book.book_owner).first()
    if user.count_books_to_return > 0:
        user.count_books_to_return = user.count_books_to_return - 1
    message = session.query(Messages).where(Messages.user_login == user.login).first()
    if message:
        session.delete(message)


# Вспомогательная функция для удаления книги: удаляет обложку книги из сохранённых
def del_photo_of_deleted_book(book):
    try:
        photo_path = f'C:\\Users\\YoungGreek\\PycharmProjects\\OpPIMain\\books_photos\\{book.book_barcode}.png'
        os.remove(photo_path)
    except Exception as e:
        print(e)


# Поиск пользователя в таблице пользователей по логину
def search_user(session, user_login):
    return session.query(Users).where(Users.login == user_login).first()


# Поиск книги в таблице книг по штрихкоду
def search_book(session, book_barcode):
    return session.query(Book).where(Book.book_barcode == book_barcode).first()


# Взятие книги пользователем
def change_status_book(user_login, book_id):
    session = Session()
    user = search_user(session, user_login)
    book = search_book(session, int(book_id))
    if book and user:
        if not book.book_status:
            if user.count_books_to_return < 3:
                session.add(book)
                session.add(user)

                book.book_status = True
                book.owner = user

                user.count_taken_books = user.count_taken_books + 1
                user.count_books_to_return = user.count_books_to_return + 1
                create_message(session, book, user_login)
                session.commit()
                session.close()
                return True
            else:
                session.close()
                return "Взять можно не более трёх книг!"
    session.close()
    return False


# Вспомогательная функция для взятия книги: создает напоминание о возврате
def create_message(session, book, user_login):
    mes = 'Уважаемый пользователь, не забудьте вернуть книгу: \"' + book.book_name + '\"'
    date = datetime.datetime.now()
    formatted_date = date.strftime("%Y.%m.%d")
    message = Messages(message=mes, date=formatted_date, book_id=book.id, user_login=user_login)
    session.add(message)


# Вспомогательная функция, возвращает список книг взятых пользователем
def return_taken_books(user_login):
    session = Session()
    user = search_user(session, user_login)
    books = session.query(Book).where(Book.book_owner == user.id).all()
    session.close()
    return books


# Используется для вывода статистики на форму профиля пользователя
def get_stats(user_login):
    session = Session()
    user = search_user(session, user_login)
    stats = []
    if user.count_taken_books is None:
        stats.append(0)
    else:
        stats.append(user.count_taken_books)
    books = return_taken_books(user_login)
    if not books:
        stats.append(0)
    else:
        stats.append(len(books))
    session.close()
    return stats


# Используется при нажатии кнопки "Вернуть" на форме профиля пользователя
def return_book_to_library(user_login, book_barcode):
    session = Session()
    user = search_user(session, user_login)
    book = search_book(session, book_barcode)
    if user and book:
        session.add(user)
        session.add(book)

        book.book_status = False
        book.book_owner = None

        if user.count_books_to_return:
            user.count_books_to_return = user.count_books_to_return - 1

        delete_reminder(session, book_barcode, user_login)
        session.commit()
        session.close()


# Вспомогательная функция для удаления напоминания о возврате
def delete_reminder(session, book_barcode, user_login):
    reminder = session.query(Messages).where(Messages.book_id == book_barcode,
                                             Messages.user_login == user_login).first()
    if reminder:
        session.add(reminder)
        session.delete(reminder)
    else:
        print('Не удалось найти напоминание')


# Вспомогательная функция для вывода на экран напоминаний
def get_reminders(user_login):
    session = Session()
    messages = session.query(Messages).where(Messages.user_login == user_login).all()
    session.close()
    return messages


# Принудительное возвращение книги в библиотеку (функция для админа)
def return_book(book_barcode):
    session = Session()
    book = search_book(session, book_barcode)
    if book:
        if book.book_status:
            session.add(book)
            user = session.query(Users).where(Users.id == book.book_owner).first()
            if user:
                session.add(user)
                if user.count_books_to_return:
                    user.count_books_to_return = user.count_books_to_return - 1
                    book.book_owner = None
                    book.book_status = False
                    delete_reminder(session, book_barcode, user.login)
                    session.commit()
                    session.close()
                    return "Книга успешно возвращена в библиотеку."
        else:
            session.close()
            return "Не удалось вернуть книгу. Статус книги: Свободна."
    session.close()
    return "Ошибка! Не удалось вернуть книгу. Возможно книги с таким штрихкодом нет в библиотеке."


# Реализация поиска книг по названию
def search_books_by_name(name):
    session = Session()
    books = session.query(Book).where(Book.book_name_to_search.like(f'%{name.lower()}%')).all()
    session.close()
    return books


# Реализация поиска книг по автору
def search_books_by_author(author):
    session = Session()
    books = session.query(Book).where(Book.book_author_to_search.like(f'%{author.lower()}%')).all()
    session.close()
    return books


# Функция, использующаяся для записи сообщений, отправленных администратором, в соответствующую таблицу
def send_message(message):
    session = Session()
    users = session.query(Users).all()

    for user in users:
        if user.login != 'Admin':
            broadcast_message = BroadcastMessages(message=message, user_id=user.id, is_show=False)
            session.add(broadcast_message)

    session.commit()
    session.close()


# Используется для вывода сообщений от администратора на форму профиля пользователя
def return_broadcast_message(user_login):
    session = Session()
    user = search_user(session, user_login)
    messages = get_messages(session, user.id)
    session.commit()
    session.close()
    return messages


# Вспомогательная функция для вывода сообщений: собирает список всех непросмотренных сообщений
def get_messages(session, user_id):
    messages = session.query(BroadcastMessages).where(BroadcastMessages.user_id == user_id,
                                                      BroadcastMessages.is_show == False).all()
    return_messages = []
    for mes in messages:
        return_messages.append(mes.message)
        session.add(mes)
        session.delete(mes)

    return return_messages
