class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return f'{self.name}. {self.description} '

    def on_take(self, player):
        player.add_item(self)
        player.current_room.remove_item(self)
        return f'You have picked up the {self.name}.'

    def on_drop(self, player):
        player.remove_item(self)
        player.current_room.add_item(self)
        return f'You have dropped the {self.name}.'
