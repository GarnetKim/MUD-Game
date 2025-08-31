import streamlit as st
from mudgame.player import Player
from mudgame.battle import Monster
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
    logs.append(msg)

# ------------------------
# 시작 메뉴
# ------------------------
if not st.session_state.initialized:
    st.title("🎮 Garnet Story - 시작 메뉴")
    st.subheader("모험을 시작하기 전에 선택하세요!")

    # 이름 입력
    player_name = st.text_input("플레이어 이름을 입력하세요:", "용사")

    # 새 게임 / 이어하기
    option = st.radio("게임 시작 옵션", ["새 게임", "이어하기"], index=0)

    if st.button("게임 시작"):
        if option == "새 게임":
            st.session_state.player = Player(player_name if player_name else "용사")
            st.session_state.logs = [f"✨ 새로운 모험이 시작됩니다! 환영합니다, {player_name}님!"]
        else:
            player = auto_load_latest()
            if player:
                st.session_state.player = player
                st.session_state.logs = ["📂 최근 세이브를 불러왔습니다!"]
            else:
                st.session_state.player = Player(player_name if player_name else "용사")
                st.session_state.logs = ["⚠️ 세이브가 없어 새 게임으로 시작합니다."]

        # 상태 요약
        p = st.session_state.player
        log(f"👤 {p.name} | Lv.{p.level} | HP {p.hp}/{p.max_hp} | MP {p.mp}/{p.max_mp} | Gold {p.gold}")
        st.session_state.initialized = True

# ------------------------
# 메인 게임 루프
# ------------------------
if st.session_state.initialized:
    st.title("🎮 Garnet Story - Web Edition")
    p = st.session_state.player

    if "battle_state" not in st.session_state:
        st.session_state.battle_state = None
    if "shop_open" not in st.session_state:
        st.session_state.shop_open = False

    # 전투 중일 때
    if st.session_state.battle_state and st.session_state.battle_state["in_battle"]:
        ...
        # (전투 버튼 부분 그대로)

    # 상점 열려있을 때
    elif st.session_state.shop_open:
        st.subheader("🏪 상점")

        items = get_shop_items()
        for i, item in enumerate(items):
            col1, col2, col3 = st.columns([3,1,1])
            with col1:
                st.write(f"{item.name} ({item.rarity}) - 💰 {item.price} Gold")
            with col2:
                if st.button(f"구매 {i}"):
                    if p.gold >= item.price:
                        p.gold -= item.price
                        p.inventory.append(item)
                        log(f"🛒 {item.name} 구매 완료! (남은 골드: {p.gold})")
                    else:
                        log("⚠️ 골드가 부족합니다!")
            with col3:
                if item in p.inventory and st.button(f"판매 {i}"):
                    p.gold += int(item.price * 0.5)
                    p.inventory.remove(item)
                    log(f"💰 {item.name} 판매 완료! (보유 골드: {p.gold})")

        if st.button("⬅️ 상점 나가기"):
            st.session_state.shop_open = False

    # 기본 메뉴
    else:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("📜 상태 확인"):
                log(f"👤 {p.name} | Lv.{p.level} | HP {p.hp}/{p.max_hp} | Gold {p.gold}")

        with col2:
            if st.button("⚔️ 전투 시작"):
                m = Monster("고블린", 30, 8, 2)
                st.session_state.battle_state = start_battle(p, m, log)

        with col3:
            if st.button("🏪 상점"):
                st.session_state.shop_open = True
                log("🏪 상점에 입장했습니다!")

        with col4:
            if st.button("🏰 던전 탐험"):
                log("던전 탐험 시스템은 준비 중입니다!")

    # 로그 출력
    st.subheader("📜 게임 로그")
    st.text_area("Logs", value="\n".join(logs), height=400)