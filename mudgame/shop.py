# mudgame/shop.py
from mudgame.item import Item

# 샘플 아이템 (실제 프로젝트에서는 아이템 풀과 드랍 테이블을 연결)
SHOP_ITEMS = [
    Item("체력 포션", "consumable", rarity="common", heal=20, price=10),
    Item("마나 포션", "consumable", rarity="common", mp_restore=15, price=12),
    Item("철검", "weapon", atk=5, rarity="rare", price=50),
    Item("가죽 갑옷", "armor", defense=3, rarity="rare", price=45),
]

def get_shop_items():
    return SHOP_ITEMS