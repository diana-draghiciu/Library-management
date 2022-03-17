from Domain.rentalStock import Rental
from Repository.bookRepository import BookRepository
from Repository.clientRepository import ClientRepository
from Repository.rentalRepository import RentalRepository
from Domain.bookStock import Book
from Domain.clientStock import Client
from datetime import date


class BookTextFileRepository(BookRepository):
    def __init__(self, file_name='ingredients.txt'):
        super().__init__()
        self._file_name = file_name
        self._load()

    def add(self, item):
        super().add(item)
        self._save()

    def remove(self, id_):
        book=super().remove(id_)
        self._save()
        return book

    def update(self, id_, title, author):
        book=super().update(id_, title,author)
        self._save()
        return book

    def _save(self):
        f = open(self._file_name, 'wt')
        for book in self.book_list:
            line = str(book.book_id) + ';' + book.title + ';' + book.author
            f.write(line)
            f.write('\n')
        f.close()

    def _load(self):
        """
        Load data from file
        We assume file-saved data is valid
        """
        f = open(self._file_name, 'rt')  # read text
        lines = f.readlines()
        f.close()

        for line in lines:
            line = line.split(';')
            super().add(Book(int(line[0]), line[1], line[2].strip('\n')))


class ClientTextFileRepository(ClientRepository):
    def __init__(self, file_name='client.txt'):
        super().__init__()
        self._file_name = file_name
        self._load()

    @property
    def file_name(self):
        return self._file_name

    def add(self, item):
        super().add(item)
        self._save()

    def remove(self, id_):
        client=super().remove(id_)
        self._save()
        return client

    def update(self, id_, name):
        client=super().update(id_,name)
        self._save()
        return client

    def _save(self):
        f = open(self.file_name, 'wt')
        for client in self.client_list:
            line = str(client.client_id) + ';' + client.name
            f.write(line+'\n')
        f.close()

    def _load(self):
        """
        Load data from file
        We assume file-saved data is valid
        """
        f = open(self.file_name, 'rt')  # read text
        lines = f.readlines()
        f.close()

        for line in lines:
            line = line.split(';')
            super().add(Client(int(line[0]), line[1].strip('\n')))


class RentalTextFileRepository(RentalRepository):
    def __init__(self, file_name='rental.txt'):
        super().__init__()
        self._file_name = file_name
        self._load()

    def add(self, item):
        super().add(item)
        self._save()

    def return_book(self, id_):
        rental=super().return_book(id_)
        self._save()
        return rental

    def _save(self):
        f = open(self._file_name, 'wt')
        for rental in self.rental_list.values():
            if rental.returned_date is not None:
                line = str(rental.rental_id) + ';' + str(rental.book_id) + ';' + str(rental.client_id) + ';' + str(
                            rental.rented_date) + ';' + str(rental.returned_date)
            else:
                line = str(rental.rental_id) + ';' + str(rental.book_id) + ';' + str(rental.client_id) + ';' + str(
                    rental.rented_date)
            f.write(line+'\n')
        f.close()

    def _load(self):
        """
        Load data from file
        We assume file-saved data is valid
        """
        f = open(self._file_name, 'rt')  # read text
        lines = f.readlines()
        f.close()

        for line in lines:
            line = line.split(';')
            start_date = line[3].strip().split('-')
            if len(line) == 5:
                end_date = line[4].strip().split('-')
                super().add(Rental(int(line[0]), int(line[1]), int(line[2]), date(int(start_date[0]),int(start_date[1]),int(start_date[2])),date(int(end_date[0]),int(end_date[1]),int(end_date[2]))))
            else:
                super().add(Rental(int(line[0]), int(line[1]), int(line[2]),
                                   date(int(start_date[0]), int(start_date[1]), int(start_date[2]))))
