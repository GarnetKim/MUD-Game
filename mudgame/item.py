class Item:
    def __init__(self, name, type, rarity="일반", attack=0, defense=0,
                 resistances=None, price=0, heal=0, mp_restore=0, durability=100, max_durability=100,
                 upgrade_level=0, special_effects=None):
        self.name = name
        self.type = type              # weapon, armor, consumable, material
        self.rarity = rarity
        self.attack = attack
        self.defense = defense
        self.resistances = resistances or {}
        self.price = price
        self.heal = heal
        self.mp_restore = mp_restore
        self.durability = durability
        self.max_durability = max_durability
        self.upgrade_level = upgrade_level
        self.special_effects = special_effects or []   # ex: ["흡혈", "치명타+10%"]

    def short_name(self):
        return f"{self.display_name()} ({self.rarity})"

    def display_name(self):
        prefix = ""
        if self.upgrade_level >= 10: prefix = "궁극의 "
        elif self.upgrade_level >= 5: prefix = "강화된 "
        suffix = f" +{self.upgrade_level}" if self.upgrade_level > 0 else ""
        return f"{prefix}{self.name}{suffix}"