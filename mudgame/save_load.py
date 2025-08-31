# save_load.py
import glob
import os
import json
import datetime
from typing import Dict, Any, Optional
from mudgame.player import Player
from mudgame.item import Item

SAVE_PATTERN = "save_*.json"
MAX_KEEP = 5

# -----------------------------
# Item <-> dict 직렬화/역직렬화
# -----------------------------
def serialize_item(item: Item) -> Dict[str, Any]:
    if item is None:
        return None
    return {
        "name": item.name,
        "type": item.type,
        "rarity": item.rarity,
        "attack": item.attack,
        "defense": item.defense,
        "enhance_level": item.enhance_level,
        "durability": item.durability,
        "max_durability": item.max_durability,
        "extra_options": list(item.extra_options),
        "resistances": dict(item.resistances),
    }

def deserialize_item(data: Dict[str, Any]) -> Item:
    item = Item(
        name=data.get("name", "이름없는 아이템"),
        type_=data.get("type", "misc"),
        rarity=data.get("rarity", "일반"),
        attack=data.get("attack", 0),
        defense=data.get("defense", 0),
        resistances=data.get("resistances", {}),
    )
    item.enhance_level = data.get("enhance_level", 0)
    item.durability = data.get("durability", 0)
    item.max_durability = data.get("max_durability", 100)
    item.extra_options = data.get("extra_options", [])
    return item

# -----------------------------
# Player <-> dict 직렬화/역직렬화
# -----------------------------
def serialize_player(p: Player) -> Dict[str, Any]:
    inventory_serialized = [serialize_item(i) for i in p.inventory]

    def index_of_equipped(target: Optional[Item]) -> Optional[int]:
        if target is None:
            return None
        for idx, it in enumerate(p.inventory):
            if it is target:
                return idx
        return None

    return {
        # 기본 스탯
        "name": p.name,
        "level": p.level,
        "exp": p.exp,
        "exp_to_next": p.exp_to_next,
        "hp": p.hp,
        "max_hp": p.max_hp,
        "mp": p.mp,
        "max_mp": p.max_mp,
        "atk": p.atk,
        "defense": p.defense,
        "gold": p.gold,

        # 인벤토리/장비
        "inventory": inventory_serialized,
        "equipped": {
            "weapon_index": index_of_equipped(p.weapon),
            "armor_index": index_of_equipped(p.armor),
        },

        # 상태/로그/이력
        "status_effects": list(p.status_effects),
        "combat_log": list(p.combat_log),
        "effect_history": list(p.effect_history),
        "set_bonus_history": list(p.set_bonus_history),

        # 스킬/도감/쿨타임
        "skills": dict(p.skills),
        "skill_codex": dict(p.skill_codex),
        "skill_cooldowns": dict(p.skill_cooldowns),
        "ultimate_used": p.ultimate_used,

        # 세트/도감
        "set_codex_unlocked": dict(p.set_codex_unlocked),
        "item_codex_unlocked": dict(p.item_codex_unlocked),

        # 칭호
        "titles": list(p.titles),
        "active_title": p.active_title,

        # 옵션
        "autoload_enabled": p.autoload_enabled,
        "inventory_sort_preference": p.inventory_sort_preference,
    }

def deserialize_player(data: Dict[str, Any]) -> Player:
    player = Player(data.get("name", "모험가"))
    # 기본 스탯
    player.level = data.get("level", 1)
    player.exp = data.get("exp", 0)
    player.exp_to_next = data.get("exp_to_next", 100)
    player.hp = data.get("hp", 100)
    player.max_hp = data.get("max_hp", 100)
    player.mp = data.get("mp", 50)
    player.max_mp = data.get("max_mp", 50)
    player.atk = data.get("atk", 10)
    player.defense = data.get("defense", 5)
    player.gold = data.get("gold", 0)

    # 인벤토리
    inv_raw = data.get("inventory", [])
    player.inventory = [deserialize_item(i) for i in inv_raw if i]

    eq = data.get("equipped", {}) or {}
    w_idx = eq.get("weapon_index", None)
    a_idx = eq.get("armor_index", None)
    if isinstance(w_idx, int) and 0 <= w_idx < len(player.inventory):
        player.weapon = player.inventory[w_idx]
    if isinstance(a_idx, int) and 0 <= a_idx < len(player.inventory):
        player.armor = player.inventory[a_idx]

    # 상태/로그
    player.status_effects = list(data.get("status_effects", []))
    player.combat_log = list(data.get("combat_log", []))
    player.effect_history = list(data.get("effect_history", []))
    player.set_bonus_history = list(data.get("set_bonus_history", []))

    # 스킬/도감/쿨타임
    player.skills = dict(data.get("skills", {}))
    player.skill_codex = dict(data.get("skill_codex", {}))
    player.skill_cooldowns = dict(data.get("skill_cooldowns", {}))
    player.ultimate_used = data.get("ultimate_used", False)

    # 세트/도감
    player.set_codex_unlocked = dict(data.get("set_codex_unlocked", {}))
    player.item_codex_unlocked = dict(data.get("item_codex_unlocked", {}))

    # 칭호
    player.titles = list(data.get("titles", []))
    player.active_title = data.get("active_title", None)

    # 옵션
    player.autoload_enabled = data.get("autoload_enabled", True)
    player.inventory_sort_preference = data.get("inventory_sort_preference", "희귀도")

    return player

# -----------------------------
# 저장 / 로드 유틸
# -----------------------------
def prune_old_saves(max_keep: int = MAX_KEEP):
    saves = sorted(glob.glob(SAVE_PATTERN), key=os.path.getmtime)
    if len(saves) > max_keep:
        for old in saves[:-max_keep]:
            try:
                os.remove(old)
                print(f"🗑 오래된 세이브 삭제: {old}")
            except Exception as e:
                print(f"⚠️ 삭제 실패: {old} ({e})")

def save_game(player: Player):
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"save_{now}.json"
    payload = {
        "schema": "mudgame.v2",
        "saved_at": now,
        "player": serialize_player(player)
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"💾 저장 완료 ({filename})")
    prune_old_saves(MAX_KEEP)

def _read_json(filename: str) -> Dict[str, Any]:
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def load_game_from_file(filename: str) -> Player:
    data = _read_json(filename)
    if "player" in data:
        p_data = data["player"]
    else:
        p_data = data
    return deserialize_player(p_data)

def auto_load_latest() -> Optional[Player]:
    saves = glob.glob(SAVE_PATTERN)
    if not saves:
        return None
    latest = max(saves, key=os.path.getmtime)
    player = load_game_from_file(latest)
    print(f"📂 최근 저장 불러오기 완료! ({latest})")
    return player

def choose_save_slot() -> Optional[Player]:
    saves = sorted(glob.glob(SAVE_PATTERN), key=os.path.getmtime, reverse=True)
    if not saves:
        print("⚠️ 저장 파일이 없습니다.")
        return None
    print("\n💾 [저장 슬롯 선택]")
    for idx, s in enumerate(saves, 1):
        print(f"{idx}. {s}")
    choice = input("번호 선택 (취소=0): ").strip()
    if choice == "0":
        return None
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(saves):
            return load_game_from_file(saves[idx])
    except:
        pass
    print("❌ 잘못된 선택")
    return None