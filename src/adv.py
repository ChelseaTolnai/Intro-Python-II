import textwrap
import color

from room import Room
from player import Player
from item import Item

# Declare all the rooms

room = {
    'outside':  Room("Outside Cave Entrance",
                     "North of you, the cave mount beckons."),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east."""),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm."""),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air."""),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south... Or is it?"""),

    'den': Room("Snake Den", """You've entered a dimly lit area surrounded by
snakes. One false move in the wrong direction will cause a snake to attack
and the venom will kill you instantly."""),

    'cavern': Room("Miner's Cavern", """The room is filled with stalagmites and
stalactites with nooks and crannies everywhere. Looks like at one point miners
tried to work in here."""),
}


# Link rooms together

room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['overlook'].s_to = room['foyer']
room['overlook'].n_to = room['den']
room['den'].s_to = room['overlook']
room['den'].w_to = room['cavern']
room['cavern'].e_to = room['den']
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']

#
# Main
#

# Make a new player object that is currently in the 'outside' room.

player = {
    'player1': Player('Mr. Adventure', room['outside']),
}

# Create items

item = {
    'rope':    Item("Rope", """Sturdy braided rope approximately 30 feet
 in length."""),

    'torch':   Item("Torch", """Portable source of light and heat."""),

    'pickaxe': Item("Pickaxe", """Multi-use hand tool with a metal
 spike attached perpendicularly to a wooden handle."""),

    'boulder':    Item("Boulder", """A large rock too heavy to pick up
 located near the steep cliff.""")
}

# Added items to rooms

room['foyer'].add_item(item['rope'])
room['overlook'].add_item(item['boulder'])
room['den'].add_item(item['boulder'])
room['cavern'].add_item(item['pickaxe'])
room['treasure'].add_item(item['torch'])


# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.


def get_inv(inventory, current_room):
    if inventory == 'i':
        if len(player.list_items()) < 1:
            color.prCyan(f"\nYou don't have any items at this time.")
        else:
            color.prCyan(f"\nYou are currently carrying:")
            for i in player.list_items():
                color.prCyan(f'-{i}')
        color.prGreen("What would you like to do?")

    elif inventory == 'l':
        if len(current_room.list_items()) < 1:
            color.prCyan(f"\nYou look arround and see that the area is empty.")
        else:
            color.prCyan(f"\nYou look around and find:")
            for i in current_room.list_items():
                color.prCyan(f'-{i}')
        color.prGreen(f"{textwrap.fill(str(player))}")


def check_inv(item):
    has_item = [True for i in player.items if i.name.lower() == item]
    if has_item == [True]:
        return True
    else:
        return False


def has_rope():
    if check_inv('rope'):
        text = "You succesfully lassoed the rope to a boulder accross " \
               "the chasm and tied the rope to a boulder in the current " \
               "room. You shimmy accross the rope and untie it.\n"
        color.prGreen(f"\n{textwrap.fill(text)}")
        return True
    else:
        color.prRed("\nYou attempted to leap accross the chasm and "
                    "failed!")
        color.prYellow("Next time try to use an item to cross.")
        color.prGreen("Try again!\n")
        return False


def check_room(direction, current_room):
    if current_room.name == 'Snake Den':
        if direction == 'n' or direction == 'e':
            color.prRed("\nA snake has attacked and you died instanstly!")
            color.prGreen("Try again!\n")
            return False
        elif direction == 's':
            if has_rope():
                return True
            else:
                return False
        else:
            return True
    elif current_room.name == 'Grand Overlook':
        if direction == 'n':
            if has_rope():
                return True
            else:
                return False
        else:
            return True
    else:
        return True


def go_dir(direction, current_room):
    if check_room(direction, current_room) is True:
        if direction == 'n' and current_room.n_to:
            go_room(current_room.n_to)
        elif direction == 's' and current_room.s_to:
            go_room(current_room.s_to)
        elif direction == 'e' and current_room.e_to:
            go_room(current_room.e_to)
        elif direction == 'w' and current_room.w_to:
            go_room(current_room.w_to)
        else:
            color.prYellow(f"\nYou cannot go this way from"
                           f"{current_room.name}. ")
            text = f"{current_room.description} What would you like to do?"
            color.prGreen(f"{textwrap.fill(text)}")
    else:
        global game
        game = False


def go_room(new_room):
    player.current_room = new_room
    color.prGreen(f"\n{textwrap.fill(str(player))}")


def take_item(current_item, current_room):
    room_item = [True for i in current_room.items
                 if current_item == i.name.lower()]
    if len(room_item) > 0:
        if current_item == 'boulder':
            color.prYellow(f"\nItem is too heavy to pick up. ")
        else:
            color.prGreen(f"\n{item[current_item].on_take(player)}")
    else:
        color.prYellow(f"\nItem is not in the {current_room.name}. ")


def drop_item(current_item, current_room):
    player_item = [True for i in player.items
                   if current_item == i.name.lower()]
    if len(player_item) > 0:
        color.prGreen(f"\n{item[current_item].on_drop(player)}")
    else:
        color.prYellow(f"\nYou are not carrying that item. ")

game = True
try:
    player = player['player1']
    color.prGreen(f"\nWelcome {player.name}! {textwrap.fill(str(player))}")

    while game:
        print("\nOptions     = [l]:look around / [i]:inventory / [q]:quit"
              "\nMove        = "
              "[n]:go north    / "
              "[s]:go south  / "
              "[e]:go east / "
              "[w]:go west"
              "\nOther       = [action] [object]"
              )

        cmd = input("Enter action: ")
        cmd = cmd.split(' ')
        action = cmd[0].lower()

        if len(cmd) == 1:
            if len(action) == 1:
                if action == 'q':
                    color.prGreen("\nCome back soon!\n")
                    break
                elif action == 'l' or action == 'i':
                    get_inv(action, player.current_room)
                elif (action == 'n' or action == 's' or
                      action == 'e' or action == 'w'):
                    go_dir(action, player.current_room)
                else:
                    color.prRed("\nInvalid action.")
            else:
                color.prYellow(f"\n{action} what?")
        else:
            obj = cmd[1].lower()
            if action == 'take' or action == 'get' or action == 'add':
                take_item(obj, player.current_room)
            elif action == 'drop' or action == 'leave' or action == 'remove':
                drop_item(obj, player.current_room)
            else:
                color.prRed("\nInvalid action.")

except:
    color.prRed("\nOops, something went wrong!\n")
