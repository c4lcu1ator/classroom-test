import sqlite3

def createdb(cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS books (
                    book_id INTEGER,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    year INTEGER,
                    available INTEGER DEFAULT 1)""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS readers (
                    reader_id INTEGER,
                    name TEXT NOT NULL,
                    phone INTEGER,
                    book_id INTEGER)""")


def addbook(cursor, title, author, year):
    cursor.execute("INSERT INTO books(title, author, year) VALUES(?,?,?)",
                   (title, author, year))


def addreader(cursor, name, phone):
    cursor.execute("INSERT INTO readers(name, phone) VALUES(?,?)",
                   (name, phone))


def givebook(cursor, reader_id, book_id):
    cursor.execute("UPDATE books SET available = 0 WHERE book_id = ?", (book_id,))
    cursor.execute("UPDATE readers SET book_id = ? WHERE reader_id = ?",
                   (book_id, reader_id))


def vozvrat(cursor, book_id):
    cursor.execute("UPDATE books SET available = 1 WHERE book_id = ?", (book_id,))
    cursor.execute("UPDATE readers SET book_id = NULL WHERE book_id = ?", (book_id,))


def books(cursor):
    cursor.execute("SELECT * FROM books WHERE available = 1")
    return cursor.fetchall()


def reader(cursor, reader_id):
    cursor.execute("SELECT book_id FROM readers WHERE reader_id = ?", (reader_id,))
    return cursor.fetchall()


# def search_books(cursor, keyword):
#     cursor.execute


if __name__ == '__main__':
    with sqlite3.connect('library.db') as conn:
        cur = conn.cursor()

        createdb(cur)

        addbook(cur, "Дюна", "Фрэнк Герберт", 1965)
        addbook(cur, "Собор Парижской Богоматери", "Виктор Гюго", 1831)
        addbook(cur, "Маленький принц", "Антуан де Сент-Экзюпери", 1943)

        addreader(cur, "Иван Якимов", "+79294360020")
        addreader(cur, "Максим Курганский", "+79021701315")

        givebook(cur, 1, 1)

        print("Доступные книги после выдачи:")
        print(books(cur))

        vozvrat(cur, 1)

        print("\nДоступные книги после возврата:")
        print(books(cur))