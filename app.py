import streamlit as st
from player import Player
from battle import Monster, battle
from shop import shop_menu
from dungeon import Dungeon, explore_dungeon
from utils import show_inventory_table
from save_load import save_game, auto_load_latest

# ------------------------
# 세션 초기화
# ------------------------
if "player" not in st.session_state:
    st.session_state.player = Player("용사")
if "dungeon" not in st.session_state:
    st.session_state.dungeon = None
if "logs" not in st.session_state:
    st.session_state.logs = []

player = st.session_state.player
dungeon = st.session_state.dungeon
logs = st.session_state.logs

# ------------------------
# 출력 함수 (print 대신 logs에 기록)
# ------------------------
def log(msg):
    st.session_state.logs.append(msg)

# ------------------------
# UI 레이아웃
# ------------------------
st.title("🎮 텍스트 MUD RPG - Web Edition")
st.write("명령어 기반 RPG를 Streamlit에서 즐겨보세요!")

cmd = st.text_input("명령어 입력:", "")

if cmd:
    if cmd == "status":
        log(f"👤 {player.name} | Lv.{player.level} | HP {player.hp}/{player.max_hp} | MP {player.mp}/{player.max_mp} | Gold {player.gold}")
    elif cmd == "inv":
        inv_text = "\n".join([f"- {i.name} ({i.rarity})" for i in player.inventory]) or "비어있음"
        log("🎒 인벤토리:\n" + inv_text)
    elif cmd == "battle":
        m = Monster("고블린", 30, 8, 2, {"poison": 30})
        battle(player, m)  # battle() 안에 print 있으니 → 나중에 Streamlit용 wrapper 필요
        log("⚔️ 전투 시작!")
    elif cmd == "shop":
        log("🏪 상점 시스템은 웹 버전에서 UI 구현 필요")
    elif cmd == "dungeon":
        if not dungeon:
            st.session_state.dungeon = Dungeon(width=4, height=4, floor=1, max_floor=2)
        st.session_state.dungeon = explore_dungeon(player, st.session_state.dungeon)
        log("🏰 던전 탐험 진행 중...")
    elif cmd == "save":
        save_game(player)
        log("💾 게임 저장 완료")
    elif cmd == "quit":
        log("👋 게임 종료 (웹 세션은 계속 유지됨)")
    else:
        log(f"❌ 알 수 없는 명령어: {cmd}")

# ------------------------
# 출력 로그 표시
# ------------------------
st.subheader("📜 게임 로그")
st.text_area("Logs", value="\n".join(logs), height=400)