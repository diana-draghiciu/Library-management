class BookException(Exception):
    def __init__(self, msg=''):
        self._msg = msg

    def __str__(self):
        return self._msg


class BookValidationException(BookException):
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


class Book:
    def __init__(self, id_, title, author):
        self.__book_id = id_
        self.__title = title
        self.__author = author

    @property
    def book_id(self):
        return self.__book_id

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, author):
        self.__author = author

    def __str__(self):
        return str(self.book_id).rjust(2) + ": " + str(self.title).ljust(20) + " by " + self.author


class BookValidator:
    def validate(self, book):
        errors = []
        try:
            int(book.book_id)
        except ValueError:
            errors.append('Invalid id input.')
        if str(book.book_id) == '0':
            errors.append("Invalid book id, empty value provided")
        if book.title == '0':
            errors.append("Invalid book title, empty value provided")
        if book.author == '0':
            errors.append("Invalid author, empty value provided")
        if len(errors) != 0:
            raise BookValidationException(errors)
