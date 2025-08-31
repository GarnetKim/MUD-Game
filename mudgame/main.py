from player import Player, show_player_summary
from utils import show_inventory_table
from save_load import auto_load_latest, save_game
from item import Item

def start_game():
    player = auto_load_latest()
    if not player:
        name = input("플레이어 이름을 입력하세요: ")
        player = Player(name)
        print(f"✨ 새로운 모험이 시작됩니다! 환영합니다, {player.name}님!")

    return player

def main_loop(player):
    while True:
        cmd = input("> ").strip()
        if cmd == "status":
            show_player_summary(player)
        elif cmd.startswith("inv"):
            if cmd == "inv":
                show_inventory_table(player, "all")
            elif cmd == "inv 무기":
                show_inventory_table(player, "weapon")
            elif cmd == "inv 방어구":
                show_inventory_table(player, "armor")
            elif cmd == "inv 소비":
                show_inventory_table(player, "consumable")
        elif cmd == "save":
            save_game(player)
        elif cmd == "quit":
            print("👋 게임을 종료합니다.")
            break
        else:
            print("❌ 알 수 없는 명령어 (status, inv, save, quit)")

if __name__ == "__main__":
    p = start_game()

    # 테스트용: 인벤토리에 아이템 몇 개 추가
    p.inventory.append(Item("불꽃 검", "weapon", "전설", 50, 0, {"burn": 20}))
    p.inventory[-1].enhance_level = 5
    p.inventory[-1].durability = 65
    p.inventory[-1].max_durability = 100
    p.inventory[-1].extra_options.append("치명타 +5%")

    p.inventory.append(Item("화염 방패 갑옷", "armor", "레어", 0, 25, {"burn": 40, "poison": 20}))
    p.inventory[-1].enhance_level = 3
    p.inventory[-1].durability = 10
    p.inventory[-1].max_durability = 80
    p.inventory[-1].extra_options.append("피해 감소 +10%")

    p.inventory.append(Item("해독제", "consumable", "일반", 0, 0))

    main_loop(p)