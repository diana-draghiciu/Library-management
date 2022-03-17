import unittest

from Domain.clientStock import Client
from Iterable.iterable import MyIterable


class Test(unittest.TestCase):
    def test_filter(self):
        clients = [Client(1, 'Berna'), Client(5, 'Clara'), Client(3, 'Anabela'), Client(2, 'Joana')]
        my_list = MyIterable.filter(clients, lambda x: x.client_id == 3)
        self.assertEqual(my_list, [clients[2]])

    def test_sort(self):
        my_list = [4, 8, 2, 1, 5]
        MyIterable.sort(my_list, lambda x, y: x < y)
        self.assertEqual(my_list, [1, 2, 4, 5, 8])

    def test_len(self):
        my_list = MyIterable()
        #test append
        for i in range(5):
            my_list.append(i)
        #test pop
        my_list.pop(4)

        self.assertEqual(len(my_list), my_list.__len__())
        self.assertEqual(len(my_list), 4)

        my_list.__setitem__(0,10)
        self.assertEqual(my_list[0],10)

        it1 = iter(my_list)


if __name__ == '__main__':
    unittest.main()
