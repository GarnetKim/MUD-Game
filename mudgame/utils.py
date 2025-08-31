from item import Item

# -------------------------
# 게이지 표시
# -------------------------
def hp_gauge(player) -> str:
    ratio = player.hp / player.max_hp if player.max_hp else 0
    filled = int(ratio * 20)
    gauge = "❤️" * filled + "⬛" * (20 - filled)
    if ratio <= 0.3:
        return f"\033[91m{gauge}\033[0m {player.hp}/{player.max_hp}"  # 빨강 강조
    return f"{gauge} {player.hp}/{player.max_hp}"

def mp_gauge(player) -> str:
    ratio = player.mp / player.max_mp if player.max_mp else 0
    filled = int(ratio * 20)
    gauge = "🔮" * filled + "⬛" * (20 - filled)
    if ratio <= 0.2:
        return f"\033[95m{gauge}\033[0m {player.mp}/{player.max_mp}"  # 보라 강조
    return f"{gauge} {player.mp}/{player.max_mp}"


# -------------------------
# 내구도 게이지
# -------------------------
def durability_gauge(item: Item) -> str:
    if not item:
        return "-"
    ratio = item.durability / item.max_durability if item.max_durability else 0
    if ratio > 0.6:
        icon = "🟩"
    elif ratio > 0.3:
        icon = "🟨"
    else:
        icon = "🟥"
    return f"{icon}{item.durability}/{item.max_durability}"


# -------------------------
# 인벤토리 표 출력
# -------------------------
def show_inventory_table(player, category: str = "all"):
    items = player.inventory
    if category != "all":
        items = [i for i in items if i.type == category]

    if not items:
        print(f"🎒 인벤토리: {category if category!='all' else '전체'} 항목 없음")
        return

    print(f"\n🎒 [인벤토리 - {category if category!='all' else '전체'}]")
    print("─" * 110)
    print(f"{'No':<3} │ {'이름':<20} │ {'희귀도':<4} │ {'강화':<4} │ {'내구도':<10} │ {'ATK':>4} │ {'DEF':>4} │ {'옵션':<20} │ {'내성':<20}")
    print("─" * 110)

    for idx, item in enumerate(items, 1):
        enh = f"+{item.enhance_level}" if item.enhance_level > 0 else "-"
        dur = durability_gauge(item)
        extras = ", ".join(item.extra_options) if item.extra_options else "-"
        resist_str = ", ".join([f"{k}:{v}%" for k, v in item.resistances.items()]) if item.resistances else "-"

        print(f"{idx:<3} │ {item.name:<20} │ {item.rarity:<4} │ {enh:<4} │ {dur:<10} │ {item.attack:>4} │ {item.defense:>4} │ {extras:<20} │ {resist_str:<20}")

    print("─" * 110)


# -------------------------
# 인벤토리 정렬
# -------------------------
RARITY_ORDER = {"일반": 1, "레어": 2, "전설": 3}

def sort_inventory(player, criterion="희귀도"):
    if not player.inventory:
        print("❌ 인벤토리에 아이템이 없습니다.")
        return

    if criterion == "이름":
        player.inventory.sort(key=lambda x: x.name)
    elif criterion == "공격력":
        player.inventory.sort(key=lambda x: x.attack, reverse=True)
    elif criterion == "방어력":
        player.inventory.sort(key=lambda x: x.defense, reverse=True)
    elif criterion == "희귀도":
        player.inventory.sort(
            key=lambda x: (RARITY_ORDER.get(x.rarity, 0), x.enhance_level),
            reverse=True
        )
    else:
        print("⚠️ 잘못된 정렬 기준입니다. (지원: 이름, 공격력, 방어력, 희귀도)")
        return

    print(f"✅ 인벤토리가 '{criterion}' 기준으로 정렬되었습니다.")


# -------------------------
# 인벤토리 필터/검색
# -------------------------
def filter_inventory(player, keyword: str):
    """키워드가 이름/옵션/내성에 들어가는 아이템만 출력"""
    results = []
    for item in player.inventory:
        if (keyword in item.name or
            any(keyword in opt for opt in item.extra_options) or
            any(keyword in k for k in item.resistances.keys())):
            results.append(item)

    if not results:
        print(f"🔍 '{keyword}'에 해당하는 아이템이 없습니다.")
        return

    print(f"\n🎒 [검색 결과: '{keyword}']")
    print("─" * 110)
    print(f"{'No':<3} │ {'이름':<20} │ {'희귀도':<4} │ {'강화':<4} │ {'내구도':<10} │ {'ATK':>4} │ {'DEF':>4} │ {'옵션':<20} │ {'내성':<20}")
    print("─" * 110)

    for idx, item in enumerate(results, 1):
        enh = f"+{item.enhance_level}" if item.enhance_level > 0 else "-"
        dur = durability_gauge(item)
        extras = ", ".join(item.extra_options) if item.extra_options else "-"
        resist_str = ", ".join([f"{k}:{v}%" for k, v in item.resistances.items()]) if item.resistances else "-"

        print(f"{idx:<3} │ {item.name:<20} │ {item.rarity:<4} │ {enh:<4} │ {dur:<10} │ {item.attack:>4} │ {item.defense:>4} │ {extras:<20} │ {resist_str:<20}")

    print("─" * 110)