import json, os
from mudgame.player import Player

SAVE_DIR = "saves"

def save_game(player):
    os.makedirs(SAVE_DIR, exist_ok=True)
    path = os.path.join(SAVE_DIR, "latest.json")
    data = {
        "name": player.name, "level": player.level, "exp": player.exp,
        "hp": player.hp, "max_hp": player.max_hp,
        "mp": player.mp, "max_mp": player.max_mp,
        "atk": player.atk, "defense": player.defense,
        "gold": player.gold,
        "inventory": [i.name for i in player.inventory],
        "titles": player.titles,
        "active_title": player.active_title,
        "codex": {k: list(v) for k,v in player.codex.items()}
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def auto_load_latest():
    path = os.path.join(SAVE_DIR, "latest.json")
    if not os.path.exists(path): return None
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    p = Player(data["name"])
    p.level = data["level"]; p.exp = data["exp"]
    p.hp = data["hp"]; p.max_hp = data["max_hp"]
    p.mp = data["mp"]; p.max_mp = data["max_mp"]
    p.atk = data["atk"]; p.defense = data["defense"]
    p.gold = data["gold"]
    p.titles = data.get("titles", [])
    p.active_title = data.get("active_title")
    p.codex = {k: set(v) for k,v in data.get("codex", {}).items()}
    return p