from log_system import log_event

# ------------------------
# 세트 효과 정의
# ------------------------
SET_EFFECTS = {
    "전설+전설": {"atk": 20, "desc": "궁극기 사용 가능", "ultimate": True},
    "전설+레어": {"atk": 10, "def": 5, "desc": "특수 보너스"},
    "레어+레어": {"def": 15, "desc": "방어 특화"},
}

# ------------------------
# 세트 효과 확인
# ------------------------
def check_set_bonus(player):
    if not player.weapon or not player.armor:
        return None
    w = player.weapon.rarity
    a = player.armor.rarity
    combo = f"{w}+{a}"
    if combo in SET_EFFECTS:
        return combo, SET_EFFECTS[combo]
    combo = f"{a}+{w}"
    if combo in SET_EFFECTS:
        return combo, SET_EFFECTS[combo]
    return None


# ------------------------
# 세트 효과 적용
# ------------------------
def apply_set_bonus(player):
    combo = check_set_bonus(player)
    if not combo:
        return
    key, effect = combo
    if "atk" in effect:
        player.atk += effect["atk"]
    if "def" in effect:
        player.defense += effect["def"]
    if effect.get("ultimate"):
        if "ultimate" not in player.skills:
            player.skills["ultimate"] = 1
            print("💥 세트 효과: 궁극기 스킬 해금!")
            log_event(player, "[세트 효과] 궁극기 해금")

    # 도감 등록
    if key not in player.set_codex_unlocked:
        player.set_codex_unlocked[key] = True
        print(f"📖 세트 도감 등록: {key}")
        log_event(player, f"[세트 도감 등록] {key}")


# ------------------------
# 세트 도감 출력
# ------------------------
def show_set_codex(player):
    print("\n📖 [세트 도감]")
    unlocked = len([k for k, v in player.set_codex_unlocked.items() if v])
    total = len(SET_EFFECTS)
    percent = int((unlocked / total) * 100)
    print(f"완성도: {unlocked}/{total} ({percent}%)")
    print("─────────────────────────────")
    for key, effect in SET_EFFECTS.items():
        if player.set_codex_unlocked.get(key, False):
            effs = []
            if "atk" in effect: effs.append(f"ATK+{effect['atk']}")
            if "def" in effect: effs.append(f"DEF+{effect['def']}")
            if effect.get("ultimate"): effs.append("궁극기 해금")
            print(f"✅ {key} - {effect['desc']} ({', '.join(effs)})")
        else:
            print(f"❌ {key} - ???")
    print("─────────────────────────────")


# ------------------------
# 세트 완성 보상
# ------------------------
def check_codex_completion(player):
    unlocked = len([k for k, v in player.set_codex_unlocked.items() if v])
    total = len(SET_EFFECTS)
    if unlocked == total:
        print("🏆 세트 도감 100% 달성! 특별 보상 지급!")
        log_event(player, "[세트 도감] 100% 달성")
        # 보상: 골드 + 특별 칭호
        player.gold += 500
        if "세트 마스터" not in player.titles:
            player.titles.append("세트 마스터")
            print("✨ 칭호 획득: 세트 마스터")