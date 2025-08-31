import streamlit as st
from mudgame.blacksmith import repair_item, upgrade_item

def blacksmith_ui(player, log):
    st.subheader("🛠️ 대장장이")

    st.write("수리 가능한 장비:")
    for i, item in enumerate([it for it in player.inventory if it.type in ["weapon", "armor"]], 1):
        st.write(f"{i}. {item.display_name()} - 내구도 {item.durability}/{item.max_durability}")
        c1, c2 = st.columns(2)
        with c1:
            if st.button(f"수리 {i}"):
                repair_item(item, player, log)
        with c2:
            if st.button(f"강화 {i}"):
                upgrade_item(item, player, log)

    if st.button("⬅️ 마을로 돌아가기"):
        st.session_state.blacksmith_open = False