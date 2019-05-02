import color


class Item:
    def __init__(self, name, description, can_take=True):
        self.name = name
        self.description = description
        self.can_take = can_take

    def __str__(self):
        return f'{self.name}. {self.description} '

    def on_take(self, player):
        if self.can_take:
            player.add_item(self)
            player.current_room.remove_item(self)
            color.prGreen(f'\nYou have picked up the {self.name}.')
            return True
        else:
            color.prYellow(f'\nYou cannot pick up the {self.name}.')
            return False

    def on_drop(self, player):
        player.remove_item(self)
        player.current_room.add_item(self)
        return f'You have dropped the {self.name}.'
