import streamlit as st
from mudgame.player import Player
from mudgame.save_load import auto_load_latest

# ------------------------
# 세션 초기화
# ------------------------
if "player" not in st.session_state:
    st.session_state.player = None
if "logs" not in st.session_state:
    st.session_state.logs = []
if "initialized" not in st.session_state:
    st.session_state.initialized = False

logs = st.session_state.logs

def log(msg: str):
    """Streamlit 로그 기록"""
    logs.append(msg)

# ------------------------
# 시작 메뉴 (게임 미시작 상태)
# ------------------------
if not st.session_state.initialized:
    st.title("🎮 Garnet story - Web Edition")
    st.subheader("모험을 시작하기 전에 선택하세요!")

    # 이름 입력
    player_name = st.text_input("플레이어 이름을 입력하세요:", "용사")

    # 새 게임 / 이어하기 옵션
    option = st.radio("게임 시작 옵션", ["새 게임", "이어하기"], index=0)

    if st.button("게임 시작"):
        if option == "새 게임":
            st.session_state.player = Player(player_name if player_name else "용사")
            log(f"✨ 새로운 모험이 시작됩니다! 환영합니다, {player_name}님!")
        else:
            player = auto_load_latest()
            if player:
                st.session_state.player = player
                log("📂 최근 세이브를 불러왔습니다!")
            else:
                st.session_state.player = Player(player_name if player_name else "용사")
                log("⚠️ 세이브가 없어 새 게임으로 시작합니다.")

        # 상태 요약 자동 출력
        p = st.session_state.player
        log(f"👤 {p.name} | Lv.{p.level} | HP {p.hp}/{p.max_hp} | MP {p.mp}/{p.max_mp} | Gold {p.gold}")

        st.session_state.initialized = True
        st.rerun()

# ------------------------
# 메인 게임 루프 (게임 시작 후)
# ------------------------
else:
    st.title("🎮 Garnet story - Web Edition")
    cmd = st.text_input("명령어 입력:", "")

    if cmd:
        p = st.session_state.player
        if cmd == "status":
            log(f"👤 {p.name} | Lv.{p.level} | HP {p.hp}/{p.max_hp} | MP {p.mp}/{p.max_mp} | Gold {p.gold}")
        elif cmd == "inv":
            inv_text = "\n".join([f"- {i.name} ({i.rarity})" for i in p.inventory]) or "비어있음"
            log("🎒 인벤토리:\n" + inv_text)
        elif cmd == "battle":
            log("⚔️ 전투 시스템은 웹 로그 전용으로 리팩터링 필요")
        elif cmd == "shop":
            log("🏪 상점 시스템은 웹 UI 구현 필요")
        elif cmd == "dungeon":
            log("🏰 던전 시스템은 웹 UI 구현 필요")
        else:
            log(f"❌ 알 수 없는 명령어: {cmd}")

    st.subheader("📜 게임 로그")
    st.text_area("Logs", value="\n".join(logs), height=400)