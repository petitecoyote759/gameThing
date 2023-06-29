


class Item:

    def __init__(self, pos, name, world):

        self.pos = pos
        self.name = name
        self.image = world.itemPics[self.name]
        self.targeted = False
