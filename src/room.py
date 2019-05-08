# Implement a class to hold room information. This should have name and
# description attributes.


class Room:
    def __init__(self, name, description,
                 n_to=False, s_to=False, e_to=False, w_to=False
                 ):
        self.name = name
        self.description = description
        self.items = []
        self.n_to = n_to
        self.s_to = s_to
        self.e_to = e_to
        self.w_to = w_to

    def __str__(self):
        return f'{self.name}. {self.description}'

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def list_items(self):
        return [f'{i.name} ({i.description})' for i in self.items]
