from item import Item

# ------------------------
# 상점 기본 재고
# ------------------------
SHOP_STOCK = {
    "해독제": {"price": 50, "stock": 5, "item": Item("해독제", "consumable", "일반", 0, 0)},
    "빙결해제제": {"price": 70, "stock": 5, "item": Item("빙결해제제", "consumable", "일반", 0, 0)},
    "화상치료제": {"price": 70, "stock": 5, "item": Item("화상치료제", "consumable", "일반", 0, 0)},
    "하이 포션": {"price": 120, "stock": 3, "item": Item("하이 포션", "consumable", "레어", 0, 0)},
    "만능 포션": {"price": 200, "stock": 2, "item": Item("만능 포션", "consumable", "전설", 0, 0)},
    "강화석": {"price": 150, "stock": 5, "item": Item("강화석", "material", "레어", 0, 0)},
}

# ------------------------
# 할인 시스템
# ------------------------
DISCOUNTS = {
    "daily": {"item": "해독제", "discount": 0.5},    # 하루 50% 할인
    "weekly": {"item": "강화석", "discount": 0.7},   # 주간 30% 할인
}


# ------------------------
# 가격 계산 (할인 반영)
# ------------------------
def get_price(item_name):
    if item_name not in SHOP_STOCK:
        return None
    base = SHOP_STOCK[item_name]["price"]

    # 할인 적용
    if DISCOUNTS["daily"]["item"] == item_name:
        return int(base * DISCOUNTS["daily"]["discount"])
    if DISCOUNTS["weekly"]["item"] == item_name:
        return int(base * DISCOUNTS["weekly"]["discount"])
    return base


# ------------------------
# 상점 메뉴
# ------------------------
def shop_menu(player):
    while True:
        print("\n🏪 [상점]")
        print("────────────────────────────")
        for idx, (name, data) in enumerate(SHOP_STOCK.items(), 1):
            price = get_price(name)
            stock = data["stock"]
            discount = ""
            if price < data["price"]:
                discount = " (할인!)"
            print(f"{idx}. {name} - {price} Gold [재고:{stock}]{discount}")
        print("────────────────────────────")
        print(f"보유 Gold: {player.gold}")
        print("명령어: buy <번호> / sell <번호> / exit")
        cmd = input("> ").strip()

        if cmd == "exit":
            break
        elif cmd.startswith("buy"):
            parts = cmd.split()
            if len(parts) < 2: 
                print("⚠️ 구매할 번호를 입력하세요")
                continue
            idx = int(parts[1]) - 1
            if idx < 0 or idx >= len(SHOP_STOCK):
                print("❌ 잘못된 번호")
                continue
            item_name = list(SHOP_STOCK.keys())[idx]
            buy_item(player, item_name)
        elif cmd.startswith("sell"):
            if not player.inventory:
                print("❌ 판매할 아이템이 없습니다.")
                continue
            print("\n🎒 [판매 가능한 아이템]")
            for i, item in enumerate(player.inventory, 1):
                print(f"{i}. {item.short_name()} (희귀도:{item.rarity})")
            parts = cmd.split()
            if len(parts) < 2:
                print("⚠️ 판매할 번호를 입력하세요")
                continue
            idx = int(parts[1]) - 1
            if idx < 0 or idx >= len(player.inventory):
                print("❌ 잘못된 번호")
                continue
            item = player.inventory[idx]
            sell_item(player, item)
        else:
            print("❌ 알 수 없는 명령어")


# ------------------------
# 구매 처리
# ------------------------
def buy_item(player, item_name):
    if item_name not in SHOP_STOCK:
        print("❌ 상점에 없는 아이템")
        return
    stock_data = SHOP_STOCK[item_name]
    if stock_data["stock"] <= 0:
        print("❌ 재고가 없습니다.")
        return
    price = get_price(item_name)
    if player.gold < price:
        print("❌ Gold가 부족합니다.")
        return
    # 구매 성공
    player.gold -= price
    stock_data["stock"] -= 1
    item = stock_data["item"]
    # 복제본 새로 추가
    bought = Item(item.name, item.type, item.rarity, item.attack, item.defense, item.resistances.copy())
    player.inventory.append(bought)
    print(f"🛒 {item_name} 구매 완료! (-{price} Gold)")


# ------------------------
# 판매 처리
# ------------------------
def sell_item(player, item):
    # 판매 가격 = 기본 가격의 절반
    base = SHOP_STOCK.get(item.name, {"price": 50})["price"]
    price = int(base * 0.5)
    player.gold += price
    player.inventory.remove(item)
    print(f"💰 {item.short_name()} 판매 완료! (+{price} Gold)")