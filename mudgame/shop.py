from mudgame.item import Item

SHOP_STOCK = {
    "체력 포션": {"price": 10, "stock": 5, "item": Item("체력 포션", "consumable", "일반", heal=20)},
    "마나 포션": {"price": 12, "stock": 5, "item": Item("마나 포션", "consumable", "일반", mp_restore=15)},
    "하이 포션": {"price": 50, "stock": 2, "item": Item("하이 포션", "consumable", "레어", heal=50, mp_restore=20)},
    "철검": {"price": 100, "stock": 2, "item": Item("철검", "weapon", "레어", attack=10, durability=120)},
    "가죽 갑옷": {"price": 90, "stock": 2, "item": Item("가죽 갑옷", "armor", "레어", defense=8, durability=120)},
    "강화석": {"price": 150, "stock": 3, "item": Item("강화석", "material", "레어")},
}

def get_price(item_name):
    return SHOP_STOCK[item_name]["price"]

def buy_item(player, item_name):
    if item_name not in SHOP_STOCK: return "❌ 없는 아이템"
    stock = SHOP_STOCK[item_name]
    if stock["stock"] <= 0: return "❌ 재고 없음"
    if player.gold < stock["price"]: return "❌ Gold 부족"
    player.gold -= stock["price"]
    stock["stock"] -= 1
    bought = stock["item"]
    player.add_item(bought, log)
    if log:
        log(f"🛒 {bought.display_name()} 구매 완료! (-{stock['price']} Gold)")
    return None

def sell_item(player, item, log=None):
    price = int(item.price * 0.5) if item.price else 5
    player.gold += price
    player.inventory.remove(item)
    if log:
        log(f"💰 {item.display_name()} 판매 완료! (+{price} Gold)")
    return None