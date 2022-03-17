from Domain.clientStock import Client
from Iterable.iterable import MyIterable


class ClientRepository:
    def __init__(self, clients=None):
        self.__client_list = MyIterable()
        if clients is not None:
            self.add_all(clients)

    @property
    def client_list(self):
        return self.__client_list

    def add_all(self, clients):
        for client in clients:
            self.client_list.append(client)

    def add(self, client):
        """
        Adds a new client to the list
        :param client:
        :return:
        """
        self.client_list.append(client)

    def remove(self, client_id):
        """
        removes the given client
        :param client_id:
        :return:
        """
        i = 0
        while i != len(self.client_list):
            if int(self.client_list[i].client_id) == int(client_id):
                save = self.client_list[i]
                self.client_list.pop(i)
                return save
            else:
                i = i + 1

    def update(self, id_, name):
        """
        Updates the name of the client with the given id
        :param id_:
        :param name: new name
        :return:
        """
        for client in self.client_list:
            if int(client.client_id) == int(id_):
                save = client
                client.name = name
                return save

    def search(self, item):
        """
        Search for books. The search must work using case-insensitive, partial string matching, and must return all matching items.
        :param item:
        :return:
        """
        list_ = []
        for client in self.client_list:
            if item in str(client.name).lower() or item in str(client.client_id):
                list_.append(client)
        return list_
