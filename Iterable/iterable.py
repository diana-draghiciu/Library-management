from Domain.clientStock import Client


class MyIterable:
    def __init__(self):
        self._my_list = []

    def __iter__(self):
        return self._my_list.__iter__()

    def __getitem__(self, item):
        return self.my_list[item]

    def __setitem__(self, index, value):
        self.my_list[index] = value

    def __len__(self):
        return len(self.my_list)

    def append(self, item):
        self.my_list.append(item)

    def pop(self, item):
        self._my_list.pop(item)

    @property
    def my_list(self):
        return self._my_list

    @staticmethod
    def filter(my_list, my_acceptance):
        new_list = []
        for elem in my_list:
            if my_acceptance(elem) is True:
                new_list.append(elem)
        return new_list

    @staticmethod
    def sort(my_list, my_comparison):
        for i in range(len(my_list)-1):
            for j in range(i + 1, len(my_list)):
                if my_comparison(my_list[i], my_list[j]) is False:
                    my_list[i], my_list[j] = my_list[j], my_list[i]




