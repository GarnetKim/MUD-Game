import streamlit as st
from mudgame.skill import SKILLS

def codex_ui(player):
    st.title("📖 도감")

    tabs = st.tabs(["아이템 도감", "세트 도감", "스킬 도감"])

    # ------------------------
    # 아이템 도감
    # ------------------------
    with tabs[0]:
        st.subheader("🎒 아이템 도감")
        unlocked = len(player.codex["items"])
        # 전체 아이템은 아이템 시스템이 확장될 때 리스트 추가 가능
        total = unlocked  
        st.write(f"완성도: {unlocked}/{total}")
        for item in sorted(player.codex["items"]):
            st.write(f"✅ {item}")

    # ------------------------
    # 세트 도감
    # ------------------------
    with tabs[1]:
        st.subheader("⚔️ 세트 도감")
        unlocked = len(player.codex["sets"])
        total = unlocked  
        st.write(f"완성도: {unlocked}/{total}")
        for s in sorted(player.codex["sets"]):
            st.write(f"✅ {s}")

    # ------------------------
    # 스킬 도감
    # ------------------------
    with tabs[2]:
        st.subheader("✨ 스킬 도감")
        unlocked = len(player.codex["skills"])
        total = len(SKILLS)
        percent = int((unlocked / total) * 100)
        st.write(f"완성도: {unlocked}/{total} ({percent}%)")

        for name, info in SKILLS.items():
            if name in player.codex["skills"]:
                st.markdown(f"✅ **{name}** - {info['desc']} (MP: {info['mp']}, 쿨타임: {info['cooldown']}턴)")
            else:
                st.markdown(f"❌ **{name}** - ???")