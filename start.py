from Functions.bookService import BookService
from Functions.clientService import ClientService
from Functions.rentalService import RentalService
from Repository.SQLite import ClientDataBaseRepo, BookDataBaseRepo, RentalDataBaseRepo
from Repository.bookRepository import BookRepository
from Repository.rentalRepository import RentalRepository
from Repository.clientRepository import ClientRepository
from Repository.textRepository import ClientTextFileRepository, BookTextFileRepository, RentalTextFileRepository
from Repository.binaryRepository import ClientBinaryFileRepository, BookBinaryFileRepository, RentalBinaryFileRepository
from Repository.jsonRepository import ClientJsonFileRepository, BookJsonFileRepository, RentalJsonFileRepository
from Domain.bookStock import BookValidator
from Domain.clientStock import ClientValidator
from Domain.rentalStock import RentalValidator
from UI.console import LibraryUI
from Functions.undoService import UndoService
from commands import GUI
from Domain.Settings import Settings

if __name__ == '__main__':
    file_location = 'Files/'
    settings = Settings(file_location + "settings.properties")
    client_repo_location = file_location + settings.client_repo
    book_repo_location = file_location + settings.book_repo
    rental_repo_location = file_location + settings.rental_repo
    try:
        if settings.repo_type == 'inmemory':
            book_repo = BookRepository()
            client_repo = ClientRepository()
            rental_repo = RentalRepository()
        elif settings.repo_type == 'textfiles':
            client_repo = ClientTextFileRepository(client_repo_location)
            book_repo = BookTextFileRepository(book_repo_location)
            rental_repo = RentalTextFileRepository(rental_repo_location)
        elif settings.repo_type == 'binaryfiles':
            client_repo = ClientBinaryFileRepository(client_repo_location)
            book_repo = BookBinaryFileRepository(book_repo_location)
            rental_repo = RentalBinaryFileRepository(rental_repo_location)
        elif settings.repo_type == 'jsonfiles':
            client_repo = ClientJsonFileRepository(client_repo_location)
            book_repo = BookJsonFileRepository(book_repo_location)
            rental_repo = RentalJsonFileRepository(rental_repo_location)
        elif settings.repo_type == 'sqlfiles':
            client_repo = ClientDataBaseRepo(client_repo_location)
            book_repo = BookDataBaseRepo(book_repo_location)
            rental_repo = RentalDataBaseRepo(rental_repo_location)
        else:
            raise Exception("Invalid settings option!")

        book_val = BookValidator()
        client_val = ClientValidator()
        rental_val = RentalValidator()

        undo_srv = UndoService()
        rental_srv = RentalService(rental_repo, book_repo, client_repo, rental_val, undo_srv)
        book_srv = BookService(book_repo, book_val, undo_srv, rental_srv)
        client_srv = ClientService(client_repo, client_val, undo_srv, rental_srv)

        if settings.repo_type == 'inmemory':
            book_srv.generate_books()
            client_srv.generate_clients()
            rental_srv.generate_rentals()
        if settings.ui_type == "console":
            library = LibraryUI(client_srv, book_srv, rental_srv, undo_srv)
            library.start()
        elif settings.ui_type == 'gui':
            gui = GUI(client_srv, book_srv, rental_srv, undo_srv)
            gui.start()
        else:
            raise Exception("Invalid settings option!")
    except Exception as e:
        print(e, "Bye!")
