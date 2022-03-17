class ClientException(Exception):
    def __init__(self, msg=''):
        self._msg = msg

    def __str__(self):
        return self._msg


class ClientValidationException(ClientException):
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


class Client:
    def __init__(self, client_id, name):
        self.__client_id = client_id
        self.__name = name

    @property
    def client_id(self):
        return self.__client_id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    def __str__(self):
        return str(self.client_id).rjust(2) + ": " + self.name


class ClientValidator:
    def validate(self, client):
        """
        Validate a given client
        """
        errors = []

        if str(client.name) == '0':
            errors.append('Invalid name, empty value provided.')
        try:
            int(client.client_id)
        except ValueError:
            errors.append('Invalid id input.')
        if str(client.client_id) == '0':
            errors.append('Invalid id, empty value provided.')
        if len(errors) != 0:
            raise ClientValidationException(errors)
