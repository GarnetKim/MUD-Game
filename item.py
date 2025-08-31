# item.py

class Item:
    def __init__(self, name, type_, rarity, attack=0, defense=0, resistances=None):
        self.name = name              # 이름
        self.type = type_             # weapon / armor / consumable ...
        self.rarity = rarity          # 일반 / 레어 / 전설
        self.attack = attack
        self.defense = defense

        # 강화/내구도
        self.enhance_level = 0
        self.durability = 100
        self.max_durability = 100

        # 추가 옵션
        self.extra_options: list[str] = []

        # 상태이상 내성
        self.resistances = resistances if resistances else {}

    def is_broken(self) -> bool:
        """내구도가 0 이하인지 체크"""
        return self.durability <= 0

    def short_name(self) -> str:
        """이름 + 강화 단계만 반환"""
        enh = f" +{self.enhance_level}" if self.enhance_level > 0 else ""
        return f"{self.name}{enh}"


# ---------------------------------------
# 아이템 문자열 포매터 (UI 표시용)
# ---------------------------------------
RARITY_ICON = {
    "일반": "⚪",
    "레어": "🔵",
    "전설": "🟡"
}

def format_item(item: Item) -> str:
    if not item:
        return "없음"

    # 희귀도 + 이름 + 강화 단계
    rarity_icon = RARITY_ICON.get(item.rarity, "❔")
    enh = f" +{item.enhance_level}" if item.enhance_level > 0 else ""

    # 내구도 게이지 (🟩🟨🟥)
    dur_ratio = item.durability / item.max_durability if item.max_durability > 0 else 0
    if dur_ratio > 0.6:
        dur_icon = "🟩"
    elif dur_ratio > 0.3:
        dur_icon = "🟨"
    else:
        dur_icon = "🟥"
    durability_str = f"{dur_icon}{item.durability}/{item.max_durability}"

    # 추가 옵션
    extras = ""
    if item.extra_options:
        extras = " | 옵션: " + ", ".join(item.extra_options)

    # 내성 표시
    resist_str = ""
    if item.resistances:
        parts = [f"{k}:{v}%" for k, v in item.resistances.items()]
        resist_str = " | 내성: " + ", ".join(parts)

    return f"{rarity_icon} {item.rarity} {item.name}{enh} ({durability_str}) ATK:{item.attack} DEF:{item.defense}{extras}{resist_str}"