from Domain.bookStock import Book
from Domain.clientStock import Client
from Domain.rentalStock import Rental
from datetime import date


class LibraryUI:
    def __init__(self, client_functions, book_functions, rental_functions, undo):
        self.__client_service = client_functions
        self.__book_service = book_functions
        self.__rental_service = rental_functions
        self.__undo_service=undo

    @property
    def client_service(self):
        return self.__client_service

    @property
    def book_service(self):
        return self.__book_service

    @property
    def rental_service(self):
        return self.__rental_service

    def add_ui(self, command_params):
        """
        Checks if parameters belong to a client object or book obj and adds them to the list
        :param command_params:
        :return:
        """
        tokens = command_params.split(" ")
        if len(tokens) == 2:
            self.client_service.add(Client(tokens[0], tokens[1]))
        elif len(tokens) == 3:
            self.book_service.add(Book(tokens[0], tokens[1], tokens[2]))
        else:
            raise ValueError("Invalid nr of parameters!")

    def rent_ui(self, command_params):
        """
        Checks if rent date introduced or return date and appends to the list with today date if rent date not introduced
        :param command_params:
        :return:
        """
        tokens = command_params.split(" ")
        if len(tokens) == 3:
            self.rental_service.rent(Rental(int(tokens[0]), int(tokens[1]), int(tokens[2])))
        elif len(tokens) == 4:
            start = tokens[3].split('-')
            self.rental_service.rent(
                Rental(int(tokens[0]), int(tokens[1]), int(tokens[2]), date(int(start[0]), int(start[1]), int(start[2]))))
        elif len(tokens) == 5:
            start = tokens[3].split('-')
            end = tokens[4].split('-')
            self.rental_service.rent(
                Rental(int(tokens[0]), int(tokens[1]), int(tokens[2]), date(int(start[0]), int(start[1]), int(start[2])),
                       date(int(end[0]), int(end[1]), int(end[2]))))
        else:
            raise ValueError("Invalid nr of parameters")

    def return_ui(self, command_params):
        """
        Modifies the returned date if previously not modified
        :param command_params:
        :return:
        """
        tokens = command_params.split(' ')
        if len(tokens) == 1:
            self.rental_service.returned(int(command_params))
        else:
            raise ValueError("Invalid nr of parameters")

    def remove_ui(self, command_params):
        """
        Removes a client or a book from the list
        :param command_params:
        :return:
        """
        tokens = command_params.split(' ')
        if tokens[0] == 'client':
            self.client_service.remove(int(tokens[1]))
        elif tokens[0] == 'book':
            self.book_service.remove(int(tokens[1]))
        else:
            raise ValueError("Invalid command for remove!")

    def update_ui(self, command_params):
        """
        updates a client or a book
        :param command_params:
        :return:
        """
        tokens = command_params.split(" ")
        if len(tokens) == 2:
            self.client_service.update(tokens[0], tokens[1])
        elif len(tokens) == 3:
            self.book_service.update(tokens[0], tokens[1], tokens[2])
        else:
            raise ValueError("Invalid nr of parameters!")

    def print_given_list(self, list_):
        for elem in list_:
            print(elem)

    def search(self, command_params):
        tokens = command_params.split(" ")
        if str(tokens[0]).lower() == 'book':
            list_ = self.book_service.search(str(tokens[1]).lower())
            if len(list_) == 0:
                raise Exception("No element found!")
            else:
                self.print_given_list(list_)
        elif str(tokens[0]).lower() == 'client':
            list_ = self.client_service.search(str(tokens[1]).lower())
            if len(list_) == 0:
                raise Exception("No element found!")
            else:
                self.print_given_list(list_)
        else:
            raise ValueError("Invalid command! Please input <search book ...> or <search client ...>")

    def statistic_ui(self, command_params):
        if str(command_params).lower() == "most rented author":
            list_=self.rental_service.rented_author()
            self.print_given_list(list_)
        elif str(command_params).lower() == "most active clients":
            list_=self.rental_service.active_clients()
            self.print_given_list(list_)
        elif str(command_params).lower() == "most rented books":
            list_ = self.rental_service.rented_books()
            self.print_given_list(list_)
        else:
            raise ValueError("statistic not found!")

    def list_ui(self, command_params):
        """
        Lists the clients/books/rentals
        :param command_params:
        :return:
        """
        if command_params == 'clients':
            list = sorted(self.client_service.repo.client_list, key=lambda client: int(client.client_id))
            self.print_given_list(list)
        elif command_params == 'books':
            list = sorted(self.book_service.repo.book_list, key=lambda book: int(book.book_id))
            self.print_given_list(list)
        elif command_params == 'rentals':
            list = sorted(self.rental_service.repo.rental_list, key=lambda rental: int(rental.rental_id))
            self.print_given_list(list)
        else:
            raise Exception("Such list not found!")

    def undo_ui(self, command=None):
        self.__undo_service.undo()

    def redo_ui(self, command=None):
        self.__undo_service.redo()

    @staticmethod
    def print_menu():
        print("You can:")
        print("add client(client_id, name) or book(book_id, title, author)")
        print("remove a client or book using its id")
        print("update client(client_id, name) or book(book_id, title, author)")
        print("search book/client")
        print('list clients/ list books/ list rentals')
        print("rent (rental_id, book_id, client_id)")
        print("return (rental_id)")
        print("statistic most rented books/ most active clients/ most rented author ")
        print("undo/redo an operation")
        print("exit")

    @staticmethod
    def split_command(command):
        """
        Separate user command into command word and parameters
        :param command: User command
        :return: (command word, command parameters=might be returned as None if not found)
        """
        tokens = command.strip().split(' ', 1)
        command_word = tokens[0].lower().strip()
        command_params = tokens[1].strip() if len(tokens) == 2 else ''

        return command_word, command_params

    def start(self):
        self.print_menu()
        command_dict = {"add": self.add_ui, "remove": self.remove_ui, "update": self.update_ui, "list": self.list_ui,
                        "rent": self.rent_ui, 'return': self.return_ui, 'search': self.search,
                        'statistic': self.statistic_ui, "undo": self.undo_ui, "redo": self.redo_ui}
        done = False
        while not done:
            command = input('command> ')
            command_word, command_params = self.split_command(command)

            if command_word in command_dict:
                try:
                    command_dict[command_word](command_params)
                except Exception as val_error:
                    print(str(val_error))
            elif command_word == 'exit':
                done = True
            else:
                print('No command found')
