from player import Player, show_player_summary
from save_load import auto_load_latest

def start_game():
    player = auto_load_latest()
    if player:
        show_player_summary(player)
        print("🎮 [메뉴 선택]\n1. 계속하기\n2. 새 게임")
        c=input("> ")
        if c=="2":
            name=input("플레이어 이름: ")
            player=Player(name)
            print("✨ 새로운 모험 시작!")
    else:
        name=input("플레이어 이름: ")
        player=Player(name)
        print("✨ 새로운 모험 시작!")
    return player

if __name__=="__main__":
    p=start_game()