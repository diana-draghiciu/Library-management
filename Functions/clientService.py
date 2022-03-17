import random
from Domain.clientStock import Client, ClientException
from Iterable.iterable import MyIterable
from Functions.undoService import *


class ClientService:
    def __init__(self, client_repo, client_validator, undo_service, rental_srv):
        self.__repo = client_repo
        self._val = client_validator
        self._rental_srv = rental_srv
        self._undo_service = undo_service

    @property
    def repo(self):
        return self.__repo

    def add(self, client, record_undo=True):
        """
        Adds if valid a new client
        :param client:
        :return:
        """
        self._val.validate(client)
        if self.check_unique_clients(client.client_id):
            self.repo.add(client)
        else:
            raise ClientException("Client id already in list!")

        if record_undo:
            undo = FunctionCall(self.remove, client.client_id, False)
            redo = FunctionCall(self.add, client, False)
            self._undo_service.record(Operation(undo, redo))

    def remove(self, id_, record_undo=True):
        """
        Removes a client using its id
        :param id_:
        :return:
        """

        if self.check_unique_clients(id_):
            raise ClientException("Client not in list to remove!")
        client = self.repo.remove(id_)

        # delete rentals with the same client_id
        ls = MyIterable.filter(self._rental_srv.repo.rental_list, lambda x: x.client_id == id_)
        for elem in ls:
            self._rental_srv.repo.remove(elem.rental_id)

        if record_undo:
            undo = FunctionCall(self.add, client, False)
            redo = FunctionCall(self.remove, client.client_id, False)
            op = Operation(undo, redo)

            # Record for cascaded undo/redo
            cascade_list = [op]
            for rent in ls: #todo change from rent to add for the sql to work
                undo = FunctionCall(self._rental_srv.rent, rent, False)
                cascade_list.append(Operation(undo, None))

            cop = CascadedOperation(*cascade_list)
            self._undo_service.record(cop)

    def update(self, id_, name, record_undo=True):
        """
        updates a client's name
        :param id_:
        :param name:
        :return:
        """
        if self.check_unique_clients(id_):
            raise ClientException("Client not in list to update!")
        original_client = self.repo.update(id_, name)

        if record_undo:
            undo = FunctionCall(self.update, id_, original_client.name, False)
            redo = FunctionCall(self.update, id_, name, False)
            self._undo_service.record(Operation(undo, redo))

    def search(self, item):
        """
        Returns a list of objects corresponding to the searched item
        :param item: the searched string
        :return: the list
        """
        return self.repo.search(item)

    def check_unique_clients(self, id_):
        unique = True
        for client in self.repo.client_list:
            if int(client.client_id) == int(id_):
                unique = False
        return unique

    def generate_clients(self):
        for i in range(10):
            client_id = random.randrange(1, 11)
            while not self.check_unique_clients(client_id):
                client_id = random.randrange(1, 11)

            names = ['Ana', 'Maria', 'Pop', 'Ion', 'Vasile', 'George', 'Cristina', 'Elena', 'David', 'Paul']
            client_name = random.choice(names)

            self.repo.client_list.append(Client(client_id, client_name))
