import streamlit as st
from mudgame.battle import Monster, start_battle

def village_ui(player, log):
    st.subheader("🏘️ 마을")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button("⚔️ 전투 훈련"):
            monster = Monster("훈련용 허수아비", 30, 5, 2)
            st.session_state.battle_state = start_battle(player, monster, log)

    with col2:
        if st.button("🏪 상점"):
            st.session_state.shop_open = True

    with col3:
        if st.button("🛠️ 대장장이"):
            st.session_state.blacksmith_open = True

    with col4:
        if st.button("🏰 던전 입구"):
            st.session_state.location = "dungeon"

    with col5:
        if st.button("💬 NPC 대화"):
            log("👴 촌장: '던전에 보스가 나타났네. 조심하게.'")