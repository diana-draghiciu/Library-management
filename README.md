# Library-management

A Python layered architecture implementation that manages books, clients and rentals. Every data is validated. Implemented using an iterable data structure and tested data structure using PyUnit tests (100% coverage).


Using a settings.properties file, the user can choose whether to use the console or the grafical interface (implemented using tkinter). They can also choose the type of file from which to model data (.json, .txt, .bin, .db, or even use in memory generated data). 
The user has the ability to view all data, to add/delete/update/partial search books or clients from the system, to rent or return a book, to display several statistics (most rented books, most active clients, most rented author) and to undo/redo operations. 
