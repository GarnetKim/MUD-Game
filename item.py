class Item:
    def __init__(self, name, type_, rarity, attack, defense, resistances=None):
        self.name = name
        self.type = type_
        self.rarity = rarity
        self.attack = attack
        self.defense = defense
        self.enhance_level = 0
        self.durability = 100
        self.max_durability = 100
        self.extra_options = []
        self.resistances = resistances if resistances else {}

def format_item(item):
    if not item:
        return "없음"
    enh = f" +{item.enhance_level}" if item.enhance_level > 0 else ""
    dur = f" ({item.durability}/{item.max_durability})"
    resist_str = ""
    if item.resistances:
        parts = [f"{k}:{v}%" for k,v in item.resistances.items()]
        resist_str = " | 내성: " + ", ".join(parts)
    return f"{item.rarity} {item.name}{enh}{dur}{resist_str}"