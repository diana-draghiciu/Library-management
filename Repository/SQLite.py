import sqlite3
from datetime import date, datetime

from Domain.bookStock import Book
from Domain.clientStock import Client
from Domain.rentalStock import Rental
from Repository.bookRepository import BookRepository
from Repository.clientRepository import ClientRepository
from Repository.rentalRepository import RentalRepository


class RentalDataBaseRepo(RentalRepository):
    def __init__(self, file_name):
        super().__init__()
        self.__file_name = file_name
        self.__load()

    def add(self, elem):
        super().add(elem)
        con = sqlite3.connect(self.__file_name)
        cursorObj = con.cursor()
        entities = (elem.rental_id, elem.book_id, elem.client_id, str(elem.rented_date), str(elem.returned_date))
        cursorObj.execute(
            'INSERT INTO rentals(id, book_id, client_id, rent_date, return_date) VALUES(?, ?, ?,?,?)', entities)
        con.commit()
        con.close()

    def return_book(self, id_):
        super().return_book(id_)
        con = sqlite3.connect(self.__file_name)
        cursorObj = con.cursor()
        cursorObj.execute('UPDATE rentals SET return_date = ? where id = ?', (str(date.today()), id_))
        con.commit()
        con.close()

    def remove(self, rental_id):
        super().remove(rental_id)
        con = sqlite3.connect(self.__file_name)
        cursorObj = con.cursor()
        cursorObj.execute('DELETE FROM rentals WHERE id = ?', (rental_id,))
        con.commit()
        con.close()

    def __load(self):
        con = sqlite3.connect(self.__file_name)
        cursorObj = con.cursor()
        for elem in cursorObj.execute('SELECT * FROM rentals'):
            rent_date = datetime.strptime(elem[3], "%Y-%m-%d").date()
            if elem[4] == "None":
                returned_date = None
            else:
                returned_date = datetime.strptime(elem[4], "%Y-%m-%d").date()
            super().add(Rental(elem[0], elem[1], elem[2], rent_date, returned_date))
        con.close()


class ClientDataBaseRepo(ClientRepository):
    def __init__(self, file_name):
        super().__init__()
        self.__file_name = file_name
        self.__load()

    def add(self, elem):
        super().add(elem)
        con = sqlite3.connect(self.__file_name)
        cursorObj = con.cursor()
        entities = (elem.client_id, elem.name)
        cursorObj.execute('INSERT INTO clients(id, name) VALUES(?, ?)', entities)
        con.commit()
        con.close()

    def update(self, id_, name):
        elem = super().update(id_, name)
        con = sqlite3.connect(self.__file_name)
        cursorObj = con.cursor()
        cursorObj.execute('UPDATE clients SET name = ? where id = ?', (name, id_))
        con.commit()
        con.close()
        return elem

    def remove(self, id_):
        elem = super().remove(id_)
        con = sqlite3.connect(self.__file_name)
        cursorObj = con.cursor()
        cursorObj.execute('DELETE FROM clients WHERE id = ?', (id_,))
        con.commit()
        con.close()
        return elem

    def __load(self):
        con = sqlite3.connect(self.__file_name)
        cursorObj = con.cursor()
        for elem in cursorObj.execute('SELECT * FROM clients'):
            super().add(Client(*elem))
        con.close()


class BookDataBaseRepo(BookRepository):
    def __init__(self, file_name):
        super().__init__()
        self.__file_name = file_name
        self.__load()

    def add(self, elem):
        super().add(elem)
        con = sqlite3.connect(self.__file_name)
        cursorObj = con.cursor()
        entities = (elem.book_id, elem.title, elem.author)
        cursorObj.execute('INSERT INTO books(id, title, author) VALUES(?, ?,?)', entities)
        con.commit()
        con.close()

    def update(self, id_, title, author):
        elem = super().update(id_, title, author)
        con = sqlite3.connect(self.__file_name)
        cursorObj = con.cursor()
        cursorObj.execute('UPDATE books SET title = ?, author = ? where id = ?', (title, author, id_))
        con.commit()
        con.close()
        return elem

    def remove(self, id_):
        elem = super().remove(id_)
        con = sqlite3.connect(self.__file_name)
        cursorObj = con.cursor()
        cursorObj.execute('DELETE FROM books WHERE id=?', (id_,))
        con.commit()
        con.close()
        return elem

    def __load(self):
        con = sqlite3.connect(self.__file_name)
        cursorObj = con.cursor()
        for elem in cursorObj.execute('SELECT * FROM books'):
            super().add(Book(*elem))
        con.close()
