from Iterable.iterable import MyIterable


class BookRepository:
    def __init__(self, books=None):
        self.__book_list = MyIterable()
        if books is not None:
            self.add_all(books)

    @property
    def book_list(self):
        return self.__book_list

    def add_all(self, books):
        for book in books:
            self.book_list.append(book)

    def add(self, book):
        """
        Adds a new book to the list
        :param book:
        :return:
        """
        self.book_list.append(book)

    def remove(self, id_):
        """
        Removes a book using its id
        :param id_:
        :return:
        """
        i = 0
        while i != len(self.book_list):
            if int(self.book_list[i].book_id) == int(id_):
                save = self.book_list[i]
                self.book_list.pop(i)
                return save
            else:
                i += 1

    def update(self, id_, title, author):
        """
        Updates the list of books using a given id with the new title and author
        :param id_:
        :param title:
        :param author:
        :return:
        """
        for book in self.book_list:
            if int(book.book_id) == int(id_):
                save = book
                book.title = title
                book.author = author
                return save

    def search(self, item):
        """
        Search for books. The search must work using case-insensitive, partial string matching, and must return all
        matching items.
        :param item:
        :return:
        """
        list_ = []
        for book in self.book_list:
            if item in str(book.author).lower() or item in str(book.title).lower() or item in str(book.book_id):
                list_.append(book)
        return list_
