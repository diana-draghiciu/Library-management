class Settings:
    def __init__(self, file_name):
        self.file_name = file_name
        self._load()

    def _load(self):
        with open(self.file_name, "rt") as f:
            self._repo_type = self.get_option(f).strip("\' ")
            self._book_repo = self.get_option(f).strip("\' ")
            self._client_repo = self.get_option(f).strip("\' ")
            self._rental_repo = self.get_option(f).strip("\' ")
            self._ui_type = self.get_option(f).strip("\' ")

    @property
    def client_repo(self):
        return self._client_repo

    @property
    def book_repo(self):
        return self._book_repo

    @property
    def rental_repo(self):
        return self._rental_repo

    @property
    def repo_type(self):
        return self._repo_type

    @property
    def ui_type(self):
        return self._ui_type

    @staticmethod
    def get_option(file):
        option = file.readline()
        option = option.split("=")
        return option[1].rstrip("\n")
