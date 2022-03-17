import pickle
from Repository.clientRepository import ClientRepository
from Repository.bookRepository import BookRepository
from Repository.rentalRepository import RentalRepository


class ClientBinaryFileRepository(ClientRepository):
    def __init__(self, file_name='client.bin'):
        super().__init__()
        self._file_name = file_name
        self._load()

    def add(self, item):
        super().add(item)
        self._save()

    def remove(self, id_):
        client = super().remove(id_)
        self._save()
        return client

    def update(self, id_, name):
        client = super().update(id_, name)
        self._save()
        return client

    def _save(self):
        f = open(self._file_name, 'wb')
        pickle.dump(self.client_list, f)
        f.close()

    def _load(self):
        f = open(self._file_name, 'rb')  # read text
        client_list = pickle.load(f)
        self.add_all(client_list)
        f.close()


class BookBinaryFileRepository(BookRepository):
    def __init__(self, file_name='book.bin'):
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
        f = open(self._file_name, 'wb')
        pickle.dump(self.book_list, f)
        f.close()

    def _load(self):
        f = open(self._file_name, 'rb')  # read text
        book_list = pickle.load(f)
        self.add_all(book_list)
        f.close()


class RentalBinaryFileRepository(RentalRepository):
    def __init__(self, file_name='rental.bin'):
        super().__init__()
        self._file_name = file_name
        self._load()

    def add(self, item):
        super().add(item)
        self._save()

    def return_book(self, id_):
        rental = super().return_book(id_)
        self._save()
        return rental

    def _save(self):
        f = open(self._file_name, 'wb')
        pickle.dump(self.rental_list, f)
        f.close()

    def _load(self):
        f = open(self._file_name, 'rb')  # read text
        rental_list = pickle.load(f)
        self.add_all(rental_list)
        f.close()
