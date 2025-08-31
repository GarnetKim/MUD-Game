from item import Item
from utils import format_item

class Player:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.exp = 0
        self.exp_to_next = 100
        self.hp = 100
        self.max_hp = 100
        self.mp = 50
        self.max_mp = 50
        self.atk = 10
        self.defense = 5
        self.gold = 100

        self.weapon = None
        self.armor = None
        self.inventory = []

        # 상태이상
        self.status_effects = []

        # 칭호 시스템
        self.titles = []
        self.active_title = None
        self.autoload_enabled = True

    def equip(self, item: Item):
        if item.type == "weapon":
            self.weapon = item
        elif item.type == "armor":
            self.armor = item

def show_player_summary(player):
    print("\n──────── [플레이어 상태 요약] ────────")
    print(f"👤 이름: {player.name}")
    print(f"⭐ 레벨: {player.level}")
    print(f"❤️ HP: {player.hp}/{player.max_hp}")
    print(f"🔮 MP: {player.mp}/{player.max_mp}")
    print(f"💰 골드: {player.gold}")
    print(f"🗡 무기: {format_item(player.weapon) if player.weapon else '없음'}")
    print(f"🛡 방어구: {format_item(player.armor) if player.armor else '없음'}")
    print("────────────────────────────────────\n")