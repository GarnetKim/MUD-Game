from item import Item

def durability_gauge(item: Item) -> str:
    if not item: return ""
    ratio = item.durability / item.max_durability if item.max_durability else 0
    if ratio > 0.6:
        icon = "🟩"
    elif ratio > 0.3:
        icon = "🟨"
    else:
        icon = "🟥"
    return f"{icon}{item.durability}/{item.max_durability}"


def show_inventory_table(player):
    if not player.inventory:
        print("🎒 인벤토리: 비어 있음")
        return

    # 표 헤더
    print("\n🎒 [인벤토리]")
    print("─"*100)
    print(f"{'No':<3} │ {'이름':<20} │ {'희귀도':<4} │ {'강화':<3} │ {'내구도':<8} │ {'ATK':>4} │ {'DEF':>4} │ {'옵션':<20} │ {'내성':<20}")
    print("─"*100)

    # 아이템 목록
    for idx, item in enumerate(player.inventory, 1):
        enh = f"+{item.enhance_level}" if item.enhance_level > 0 else "-"
        dur = durability_gauge(item)
        extras = ", ".join(item.extra_options) if item.extra_options else "-"
        resist_str = ", ".join([f"{k}:{v}%" for k,v in item.resistances.items()]) if item.resistances else "-"

        print(f"{idx:<3} │ {item.name:<20} │ {item.rarity:<4} │ {enh:<3} │ {dur:<8} │ {item.attack:>4} │ {item.defense:>4} │ {extras:<20} │ {resist_str:<20}")

    print("─"*100)