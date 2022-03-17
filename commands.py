from tkinter import *
import tkinter.messagebox as tm
from Domain.bookStock import Book
from Domain.clientStock import Client
from Domain.rentalStock import Rental

class GUI:
    def __init__(self,client_srv, book_srv, rental_srv, undo_srv):
        self._client_srv=client_srv
        self._book_srv=book_srv
        self._rental_srv=rental_srv
        self._undo_srv=undo_srv

    def command(self, command, a, b=None, c=None, d=None, e=None):
        if command == 1:
            try:
                self._client_srv.add(Client(a, b))
            except Exception as ex:
                tm.showerror("Error!", str(ex))
            else:
                label = Label(self.add_client_frame, text="Client successfully added!")
                label.grid(row=5, column=1)
        elif command == 2:
            try:
                self._book_srv.add(Book(a, b, c))
            except Exception as ex:
                tm.showerror("Error!", str(ex))
            else:
                # tm.showinfo("Alert!", "Client successfully added!")
                label = Label(self.add_book_frame, text="Book successfully added!")
                label.grid(row=5, column=1)
        elif command == 3:
            try:
                self._client_srv.remove(a)
            except Exception as ex:
                tm.showerror("Error!", str(ex))
            else:
                label = Label(self.remove_client_frame, text="Client successfully removed!")
                label.grid(row=5, column=1)
        elif command == 4:
            try:
                self._book_srv.remove(a)
            except Exception as ex:
                tm.showerror("Error!", str(ex))
            else:
                label = Label(self.remove_book_frame, text="Book successfully removed!")
                label.grid(row=5, column=1)
        elif command == 5:
            try:
                self._client_srv.update(a, b)
            except Exception as ex:
                tm.showerror("Error!", str(ex))
            else:
                label = Label(self.update_client_frame, text="Client successfully updated!")
                label.grid(row=5, column=1)
        elif command == 6:
            try:
                self._book_srv.update(a, b, c)
            except Exception as ex:
                tm.showerror("Error!", str(ex))
            else:
                label = Label(self.update_book_frame, text="Book successfully updated!")
                label.grid(row=5, column=1)
        elif command == 7:
            try:
                list_ = self._client_srv.search(str(a).lower())
                t = Text(self.search_client_frame)
                if len(list_) == 0:
                    t.insert(END, "No element found!")
                else:
                    for client in list_:
                        t.insert(END, str(client) + '\n')
                t.grid(row=6, column=0, rowspan=3, columnspan=3)
            except Exception as ex:
                tm.showerror("Error!", str(ex))
        elif command == 8:
            try:
                list_ = self._book_srv.search(str(a).lower())
            except Exception as ex:
                tm.showerror("Error!", str(ex))
            else:
                t = Text(self.search_book_frame)
                if len(list_) == 0:
                    t.insert(END, "No element found!")
                else:
                    for book in list_:
                        t.insert(END, str(book) + '\n')
                t.grid(row=6, column=0, rowspan=3, columnspan=3)
        elif command == 9:
            from datetime import date
            try:
                if e == "" and d == "":
                    self._rental_srv.rent(Rental(a, b, c))
                elif e == "":
                    d = str(d).split("-")
                    start_date = date(int(d[0]), int(d[1]), int(d[2]))

                    self._rental_srv.rent(Rental(int(a), int(b), int(c), start_date))
                else:
                    d = str(d).split("-")
                    start_date = date(int(d[0]), int(d[1]), int(d[2]))
                    e = str(e).split("-")
                    end_date = date(int(e[0]), int(e[1]), int(e[2]))

                    self._rental_srv.rent(Rental(int(a), int(b), int(c), start_date, end_date))
            except Exception as ex:
                tm.showerror("Error!", str(ex))
            else:
                label = Label(self.rent_frame, text="Rental successfully added!")
                label.grid(row=5, column=1)
        elif command == 10:
            try:
                self._rental_srv.returned(int(a))
            except Exception as ex:
                tm.showerror("Error!", str(ex))
            else:
                label = Label(self.return_frame, text="Book successfully returned!")
                label.grid(row=5, column=1)

    def add_new_client(self):
        self.hide_all_frames()
        self.add_client_frame.pack(fill="both", expand=1)

        L1 = Label(self.add_client_frame, text="Give id:")
        E1 = Entry(self.add_client_frame, bd=5)

        L2 = Label(self.add_client_frame, text="Give name:")
        E2 = Entry(self.add_client_frame, bd=5)

        L1.grid(row=0)
        L2.grid(row=1)
        E1.grid(row=0, column=1)
        E2.grid(row=1, column=1)

        button_1 = Button(self.add_client_frame, text="Press after entering the data",
                          command=lambda: self.command(1, str(E1.get()), str(E2.get())))
        button_1.grid(row=4, column=0)

    def add_new_book(self):
        self.hide_all_frames()
        self.add_book_frame.pack(fill="both", expand=1)

        L1 = Label(self.add_book_frame, text="Give id:")
        E1 = Entry(self.add_book_frame, bd=5)

        L2 = Label(self.add_book_frame, text="Give title:")
        E2 = Entry(self.add_book_frame, bd=5)

        L3 = Label(self.add_book_frame, text="Give author:")
        E3 = Entry(self.add_book_frame, bd=5)

        L1.grid(row=0)
        L2.grid(row=1)
        L3.grid(row=2)
        E1.grid(row=0, column=1)
        E2.grid(row=1, column=1)
        E3.grid(row=2, column=1)

        button_1 = Button(self.add_book_frame, text="Press after entering the data",
                          command=lambda: self.command(2, str(E1.get()), str(E2.get()), str(E3.get())))
        button_1.grid(row=3, column=0)

    def list_client(self):
        self.hide_all_frames()
        self.list_client_frame.pack(fill="both", expand=1)
        self.t1.delete(1.0, END)
        list = sorted(self._client_srv.repo.client_list, key=lambda client: int(client.client_id))
        for client in list:
            self.t1.insert(END, str(client) + '\n')

    def list_book(self):
        self.hide_all_frames()
        self.list_book_frame.pack(fill="both", expand=1)

        self.t2.delete(1.0, END)
        list = sorted(self._book_srv.repo.book_list, key=lambda book: int(book.book_id))
        for book in list:
            self.t2.insert(END, str(book) + '\n')

    def list_rentals(self):
        self.hide_all_frames()
        self.list_rental_frame.pack(fill="both", expand=1)

        self.t3.delete(1.0, END)
        list = sorted(self._rental_srv.repo.rental_list, key=lambda rental: int(rental.rental_id))
        for rental in list:
            self.t3.insert(END, str(rental) + '\n')

    def remove_client(self):
        self.hide_all_frames()
        self.remove_client_frame.pack(fill="both", expand=1)

        L1 = Label(self.remove_client_frame, text="Give id:")
        E1 = Entry(self.remove_client_frame, bd=5)

        L1.grid(row=0)
        E1.grid(row=0, column=1)
        button_1 = Button(self.remove_client_frame, text="Press after entering the data",
                          command=lambda: self.command(3, str(E1.get())))
        button_1.grid(row=3, column=0)

    def remove_book(self):
        self.hide_all_frames()
        self.remove_book_frame.pack(fill="both", expand=1)

        L1 = Label(self.remove_book_frame, text="Give id:")
        E1 = Entry(self.remove_book_frame, bd=5)

        L1.grid(row=0)
        E1.grid(row=0, column=1)

        button_1 = Button(self.remove_book_frame, text="Press after entering the data",
                          command=lambda: self.command(4, str(E1.get())))
        button_1.grid(row=3, column=0)

    def update_client(self):
        self.hide_all_frames()
        self.update_client_frame.pack(fill="both", expand=1)

        L1 = Label(self.update_client_frame, text="Give id:")
        E1 = Entry(self.update_client_frame, bd=5)

        L2 = Label(self.update_client_frame, text="Give name:")
        E2 = Entry(self.update_client_frame, bd=5)

        L1.grid(row=0)
        L2.grid(row=1)
        E1.grid(row=0, column=1)
        E2.grid(row=1, column=1)

        button_1 = Button(self.update_client_frame, text="Press after entering the data",
                          command=lambda: self.command(5, str(E1.get()), str(E2.get())))
        button_1.grid(row=3, column=0)

    def update_book(self):
        self.hide_all_frames()
        self.update_book_frame.pack(fill="both", expand=1)

        L1 = Label(self.update_book_frame, text="Which id to update?")
        E1 = Entry(self.update_book_frame, bd=5)

        L2 = Label(self.update_book_frame, text="Give title:")
        E2 = Entry(self.update_book_frame, bd=5)

        L3 = Label(self.update_book_frame, text="Give author:")
        E3 = Entry(self.update_book_frame, bd=5)

        L1.grid(row=0)
        L2.grid(row=1)
        L3.grid(row=2)
        E1.grid(row=0, column=1)
        E2.grid(row=1, column=1)
        E3.grid(row=2, column=1)

        button_1 = Button(self.update_book_frame, text="Press after entering the data",
                          command=lambda: self.command(6, str(E1.get()), str(E2.get()), str(E3.get())))
        button_1.grid(row=3, column=0)

    def search_client(self):
        self.hide_all_frames()
        self.search_client_frame.pack(fill="both", expand=1)

        L1 = Label(self.search_client_frame, text="Give element:")
        E1 = Entry(self.search_client_frame, bd=5)

        L1.grid(row=0)
        E1.grid(row=0, column=1)
        button_1 = Button(self.search_client_frame, text="Press after entering the data",
                          command=lambda: self.command(7, str(E1.get())))
        button_1.grid(row=3, column=0)

    def search_book(self):
        self.hide_all_frames()
        self.search_book_frame.pack(fill="both", expand=1)

        L1 = Label(self.search_book_frame, text="Give element:")
        E1 = Entry(self.search_book_frame, bd=5)

        L1.grid(row=0)
        E1.grid(row=0, column=1)
        button_1 = Button(self.search_book_frame, text="Press after entering the data",
                          command=lambda: self.command(8, str(E1.get())))
        button_1.grid(row=3, column=0)

    def rent(self):
        self.hide_all_frames()
        self.rent_frame.pack(fill="both", expand=1)

        L1 = Label(self.rent_frame, text="Give rental id:")
        E1 = Entry(self.rent_frame, bd=5)

        L2 = Label(self.rent_frame, text="Give book id:")
        E2 = Entry(self.rent_frame, bd=5)

        L3 = Label(self.rent_frame, text="Give client id:")
        E3 = Entry(self.rent_frame, bd=5)

        L4 = Label(self.rent_frame, text="Give rented date:")
        E4 = Entry(self.rent_frame, bd=5)

        L5 = Label(self.rent_frame, text="Give returned date:")
        E5 = Entry(self.rent_frame, bd=5)

        L1.grid(row=0)
        L2.grid(row=1)
        L3.grid(row=2)
        L4.grid(row=3)
        L5.grid(row=4)
        E1.grid(row=0, column=1)
        E2.grid(row=1, column=1)
        E3.grid(row=2, column=1)
        E4.grid(row=3, column=1)
        E5.grid(row=4, column=1)

        button_1 = Button(self.rent_frame, text="Press after entering the data",
                          command=lambda: self.command(9, str(E1.get()), str(E2.get()), str(E3.get()), str(E4.get()),
                                                  str(E5.get())))
        button_1.grid(row=6, column=0)

    def return_book(self):
        self.hide_all_frames()
        self.return_frame.pack(fill="both", expand=1)

        L1 = Label(self.return_frame, text="Give rental id:")
        E1 = Entry(self.return_frame, bd=5)

        L1.grid(row=0)
        E1.grid(row=0, column=1)

        button_1 = Button(self.return_frame, text="Press after entering the data",
                          command=lambda: self.command(10, str(E1.get())))
        button_1.grid(row=1, column=0)

    def statistic_most_rented_books(self):
        self.hide_all_frames()
        self.statistic_book_frame.pack(fill="both", expand=1)

        self.s1.delete(1.0, END)
        list_ = self._rental_srv.rented_books()
        for elem in list_:
            self.s1.insert(END, str(elem) + '\n')

    def statistic_most_rented_author(self):
        self.hide_all_frames()
        self.statistic_author_frame.pack(fill="both", expand=1)

        self.s2.delete(1.0, END)
        list_ = self._rental_srv.rented_author()
        for elem in list_:
            self.s2.insert(END, str(elem) + '\n')

    def statistic_most_active_clients(self):
        self.hide_all_frames()
        self.statistic_client_Frame.pack(fill="both", expand=1)

        self.s3.delete(1.0, END)
        list_ = self._rental_srv.active_clients()
        for elem in list_:
            self.s3.insert(END, str(elem) + '\n')

    def undo(self):
        try:
            self._undo_srv.undo()
        except Exception as ex:
            tm.showerror("Error!", str(ex))

    def redo(self):

        try:
            self._undo_srv.redo()
        except Exception as ex:
            tm.showerror("Error!", str(ex))

    def hide_all_frames(self):
        self.add_client_frame.pack_forget()
        self.add_book_frame.pack_forget()
        self.list_client_frame.pack_forget()
        self.list_book_frame.pack_forget()
        self.list_rental_frame.pack_forget()
        self.remove_book_frame.pack_forget()
        self.remove_client_frame.pack_forget()
        self.update_book_frame.pack_forget()
        self.update_client_frame.pack_forget()
        self.search_book_frame.pack_forget()
        self.search_client_frame.pack_forget()
        self.rent_frame.pack_forget()
        self.return_frame.pack_forget()
        self.statistic_client_Frame.pack_forget()
        self.statistic_author_frame.pack_forget()
        self.statistic_book_frame.pack_forget()
        
    def start(self):
        root = Tk()  # blank page
        root.geometry("500x400")
        menubar = Menu(root)

        self.addmenu = Menu(menubar, tearoff=0)
        self.removemenu = Menu(menubar, tearoff=0)
        self.updatemenu = Menu(menubar, tearoff=0)
        self.searchmenu = Menu(menubar, tearoff=0)
        self.listmenu = Menu(menubar, tearoff=0)
        self.rentalmenu = Menu(menubar, tearoff=0)
        self.statisticsmenu = Menu(menubar, tearoff=0)
        self.moremenu = Menu(menubar, tearoff=0)

        # add
        self.addmenu.add_command(label="Book", command=self.add_new_book)
        self.addmenu.add_command(label="Client", command=self.add_new_client)

        menubar.add_cascade(label="Add", menu=self.addmenu)

        # remove
        self.removemenu.add_command(label="Book", command=self.remove_book)
        self.removemenu.add_command(label="Client", command=self.remove_client)

        menubar.add_cascade(label="Remove", menu=self.removemenu)

        # update
        self.updatemenu.add_command(label="Book", command=self.update_book)
        self.updatemenu.add_command(label="Client", command=self.update_client)

        menubar.add_cascade(label="Update", menu=self.updatemenu)

        # search
        self.searchmenu.add_command(label="Book", command=self.search_book)
        self.searchmenu.add_command(label="Client", command=self.search_client)

        menubar.add_cascade(label="Search", menu=self.searchmenu)

        # list
        self.listmenu.add_command(label="Book", command=self.list_book)
        self.listmenu.add_command(label="Client", command=self.list_client)
        self.listmenu.add_command(label="Rentals", command=self.list_rentals)

        menubar.add_cascade(label="List", menu=self.listmenu)

        # rental
        menubar.add_cascade(label="Rental", menu=self.rentalmenu)
        self.rentalmenu.add_command(label="Rent", command=self.rent)
        self.rentalmenu.add_command(label="Return book", command=self.return_book)

        # statistics
        menubar.add_cascade(label="Statistics", menu=self.statisticsmenu)
        self.statisticsmenu.add_command(label="Most rented books", command=self.statistic_most_rented_books)
        self.statisticsmenu.add_command(label="Most active clients", command=self.statistic_most_active_clients)
        self.statisticsmenu.add_command(label="Most rented author", command=self.statistic_most_rented_author)

        # undo/redo
        menubar.add_cascade(label="More...", menu=self.moremenu)

        self.moremenu.add_command(label="Undo", command=self.undo)
        self.moremenu.add_command(label="Redo", command=self.redo)
        # exit
        menubar.add_command(label="Exit", command=root.quit)

        # declare frames
        self.add_client_frame = Frame(root)
        self.add_book_frame = Frame(root)
        self.list_client_frame = Frame(root)
        self.t1 = Text(self.list_client_frame)
        self.t1.pack()
        self.list_book_frame = Frame(root)
        self.t2 = Text(self.list_book_frame)
        self.t2.pack()
        self.list_rental_frame = Frame(root)
        self.t3 = Text(self.list_rental_frame)
        self.t3.pack()
        self.remove_book_frame = Frame(root)
        self.remove_client_frame = Frame(root)
        self.update_client_frame = Frame(root)
        self.update_book_frame = Frame(root)
        self.rent_frame = Frame(root)
        self.return_frame = Frame(root)

        self.statistic_book_frame = Frame(root)
        self.s1 = Text(self.statistic_book_frame)
        self.s1.pack()
        self.statistic_client_Frame = Frame(root)
        self.s2 = Text(self.statistic_client_Frame)
        self.s2.pack()
        self.statistic_author_frame = Frame(root)
        self.s3 = Text(self.statistic_author_frame)
        self.s3.pack()

        self.search_client_frame = Frame(root)
        self.search_book_frame = Frame(root)

        root.config(menu=menubar)
        root.mainloop()
