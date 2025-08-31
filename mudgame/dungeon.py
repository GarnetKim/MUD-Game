import random
from mudgame.battle import Monster, battle
from mudgame.shop import shop_menu
from mudgame.item import Item
from mudgame.utils import show_inventory_table

# ------------------------
# 방(Room) 클래스
# ------------------------
class Room:
    def __init__(self, x, y, is_boss=False):
        self.x = x
        self.y = y
        self.visited = False
        self.is_boss = is_boss
        self.event = None  # treasure, trap, merchant, monster


# ------------------------
# 던전 클래스
# ------------------------
class Dungeon:
    def __init__(self, width=4, height=4, floor=1, max_floor=3):
        self.width = width
        self.height = height
        self.floor = floor
        self.max_floor = max_floor
        self.rooms = [[Room(x, y) for y in range(height)] for x in range(width)]
        self.current_pos = (0, 0)
        self.generate_events()

    def current_room(self):
        x, y = self.current_pos
        return self.rooms[x][y]

    def generate_events(self):
        """랜덤 이벤트 배치"""
        for row in self.rooms:
            for room in row:
                roll = random.randint(1, 100)
                if roll <= 15:
                    room.event = "treasure"
                elif roll <= 30:
                    room.event = "trap"
                elif roll <= 40:
                    room.event = "merchant"
                elif roll <= 70:
                    room.event = "monster"
        # 마지막 방 = 보스
        self.rooms[-1][-1].is_boss = True
        self.rooms[-1][-1].event = "boss"

    def display_minimap(self):
        print("\n🗺️ [던전 미니맵]")
        for y in range(self.height):
            row = []
            for x in range(self.width):
                room = self.rooms[x][y]
                if (x, y) == self.current_pos:
                    marker = "🙂"
                elif not room.visited:
                    marker = "⬛"
                elif room.is_boss:
                    marker = "👹"
                else:
                    marker = "⬜"
                row.append(marker)
            print(" ".join(row))
        print("")


# ------------------------
# 던전 탐험
# ------------------------
def explore_dungeon(player, dungeon: Dungeon):
    print(f"\n🏰 {dungeon.floor}층 던전 탐험을 시작합니다!")
    while True:
        dungeon.display_minimap()
        room = dungeon.current_room()
        if not room.visited:
            trigger_event(player, room)
            room.visited = True
            if room.is_boss and room.event == "boss":
                print("🎉 보스를 처치하고 층을 클리어했습니다!")
                if dungeon.floor < dungeon.max_floor:
                    print("⬇️ 다음 층으로 이동합니다!")
                    return Dungeon(width=dungeon.width, height=dungeon.height,
                                   floor=dungeon.floor+1, max_floor=dungeon.max_floor)
                else:
                    print("🏆 모든 층 클리어! 던전을 정복했습니다!")
                    return None

        cmd = input("이동 (w/a/s/d) / exit: ").strip()
        x, y = dungeon.current_pos
        if cmd == "w" and y > 0:
            dungeon.current_pos = (x, y-1)
        elif cmd == "s" and y < dungeon.height-1:
            dungeon.current_pos = (x, y+1)
        elif cmd == "a" and x > 0:
            dungeon.current_pos = (x-1, y)
        elif cmd == "d" and x < dungeon.width-1:
            dungeon.current_pos = (x+1, y)
        elif cmd == "exit":
            print("👉 던전 탐험을 중단했습니다.")
            return None
        else:
            print("❌ 잘못된 입력")


# ------------------------
# 이벤트 처리
# ------------------------
def trigger_event(player, room: Room):
    if room.event == "treasure":
        print("💎 보물상자를 발견했습니다!")
        loot = generate_loot()
        player.inventory.append(loot)
        print(f"📦 획득: {loot.name} ({loot.rarity})")
    elif room.event == "trap":
        print("☠️ 함정 발동! HP -10")
        player.hp = max(0, player.hp - 10)
    elif room.event == "merchant":
        print("🧑‍💼 떠돌이 상인을 만났습니다.")
        shop_menu(player)
    elif room.event == "monster":
        print("👹 몬스터가 나타났습니다!")
        m = Monster("던전 몬스터", 20, 5, 2, exp_reward=15, gold_reward=10)
        battle(player, m)
    elif room.event == "boss":
        print("👹 보스 등장! [던전 보스]")
        m = Monster("던전 보스", 80, 12, 5, exp_reward=100, gold_reward=50, is_boss=True)
        battle(player, m)


# ------------------------
# 보물상자 드랍
# ------------------------
def generate_loot():
    roll = random.randint(1, 100)
    if roll <= 60:
        return Item("낡은 검", "weapon", "일반", 5, 0)
    elif roll <= 85:
        return Item("강철 방패", "armor", "레어", 0, 10)
    else:
        loot = Item("용의 검", "weapon", "전설", 20, 5)
        loot.extra_options.append("치명타 확률 +5%")
        return loot