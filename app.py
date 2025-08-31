import streamlit as st
from mudgame.player import Player
from mudgame.save_load import auto_load_latest
from mudgame.battle import Monster, start_battle, battle_turn
from mudgame.village import village_ui
from mudgame.shop import shop_ui
from mudgame.blacksmith import blacksmith_ui
from mudgame.codex import codex_ui
from mudgame.titles import titles_ui
from mudgame.dungeon import explore_room

# 세션 초기화
for k, v in {
    "player": None, "logs": [], "initialized": False,
    "battle_state": None, "shop_open": False,
    "blacksmith_open": False, "codex_open": False, "titles_open": False,
    "location": "village"
}.items():
    if k not in st.session_state: st.session_state[k] = v

logs = st.session_state.logs
def log(msg): logs.append(msg)

# 시작 메뉴
if not st.session_state.initialized:
    st.title("🎮 Garnet Story - 시작 메뉴")
    player_name = st.text_input("플레이어 이름:", "용사")
    option = st.radio("게임 시작 옵션", ["새 게임", "이어하기"], index=0)
    if st.button("게임 시작"):
        if option == "새 게임":
            st.session_state.player = Player(player_name)
            logs[:] = [f"✨ 새로운 모험이 시작됩니다! {player_name}님!"]
        else:
            player = auto_load_latest()
            if player:
                st.session_state.player = player
                logs[:] = ["📂 세이브 불러오기 성공!"]
            else:
                st.session_state.player = Player(player_name)
                logs[:] = ["⚠️ 세이브 없음, 새 게임 시작!"]

        st.session_state.initialized = True
        st.session_state.location = "village"

# 게임 루프
else:
    st.title("🎮 Garnet Story - Web Edition")
    p = st.session_state.player

    if st.session_state.battle_state and st.session_state.battle_state["in_battle"]:
        st.subheader(f"⚔️ {st.session_state.battle_state['monster'].name} 전투 중")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🗡️ 공격"):
                st.session_state.battle_state = battle_turn(p, st.session_state.battle_state, "attack", log)
        with col2:
            if st.button("🔥 스킬"):
                st.session_state.battle_state = battle_turn(p, st.session_state.battle_state, "skill", log)
        with col3:
            if st.button("🏃 도망"):
                st.session_state.battle_state = battle_turn(p, st.session_state.battle_state, "run", log)

    elif st.session_state.shop_open:
        shop_ui(p, log)

    elif st.session_state.blacksmith_open:
        blacksmith_ui(p, log)

    elif st.session_state.codex_open:
        codex_ui(p)

    elif st.session_state.titles_open:
        titles_ui(p, log)

    elif st.session_state.location == "dungeon":
        result, obj = explore_room(p, log)
        if result == "battle":
            st.session_state.battle_state = start_battle(p, obj, log)
        elif result == "merchant":
            st.session_state.shop_open = True
        if st.button("⬅️ 마을로 돌아가기"):
            st.session_state.location = "village"

    elif st.session_state.location == "village":
        village_ui(p, log)

    st.subheader("📜 게임 로그")
    st.text_area("Logs", value="\n".join(logs), height=400)