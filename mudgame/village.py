import streamlit as st

def village_ui(player, log):
    st.subheader("🏘️ 마을")
    st.write("따뜻한 마을입니다. 어디로 가시겠습니까?")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏰 던전 탐험"):
            st.session_state.location = "dungeon"
            log("🏰 던전으로 향합니다!")
    with col2:
        if st.button("🏪 상점"):
            st.session_state.shop_open = True
            log("🛒 상점에 들어갑니다.")
    with col3:
        if st.button("⚒️ 대장장이"):
            st.session_state.blacksmith_open = True
            log("⚒️ 대장장이를 만났습니다.")

    col4, col5, col6 = st.columns(3)
    with col4:
        if st.button("📖 도감"):
            st.session_state.codex_open = True
            log("📖 도감을 펼쳤습니다.")
    with col5:
        if st.button("🏆 칭호 관리"):
            st.session_state.titles_open = True
            log("🏆 칭호를 확인합니다.")
    with col6:
        if st.button("🛏️ 휴식"):
            player.hp = player.max_hp
            player.mp = player.max_mp
            log("🛏️ 여관에서 휴식! HP/MP가 모두 회복되었습니다.")