from mudgame.item import Item

class Player:
    def __init__(self, name="용사"):
        self.name = name
        self.level = 1
        self.exp = 0
        self.hp = 100
        self.max_hp = 100
        self.mp = 30
        self.max_mp = 30
        self.atk = 10
        self.defense = 5
        self.gold = 100
        self.inventory = []
        self.weapon = None
        self.armor = None
        self.titles = []       # 칭호 보유
        self.active_title = None
        self.codex = {"items": set(), "sets": set(), "skills": set()}  # 도감

    def add_item(self, item: Item):
        self.inventory.append(item)
        self.codex["items"].add(item.name)

    def equip(self, item: Item):
        if item.type == "weapon":
            self.weapon = item
        elif item.type == "armor":
            self.armor = item

    def stats(self):
        atk = self.atk + (self.weapon.attack if self.weapon else 0)
        defense = self.defense + (self.armor.defense if self.armor else 0)
        return atk, defense