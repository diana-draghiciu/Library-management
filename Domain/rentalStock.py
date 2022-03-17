from datetime import date


class RentalException(Exception):
    def __init__(self, msg=''):
        self._msg = msg

    def __str__(self):
        return self._msg


class RentalValidationException(RentalException):
    def __init__(self, error_list):
        self._errors = error_list

    @property
    def errors(self):
        # Gives access to the list of errors
        return self._errors

    def __str__(self):
        # str representation
        result = ''
        for e in self.errors:
            result += e
            result += '\n'
        return result


class Rental:
    def __init__(self, rental_id, book_id, client_id, rented_date=date.today(), returned_date=None):
        self.__rental_id = rental_id
        self.__book_id = book_id
        self.__client_id = client_id
        self.__rented_date = rented_date
        self.__returned_date = returned_date

    @property
    def rental_id(self):
        return self.__rental_id

    @property
    def book_id(self):
        return self.__book_id

    @property
    def client_id(self):
        return self.__client_id

    @property
    def rented_date(self):
        return self.__rented_date

    @property
    def returned_date(self):
        return self.__returned_date

    @returned_date.setter
    def returned_date(self, date):
        self.__returned_date = date

    def __str__(self):
        return str(self.rental_id).rjust(2) + ": book_id-" + str(self.book_id).rjust(2) + ", client_id-" + str(
            self.client_id).rjust(2) + " (" + str(
            self.rented_date) + ") - (" + str(self.returned_date) + ")"


class RentalValidator:
    def validate(self, rental):
        # rental_id, book_id, client_id, rented_date, returned_date
        errors = []
        try:
            int(rental.rental_id)
        except ValueError:
            errors.append('Invalid rental id input.')
        if str(rental.rental_id) == '0':
            errors.append("Invalid rental id, empty value provided")
        try:
            int(rental.book_id)
        except ValueError:
            errors.append('Invalid book id input.')
        if str(rental.book_id) == '0':
            errors.append("Invalid book id, empty value provided")
        try:
            int(rental.client_id)
        except ValueError:
            errors.append('Invalid client id input.')
        if str(rental.client_id) == '0':
            errors.append("Invalid client id, empty value provided")

        if rental.rented_date == date(1, 1, 1):
            errors.append("Invalid start date, default value provided (1, 1, 1)")
        if rental.returned_date == date(1, 1, 1):
            errors.append("Invalid end date, default value provided (1, 1, 1)")

        if rental.returned_date != None:
            if rental.rented_date > rental.returned_date:
                errors.append("The rental date is bigger than the returned date")

        if len(errors) != 0:
            raise RentalValidationException(errors)
