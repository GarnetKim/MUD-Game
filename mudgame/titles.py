import streamlit as st

def titles_ui(player, log):
    st.subheader("🏅 칭호")

    for idx, title in enumerate(player.titles, 1):
        is_active = (player.active_title == title)
        label = f"{title} {'(활성화)' if is_active else ''}"
        if st.button(f"선택 {idx} - {label}"):
            player.active_title = title
            log(f"칭호 '{title}' 활성화!")

    if st.button("⬅️ 마을로 돌아가기"):
        st.session_state.titles_open = False