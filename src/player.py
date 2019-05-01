# Write a class to hold player information, e.g. what room they are in
# currently.
from item import Items


class Player(Items):
    def __init__(self, name, current_room):
        self.name = name
        self.current_room = current_room

    def __str__(self):
        return f'{self.name}, you are in the {self.current_room} ' \
                'What would you like to do?'
