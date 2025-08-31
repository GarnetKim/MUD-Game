from player import Player, show_player_summary
from utils import show_inventory_table, sort_inventory, filter_inventory
from save_load import auto_load_latest, save_game, choose_save_slot
from battle import battle, Monster
from dungeon import Dungeon, explore_dungeon
from shop import shop_menu
from skill import unlock_skill, show_skill_codex, use_skill, tick_cooldowns
from titles import unlock_title, activate_title, deactivate_title, show_titles, apply_title_effects
from sets import apply_set_bonus, show_set_codex, check_codex_completion
from log_system import search_logs, export_logs_to_csv, paginate_logs, monitor_logs

# ------------------------
# 게임 시작
# ------------------------
def start_game():
    print("🎮 텍스트 MUD RPG 에 오신 걸 환영합니다!")
    choice = input("👉 자동 로드 하시겠습니까? (Y/n): ").strip().lower()
    if choice == "n":
        player = choose_save_slot()
        if not player:
            name = input("플레이어 이름을 입력하세요: ")
            player = Player(name)
            print(f"✨ 새로운 모험이 시작됩니다! 환영합니다, {player.name}님!")
    else:
        player = auto_load_latest()
        if not player:
            name = input("플레이어 이름을 입력하세요: ")
            player = Player(name)
            print(f"✨ 새로운 모험이 시작됩니다! 환영합니다, {player.name}님!")
    return player

# ------------------------
# 명령어 처리
# ------------------------
def handle_command(player, cmd: str, dungeon: Dungeon):
    if cmd == "status":
        show_player_summary(player)

    elif cmd == "inv":
        show_inventory_table(player, "all")
    elif cmd.startswith("inv "):
        parts = cmd.split()
        if parts[1] in ["무기","weapon"]:
            show_inventory_table(player, "weapon")
        elif parts[1] in ["방어구","armor"]:
            show_inventory_table(player, "armor")
        elif parts[1] in ["소비","consumable"]:
            show_inventory_table(player, "consumable")
        elif parts[1] == "검색" and len(parts) >= 3:
            keyword = parts[2]
            filter_inventory(player, keyword)
        elif parts[1] == "정렬" and len(parts) >= 3:
            sort_inventory(player, parts[2])
        else:
            print("❌ 잘못된 inv 옵션")

    elif cmd == "battle":
        m = Monster("고블린", 30, 8, 2, {"poison": 30})
        battle(player, m)

    elif cmd == "dungeon":
        if not dungeon:
            dungeon = Dungeon(width=4, height=4, floor=1, max_floor=3)
        dungeon = explore_dungeon(player, dungeon)

    elif cmd == "shop":
        shop_menu(player)

    elif cmd.startswith("skill"):
        parts = cmd.split()
        if len(parts) == 2 and parts[1] == "codex":
            show_skill_codex(player)
        elif len(parts) >= 2:
            skill_name = parts[1]
            use_skill(player, skill_name, None)
        else:
            print("❌ 사용법: skill <이름> / skill codex")

    elif cmd.startswith("title"):
        parts = cmd.split()
        if len(parts) == 2 and parts[1] == "list":
            show_titles(player)
        elif len(parts) == 3 and parts[1] == "unlock":
            unlock_title(player, parts[2])
        elif len(parts) == 3 and parts[1] == "activate":
            activate_title(player, parts[2])
        elif len(parts) == 2 and parts[1] == "deactivate":
            deactivate_title(player)
        else:
            print("❌ 사용법: title list/unlock/activate/deactivate")

    elif cmd == "setcodex":
        show_set_codex(player)

    elif cmd.startswith("log "):
        parts = cmd.split()
        if parts[1] == "search":
            keywords = parts[2:]
            search_logs(keywords)
        elif parts[1] == "csv":
            export_logs_to_csv()
        elif parts[1] == "page":
            paginate_logs()
        elif parts[1] == "monitor":
            monitor_logs()
        else:
            print("❌ 사용법: log search/csv/page/monitor")

    elif cmd == "save":
        save_game(player)

    elif cmd == "quit":
        print("👋 게임을 종료합니다.")
        return False, dungeon

    else:
        print("❌ 알 수 없는 명령어")

    return True, dungeon

# ------------------------
# 메인 루프
# ------------------------
def main_loop(player):
    dungeon = None
    while True:
        cmd = input("> ").strip()
        tick_cooldowns(player)  # 턴마다 스킬 쿨타임 감소
        apply_title_effects(player)  # 칭호 효과 적용
        apply_set_bonus(player)      # 세트 효과 적용
        check_codex_completion(player) # 세트 도감 완성 보상
        cont, dungeon = handle_command(player, cmd, dungeon)
        if not cont:
            break

# ------------------------
# 실행
# ------------------------
if __name__ == "__main__":
    p = start_game()
    main_loop(p)