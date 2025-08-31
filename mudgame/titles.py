from mudgame.log_system import log_event

# ------------------------
# 칭호 정의
# ------------------------
TITLES = {
    "초보 모험가": {"atk": 1, "def": 1, "desc": "모험의 시작을 알리는 칭호"},
    "용사": {"atk": 5, "def": 2, "desc": "전설의 모험가에게 부여되는 칭호"},
    "마법사": {"mp": 20, "desc": "마나 친화력 +20"},
    "용학살자": {"atk": 15, "def": 5, "skill": "dragon_slayer", "desc": "드래곤에게 강한 궁극기 부여"},
}

# ------------------------
# 칭호 획득
# ------------------------
def unlock_title(player, title_name):
    if title_name not in TITLES:
        print("❌ 알 수 없는 칭호")
        return
    if title_name not in player.titles:
        player.titles.append(title_name)
        print(f"🏆 새로운 칭호 획득: {title_name}")
        log_event(player, f"[칭호 획득] {title_name}")
    else:
        print("이미 보유한 칭호입니다.")


# ------------------------
# 칭호 활성화
# ------------------------
def activate_title(player, title_name):
    if title_name not in player.titles:
        print("❌ 아직 보유하지 않은 칭호")
        return
    player.active_title = title_name
    print(f"👉 칭호 활성화: {title_name}")
    log_event(player, f"[칭호 활성화] {title_name}")


# ------------------------
# 칭호 효과 적용
# ------------------------
def apply_title_effects(player):
    if not player.active_title:
        return
    effect = TITLES.get(player.active_title, {})
    if "atk" in effect:
        player.atk += effect["atk"]
    if "def" in effect:
        player.defense += effect["def"]
    if "mp" in effect:
        player.max_mp += effect["mp"]
        player.mp = min(player.mp, player.max_mp)
    if "skill" in effect:
        # 칭호 전용 스킬 부여
        skill = effect["skill"]
        if skill not in player.skills:
            player.skills[skill] = 1
            print(f"✨ 칭호 전용 스킬 '{skill}' 해금!")
            log_event(player, f"[칭호 스킬 해금] {skill}")


# ------------------------
# 칭호 비활성화
# ------------------------
def deactivate_title(player):
    if not player.active_title:
        print("❌ 현재 활성화된 칭호 없음")
        return
    print(f"❌ 칭호 해제: {player.active_title}")
    log_event(player, f"[칭호 해제] {player.active_title}")
    player.active_title = None


# ------------------------
# 칭호 목록 보기
# ------------------------
def show_titles(player):
    print("\n🏷 [칭호 목록]")
    if not player.titles:
        print("보유한 칭호가 없습니다.")
        return
    for t in player.titles:
        eff = TITLES.get(t, {})
        mark = "✅" if player.active_title == t else "❌"
        desc = eff.get("desc", "")
        print(f"{mark} {t} - {desc}")