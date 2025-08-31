import json, os
from player import Player

SAVE_FILE = "save.json"

def save_game(player):
    data = {
        "name": player.name,
        "level": player.level,
        "hp": player.hp,
        "max_hp": player.max_hp,
        "mp": player.mp,
        "max_mp": player.max_mp,
        "atk": player.atk,
        "defense": player.defense,
        "gold": player.gold,
        "inventory": [i.name for i in player.inventory],
    }
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def auto_load_latest():
    if not os.path.exists(SAVE_FILE): return None
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    p = Player(data["name"])
    p.level = data["level"]; p.hp = data["hp"]; p.max_hp = data["max_hp"]
    p.mp = data["mp"]; p.max_mp = data["max_mp"]
    p.atk = data["atk"]; p.defense = data["defense"]
    p.gold = data["gold"]
    return p