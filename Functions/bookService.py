from Domain.bookStock import Book, BookException
import random
from Functions.undoService import *
from Iterable.iterable import MyIterable


class BookService:
    def __init__(self, book_repo, book_validator, undo_service, rental_srv):
        self.__repo = book_repo
        self._val = book_validator
        self._rental_srv = rental_srv
        self._undo_service = undo_service

    @property
    def repo(self):
        return self.__repo

    def add(self, book, record_undo=True):
        """
        adds a new book if valid
        :param book:
        :param record_undo:
        :return:
        """
        self._val.validate(book)
        if self.check_unique_id(book.book_id):
            self.repo.add(book)
        else:
            raise BookException("Book already in list!")
        if record_undo:
            undo = FunctionCall(self.remove, book.book_id, False)
            redo = FunctionCall(self.add, book, False)
            self._undo_service.record(Operation(undo, redo))

    def remove(self, book_id, record_undo=True):
        """
        Removes a book and its rentals
        :param book_id:
        :return:
        """
        if self.check_unique_id(book_id):
           raise BookException("Book not in list to remove!")
        book = self.repo.remove(book_id)

        # delete rentals with book_id
        ls = MyIterable.filter(self._rental_srv.repo.rental_list, lambda x: x.book_id == book_id)

        for elem in ls:
            self._rental_srv.repo.remove(elem.rental_id)

        # Record for cascaded undo/redo
        if record_undo:

            undo = FunctionCall(self.add, book, False)
            redo = FunctionCall(self.remove, book.book_id, False)
            op = Operation(undo, redo)

            cascade_list = [op]
            for rent in ls:
                undo = FunctionCall(self._rental_srv.rent, rent, False)
                #redo = FunctionCall(self._rental_srv.repo.remove, rent.rental_id)
                cascade_list.append(Operation(undo, None))

            cop = CascadedOperation(*cascade_list)
            self._undo_service.record(cop)

    def update(self, id_, title, author, record_undo=True):
        """
        Updates the data for a given id of a book
        :param id_:
        :param title:
        :param author:
        :return:
        """
        if not self.check_unique_id(id_):
            original_book = self.repo.update(id_, title, author)
        else:
            raise BookException("Book id not in list to update!")

        if record_undo:
            undo = FunctionCall(self.update, original_book.book_id, original_book.title, original_book.author, False)
            redo = FunctionCall(self.update, id_, title, author, False)
            self._undo_service.record(Operation(undo, redo))

    def search(self, item):
        """
        This function calls the repo search function and returns a list of partial matching strings
        :param item:
        :return:
        """
        return self.repo.search(item)

    def check_unique_id(self, id_):
        unique = True
        for book in self.repo.book_list:
            if int(book.book_id) == int(id_):
                unique = False
        return unique

    def generate_books(self):
        list1 = ['Harap Alb', 'Iona', 'Ion', 'Luceafarul', 'Moara cu Noroc', 'Riga Cypto', 'O scrisoare pierduta',
                 'Baltagul', 'Floare Albastra', 'Testament']
        list2 = ['Creanga', 'Marin Sorescu', 'Rebreanu', 'Eminescu', 'Slavici', 'Ion Barbu', 'I.L.Caragiale',
                 'Sadoveanu',
                 'Eminescu', 'Arghezi']
        for i in range(10):
            book_id = random.randrange(1, 11)
            while not self.check_unique_id(book_id):
                book_id = random.randrange(1, 11)

            nr = random.randrange(10)
            book_title = list1[nr]
            book_author = list2[nr]

            self.repo.book_list.append(Book(book_id, book_title, book_author))
