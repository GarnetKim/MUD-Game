import glob
import os
import json
import datetime
from typing import Dict, Any, List, Optional

from player import Player
from item import Item

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
        "enhance_level": getattr(item, "enhance_level", 0),
        "durability": getattr(item, "durability", 0),
        "max_durability": getattr(item, "max_durability", 0),
        "extra_options": list(getattr(item, "extra_options", [])),
        "resistances": dict(getattr(item, "resistances", {})),
    }


def deserialize_item(data: Dict[str, Any]) -> Item:
    # type_ 매개변수 주의
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
    item.max_durability = data.get("max_durability", 0)
    item.extra_options = data.get("extra_options", [])
    return item


# -----------------------------
# Player <-> dict 직렬화/역직렬화
# -----------------------------
def serialize_player(p: Player) -> Dict[str, Any]:
    # 인벤토리 먼저 직렬화
    inventory_serialized = [serialize_item(i) for i in getattr(p, "inventory", [])]

    # 장비 인덱스 (인벤토리 내 위치로 복원)
    def index_of_equipped(target: Optional[Item]) -> Optional[int]:
        if target is None:
            return None
        for idx, it in enumerate(getattr(p, "inventory", [])):
            if it is target:
                return idx
        return None  # 못찾으면 None (호환: 로드시 fallback)

    equipped = {
        "weapon_index": index_of_equipped(getattr(p, "weapon", None)),
        "armor_index": index_of_equipped(getattr(p, "armor", None)),
    }

    data: Dict[str, Any] = {
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
        "equipped": equipped,

        # 상태이상 & 전투 로그/이력
        "status_effects": list(getattr(p, "status_effects", [])),
        "combat_log": list(getattr(p, "combat_log", [])),
        "effect_history": list(getattr(p, "effect_history", [])),            # 스킬/버프 이펙트 히스토리
        "set_bonus_history": list(getattr(p, "set_bonus_history", [])),      # 세트 보너스 이펙트 히스토리

        # 스킬/도감/쿨타임
        "skills": dict(getattr(p, "skills", {})),                 # {"heal": 2, "fireball": 1, ...}
        "skill_codex": dict(getattr(p, "skill_codex", {})),       # 도감: 최대 해금 레벨 기록
        "skill_cooldowns": dict(getattr(p, "skill_cooldowns", {})),  # {"heal": 2, ...}
        "ultimate_used": getattr(p, "ultimate_used", False),

        # 세트/도감
        "set_codex_unlocked": dict(getattr(p, "set_codex_unlocked", {})),  # 세트 도감 잠금 해제 상태
        "item_codex_unlocked": dict(getattr(p, "item_codex_unlocked", {})),# 아이템 도감 잠금 해제 상태

        # 칭호 시스템
        "titles": list(getattr(p, "titles", [])),
        "active_title": getattr(p, "active_title", None),

        # 옵션/환경
        "autoload_enabled": getattr(p, "autoload_enabled", True),
        "inventory_sort_preference": getattr(p, "inventory_sort_preference", "희귀도"),
    }

    return data


def deserialize_player(data: Dict[str, Any]) -> Player:
    # 이름은 반드시 필요
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
    player.inventory = [deserialize_item(i) for i in inv_raw]

    # 장비 인덱스 복원 (없거나 범위 밖이면 무시)
    eq = data.get("equipped", {}) or {}
    w_idx = eq.get("weapon_index", None)
    a_idx = eq.get("armor_index", None)
    if isinstance(w_idx, int) and 0 <= w_idx < len(player.inventory):
        player.weapon = player.inventory[w_idx]
    else:
        player.weapon = None
    if isinstance(a_idx, int) and 0 <= a_idx < len(player.inventory):
        player.armor = player.inventory[a_idx]
    else:
        player.armor = None

    # 상태/로그/이력
    player.status_effects = list(data.get("status_effects", []))
    player.combat_log = list(data.get("combat_log", []))
    player.effect_history = list(data.get("effect_history", []))
    player.set_bonus_history = list(data.get("set_bonus_history", []))

    # 스킬/도감/쿨타임
    player.skills = dict(data.get("skills", getattr(player, "skills", {})))
    player.skill_codex = dict(data.get("skill_codex", getattr(player, "skill_codex", {})))
    player.skill_cooldowns = dict(data.get("skill_cooldowns", {}))
    player.ultimate_used = data.get("ultimate_used", False)

    # 세트/도감
    player.set_codex_unlocked = dict(data.get("set_codex_unlocked", {}))
    player.item_codex_unlocked = dict(data.get("item_codex_unlocked", {}))

    # 칭호
    player.titles = list(data.get("titles", []))
    player.active_title = data.get("active_title", None)

    # 옵션/환경
    player.autoload_enabled = data.get("autoload_enabled", True)
    player.inventory_sort_preference = data.get("inventory_sort_preference", "희귀도")

    return player


# -----------------------------
# 저장 / 로드 유틸
# -----------------------------
def prune_old_saves(max_keep: int = MAX_KEEP):
    saves = sorted(glob.glob(SAVE_PATTERN), key=os.path.getmtime)
    if len(saves) > max_keep:
        to_delete = saves[:-max_keep]
        for old in to_delete:
            try:
                os.remove(old)
                print(f"🗑 오래된 세이브 삭제: {old}")
            except Exception as e:
                print(f"⚠️ 세이브 삭제 실패: {old} ({e})")


def save_game(player: Player):
    # 날짜+시간 포함 파일명
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"save_{now}.json"

    payload = {
        "schema": "mudgame.v2",        # 스키마 버전 명시 (호환성)
        "saved_at": now,
        "player": serialize_player(player)
        # 추후 world/dungeon/state 등을 추가하려면 여기 확장
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"💾 자동 저장 완료! ({filename})")
    prune_old_saves(MAX_KEEP)


def _read_json(filename: str) -> Dict[str, Any]:
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def load_game_from_file(filename: str) -> Player:
    data = _read_json(filename)

    # 호환성: v2는 {"player": {...}}, 구버전은 루트에 필드가 바로 있음
    if "player" in data:
        p_data = data["player"]
    else:
        p_data = data  # 구버전 호환

    player = deserialize_player(p_data)
    return player


def auto_load_latest() -> Optional[Player]:
    saves = glob.glob(SAVE_PATTERN)
    if not saves:
        print("⚠️ 저장 파일 없음, 새 게임을 시작합니다.")
        return None

    latest = max(saves, key=os.path.getmtime)
    player = load_game_from_file(latest)
    print(f"📂 최근 저장 불러오기 완료! ({latest})")
    return player