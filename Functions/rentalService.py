import random
from datetime import date, timedelta
from Repository.rentalRepository import RentalException
from Domain.rentalStock import Rental
from Functions.undoService import *
from Iterable.iterable import MyIterable


class RentalService:
    def __init__(self, rental_repo, book_repo, client_repo, rental_validator, undo):
        self.__repo = rental_repo
        self._val = rental_validator
        self.__book_repo = book_repo
        self.__client_repo = client_repo
        self._undo_service = undo

    @property
    def repo(self):
        return self.__repo

    @property
    def book_repo(self):
        return self.__book_repo

    @property
    def client_repo(self):
        return self.__client_repo

    def check_client_existence(self, client_id):
        """
        Checks if the client already exists by its given id
        :param client_id:
        :return:
        """
        found = False
        for client in self.client_repo.client_list:
            if int(client_id) == int(client.client_id):
                found = True
        return found

    def check_book_existence(self, book_id):
        found = False
        for book in self.book_repo.book_list:
            if int(book_id) == int(book.book_id):
                found = True
        return found

    def check_rental_existence(self, rental_id):
        # check rental_id is unique
        found = False
        for elem in self.repo.rental_list:
            if int(rental_id) == int(elem.rental_id):
                found = True
        return found

    def check_rental_availability(self, book_id, start_date, end_date):
        available = True
        for rents in self.repo.rental_list:
            if int(rents.book_id) == int(book_id):
                if rents.returned_date == None:
                    available = False
                elif end_date == None and rents.returned_date > start_date:
                    available = False
                elif rents.returned_date > start_date and rents.rented_date < end_date:
                    available = False
        return available

    def rent(self, rental, record_undo=True):
        """
        if rental is valid(book exists,client exists,rental id is unique, rental is available) appends
        :param rental:
        :return:
        """
        self._val.validate(rental)

        # check if client existent
        if not self.check_client_existence(rental.client_id):
            raise RentalException("client id not existent")

        # check if book exists
        if not self.check_book_existence(rental.book_id):
            raise RentalException("book id not existent")

        # check rental_id is unique
        if self.check_rental_existence(rental.rental_id):
            raise RentalException("Rental id already in list!")

        # check if rental available
        if self.check_rental_availability(rental.book_id, rental.rented_date, rental.returned_date):
            self.repo.add(rental)
        else:
            raise RentalException("Rental not available!")

        if record_undo:
            undo = FunctionCall(self.repo.remove, rental.rental_id)
            redo = FunctionCall(self.repo.add, rental, False)
            self._undo_service.record(Operation(undo, redo))

    def set_returned_date_to_none(self, rental):
        rental.returned_date = None

    def returned(self, rental_id, record_undo=True):
        """
        sets the returned date
        :param rental_id:
        :return:
        """
        rental = self.repo.return_book(rental_id)

        if record_undo:
            undo = FunctionCall(self.set_returned_date_to_none, rental)
            redo = FunctionCall(self.returned, rental_id, False)
            self._undo_service.record(Operation(undo, redo))

    def count_book_rental(self, book_id):
        """
        This function will count the nr of times a book was rented
        :return: the nr of times the book was rented
        """
        s = 0
        for book in self.repo.rental_list:
            if int(book_id) == int(book.book_id):
                s = s + 1
        return s

    def rented_books(self):
        list_ = []
        for book in self.book_repo.book_list:
            list_.append(rented_book(book.book_id, book.title, self.count_book_rental(book.book_id)))
        MyIterable.sort(list_, lambda elem1, elem2: elem1.rentals > elem2.rentals)
        return list_

    def count_client_rental(self, client_id):
        """
        This function will count the number of book rental days a given client has.
        :param client_id:
        :return:
        """
        day = 0
        for rental in self.repo.rental_list:
            if int(rental.client_id) == int(client_id):
                if rental.returned_date == None:
                    day = day + (date.today() - rental.rented_date).days
                else:
                    day = day + (rental.returned_date - rental.rented_date).days
        return day

    def active_clients(self):
        list_ = []
        for client in self.client_repo.client_list:
            list_.append(active_client(client.name, client.client_id,
                                       self.count_client_rental(client.client_id)))
        MyIterable.sort(list_, lambda elem1, elem2: elem1.days > elem2.days)
        return list_

    def find_author(self, book_id):
        for book in self.book_repo.book_list:
            if int(book_id) == int(book.book_id):
                return book.author

    def count_author_rentals(self, book_id):
        """
        This function will count the number of rentals a given author has
        :param author:
        :return:
        """
        s = 0
        author = self.find_author(book_id)
        for rental in self.repo.rental_list:
            if self.find_author(rental.book_id) == author:
                s = s + 1
        return s

    def check_if_author_in_list(self, list, name):
        for elem in list:
            if elem.name == name:
                return True
        return False

    def rented_author(self):
        list_ = []
        for book in self.book_repo.book_list:
            if self.check_if_author_in_list(list_,book.author) is False:
                list_.append(rented_author(book.author, self.count_author_rentals(book.book_id)))
        MyIterable.sort(list_, lambda elem1, elem2: elem1.rentals > elem2.rentals)
        return list_

    @staticmethod
    def generate_random_date():
        return date(random.randrange(2000, 2020), random.randrange(1, 13), random.randrange(1, 29))

    def generate_rentals(self):
        for i in range(10):
            id_ = random.randrange(1, 11)
            while self.check_rental_existence(id_):
                id_ = random.randrange(1, 11)

            client_id = random.randrange(1, 11)
            while not self.check_client_existence(client_id):
                client_id = random.randrange(1, 11)

            book_id = random.randrange(1, 11)
            while not self.check_book_existence(book_id):
                book_id = random.randrange(1, 11)

            start_date = self.generate_random_date()
            end_date = start_date + timedelta(days=random.randrange(1, 11))
            while not self.check_rental_availability(book_id, start_date, end_date):
                start_date = self.generate_random_date()
                end_date = start_date + timedelta(days=random.randrange(1, 11))

            self.repo.rental_list.append(Rental(id_, book_id, client_id, start_date, end_date))


class active_client:
    def __init__(self, name, id_, days):
        self._id = id_
        self._name = name
        self._days = days

    @property
    def name(self):
        return self._name

    @property
    def days(self):
        return self._days

    @property
    def id(self):
        return self._id

    def __str__(self):
        return str(self.id).ljust(3) + ": " + str(self.name).ljust(10) + " has " + str(self.days).ljust(
            3) + " rental days"


class rented_author:
    def __init__(self, name, rentals):
        self._name = name
        self._rentals = rentals

    @property
    def name(self):
        return self._name

    @property
    def rentals(self):
        return self._rentals

    def __str__(self):
        return str(self.name).ljust(15) + " has the nr of rentals= " + str(self.rentals)


class rented_book:
    def __init__(self, id, name, rentals):
        self._id = id
        self._name = name
        self._rentals = rentals

    @property
    def name(self):
        return self._name

    @property
    def rentals(self):
        return self._rentals

    def __str__(self):
        return str(self._id).ljust(3) + str(self.name).ljust(25) + " was rented: " + str(self.rentals).ljust(
            2) + " times"
