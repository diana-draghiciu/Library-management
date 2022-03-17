import json
from datetime import date

from Domain.bookStock import Book
from Domain.rentalStock import Rental
from Repository.clientRepository import ClientRepository
from Repository.bookRepository import BookRepository
from Repository.rentalRepository import RentalRepository
from Domain.clientStock import Client


class ClientJsonFileRepository(ClientRepository):
    def __init__(self, file_name):
        super().__init__()
        self._file_name = file_name
        self._load()

    def add(self, item):
        super().add(item)
        self.save()

    def remove(self, id_):
        client = super().remove(id_)
        self.save()
        return client

    def update(self, id_, name):
        client = super().update(id_, name)
        self.save()
        return client

    def _load(self):
        f = open(self._file_name, 'r')
        dict_ = json.load(f)
        for elem in dict_["list"]:
            self.client_list.append(Client(elem['id'], elem['name']))
        f.close()

    def save(self):
        f = open(self._file_name, 'w')

        dict = {}
        dict_aux = {}
        dict["list"] = []
        for client in self.client_list:
            dict_aux["id"] = client.client_id
            dict_aux["name"] = client.name
            dict["list"].append(dict_aux.copy())

        json.dump(dict, f, indent=4)
        f.close()


class BookJsonFileRepository(BookRepository):
    def __init__(self, file_name):
        super().__init__()
        self._file_name = file_name
        self._load()

    def add(self, item):
        super().add(item)
        self.save()

    def remove(self, id_):
        book = super().remove(id_)
        self.save()
        return book

    def update(self, id_, title, author):
        client = super().update(id_, title, author)
        self.save()
        return client

    def _load(self):
        f = open(self._file_name, 'r')
        dict_ = json.load(f)
        for elem in dict_["list"]:
            self.book_list.append(Book(elem['id'], elem["title"], elem["author"]))
        f.close()

    def save(self):
        f = open(self._file_name, 'w')

        dict = {}
        dict_aux = {}
        dict["list"] = []
        for book in self.book_list:
            dict_aux["id"] = book.book_id
            dict_aux["title"] = book.title
            dict_aux["author"] = book.author
            dict["list"].append(dict_aux.copy())

        json.dump(dict, f, indent=4)
        f.close()


class RentalJsonFileRepository(RentalRepository):
    def __init__(self, file_name):
        super().__init__()
        self._file_name = file_name
        self._load()

    def add(self, item):
        super().add(item)
        self.save()

    def return_book(self, id_):
        rental = super().return_book(id_)
        self.save()
        return rental

    def _load(self):
        f = open(self._file_name, 'r')
        dict_ = json.load(f)
        for elem in dict_["list"]:
            start_date = elem["rent_date"].split("-")
            if elem["return_date"] != "None":
                end_date = elem["return_date"].split("-")
                rental = Rental(elem['id'], elem["book_id"], elem["client_id"],
                                date(int(start_date[0]), int(start_date[1]), int(start_date[2])),
                                date(int(end_date[0]), int(end_date[1]), int(end_date[2])))
            else:
                rental = Rental(elem['id'], elem["book_id"], elem["client_id"],
                                date(int(start_date[0]), int(start_date[1]), int(start_date[2])))
            self.rental_list[rental.rental_id] = rental
        f.close()

    def save(self):
        f = open(self._file_name, 'w')

        dict = {}
        dict_aux = {}
        dict["list"] = []
        for rental in self.rental_list.values():
            dict_aux["id"] = rental.rental_id
            dict_aux["book_id"] = rental.book_id
            dict_aux["client_id"] = rental.client_id
            dict_aux["rent_date"] = str(rental.rented_date)
            dict_aux["return_date"] = str(rental.returned_date)
            dict["list"].append(dict_aux.copy())

        json.dump(dict, f, indent=4)
        f.close()
