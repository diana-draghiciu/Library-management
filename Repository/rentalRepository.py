from Domain.rentalStock import RentalException
from datetime import date
from Iterable.iterable import MyIterable


class RentalRepository:
    def __init__(self, rentals=None):
        self.__rental_list = MyIterable()
        if rentals is not None:
            self.add_all(rentals)

    @property
    def rental_list(self):
        return self.__rental_list

    def add_all(self, rentals):
        for rental in rentals:
            self.rental_list.append(rental)

    def add(self, rental):
        """
        adds a new rental to the rental dictionary with the rental_id as key
        :param rental:
        :return:
        """
        self.rental_list.append(rental)

    def find_elem(self, rental_id):
        for index in range(len(self.rental_list)):
            if self.rental_list[index].rental_id == rental_id:
                return index
        return -1

    def return_book(self, rental_id):
        """
        sets the returned date with today's date
        :param rental_id:
        :return:
        """
        index = self.find_elem(rental_id)
        if index != -1:
            if self.rental_list[index].returned_date is None:
                save = self.rental_list[index]
                self.rental_list[index].returned_date = date.today()
                return save
            else:
                raise RentalException("This book was already returned")

    def remove(self, rental_id):
        """
        Removes a rental from the list
        :param rental_id:
        :return:
        """
        for i in range(len(self.rental_list)):
            if self.rental_list[i].rental_id == rental_id:
                self.rental_list.pop(i)
                return
