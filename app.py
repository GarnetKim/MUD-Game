import streamlit as st
from mudgame.player import Player
from mudgame.save_load import auto_load_latest
from mudgame.battle import Monster, start_battle, battle_turn
from mudgame.village import village_ui
from mudgame.shop_ui import shop_ui
from mudgame.blacksmith_ui import blacksmith_ui
from mudgame.codex import codex_ui
from mudgame.titles import titles_ui
from mudgame.dungeon import explore_room
from mudgame.skill import SKILLS, unlock_skill

# 세션 초기화
for k, v in {
    "player": None, "logs": [], "initialized": False,
    "battle_state": None, "shop_open": False,
    "blacksmith_open": False, "codex_open": False, "titles_open": False,
    "location": "village", "skill_choice_open": False
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

    # ✅ 상태 게이지 출력
    st.subheader("📊 상태")
    st.progress(p.hp / p.max_hp, text=f"❤️ HP {p.hp}/{p.max_hp}")
    st.progress(p.mp / p.max_mp, text=f"🔮 MP {p.mp}/{p.max_mp}")

    # ------------------------
    # 전투 UI
    # ------------------------
    if st.session_state.battle_state and st.session_state.battle_state["in_battle"]:
        # 🧪 아이템 사용
        st.markdown("---")
        st.subheader("🧪 아이템 사용")

        consumables = [i for i in p.inventory if i.type == "consumable"]
        if not consumables:
            st.write("❌ 사용할 수 있는 아이템 없음")
        else:
            for item in consumables:
                col1, col2 = st.columns([2, 1])
                with col1:
                    count = st.number_input(
                        f"{item.name} 개수", 
                        min_value=1, 
                        max_value=p.inventory.count(item), 
                        value=1, 
                        key=f"use_{item.name}"
                    )
                with col2:
                    if st.button(f"{item.name} 사용", key=f"btn_{item.name}"):
                        if p.use_item(item.name, count=count, log=log):
                            st.success(f"{item.name} 사용 완료!")   # ✅ 사용 완료 메시지
                            st.experimental_rerun()                # ✅ 바로 게이지 반영

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
       
        # ✅ 전투 중 상태 게이지
        st.subheader("📊 상태")
        st.progress(p.hp / p.max_hp, text=f"❤️ HP {p.hp}/{p.max_hp}")
        st.progress(p.mp / p.max_mp, text=f"🔮 MP {p.mp}/{p.max_mp}")

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

    # ------------------------
    # 스킬 선택 UI (레벨업 시)
    # ------------------------
    if st.session_state.skill_choice_open:
        st.subheader("✨ 새로운 스킬을 선택하세요!")
        choices = [s for s in SKILLS.keys() if s not in p.skills]  # 아직 배우지 않은 스킬
        if not choices:
            st.write("모든 스킬을 이미 배웠습니다!")
            st.session_state.skill_choice_open = False
        else:
            for idx, skill in enumerate(choices, 1):
                info = SKILLS[skill]
                st.markdown(f"**{idx}. {skill}**  \n💡 {info['desc']}  \n🔹 MP 소모: {info['mp']}")
                if st.button(f"{skill} 배우기"):
                    unlock_skill(p, skill, log=log)  # ✅ skill.py의 unlock_skill 사용
                    st.session_state.skill_choice_open = False

    # ------------------------
    # 로그 출력
    # ------------------------
    st.subheader("📜 게임 로그")

    filter_option = st.radio(
        "로그 필터",
        ["전체", "전투", "아이템", "골드"],
        horizontal=True
    )

    recent_logs = logs[-50:]

    if filter_option == "전투":
        filtered_logs = [l for l in recent_logs if "⚔️" in l or "🗡️" in l or "🔥" in l or "💥" in l or "🎉" in l]
    elif filter_option == "아이템":
        filtered_logs = [l for l in recent_logs if "🎁" in l or "🛒" in l]
    elif filter_option == "골드":
        filtered_logs = [l for l in recent_logs if "💰" in l]
    else:
        filtered_logs = recent_logs

    st.text_area("Logs", value="\n".join(reversed(filtered_logs)), height=400)