import streamlit as st

def codex_ui(player):
    st.subheader("📖 도감")

    st.write(f"아이템 도감: {len(player.codex['items'])} 개 해금")
    for name in sorted(player.codex["items"]):
        st.write(f"✅ {name}")

    st.write(f"스킬 도감: {len(player.codex['skills'])} 개 해금")
    for name in sorted(player.codex["skills"]):
        st.write(f"✅ {name}")

    st.write(f"세트 도감: {len(player.codex['sets'])} 개 해금")
    for name in sorted(player.codex["sets"]):
        st.write(f"✅ {name}")

    if st.button("⬅️ 마을로 돌아가기"):
        st.session_state.codex_open = False