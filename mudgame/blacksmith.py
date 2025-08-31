import random

def repair_item(item, player, log):
    cost = int(item.max_durability * 0.2)
    if player.gold < cost:
        return "❌ Gold 부족"
    player.gold -= cost
    item.durability = item.max_durability
    log(f"🛠️ {item.display_name()} 내구도 완전 회복! (-{cost} Gold)")
    return None

def upgrade_item(item, player, log):
    if not any(i.name == "강화석" for i in player.inventory):
        return "❌ 강화석이 없습니다."
    stone = next(i for i in player.inventory if i.name == "강화석")
    player.inventory.remove(stone)

    success_rate = 0.7 if item.rarity == "레어" else 0.5 if item.rarity == "전설" else 0.9
    if random.random() < success_rate:
        item.upgrade_level += 1
        item.attack += 1 if item.type == "weapon" else 0
        item.defense += 1 if item.type == "armor" else 0
        log(f"✨ 강화 성공! {item.display_name()} → +{item.upgrade_level}")
    else:
        if random.random() < 0.3:  # 파괴 확률
            log(f"💥 강화 실패! {item.display_name()} 파괴됨!")
            player.inventory.remove(item)
        else:
            log(f"⚠️ 강화 실패! {item.display_name()} 변화 없음.")
    return None