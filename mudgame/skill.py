import random
from mudgame.log_system import log_event

# ------------------------
# 스킬 정의
# ------------------------
SKILLS = {
    "heal": {"mp": 8, "cooldown": 3, "desc": "HP 30 회복"},
    "fireball": {"mp": 10, "cooldown": 2, "desc": "ATK*2 피해"},
    "shield": {"mp": 6, "cooldown": 3, "desc": "방어력 +5 (3턴)"},
    "ultimate": {"mp": 30, "cooldown": 0, "desc": "궁극기 (1회 제한)"},
}

# ------------------------
# 스킬 이펙트 ASCII
# ------------------------
ASCII_EFFECTS = {
    "heal": """
      ✨✨✨
     ✨  +HP  ✨
      ✨✨✨
    """,
    "fireball": """
      🔥🔥🔥
     🔥  BOOM!  🔥
      🔥🔥🔥
    """,
    "shield": """
      🛡️🛡️🛡️
     🛡️ DEF+ 🛡️
      🛡️🛡️🛡️
    """,
    "ultimate": """
██████╗ ██╗   ██╗███╗   ███╗██╗███╗   ██╗████████╗
██╔══██╗██║   ██║████╗ ████║██║████╗  ██║╚══██╔══╝
██████╔╝██║   ██║██╔████╔██║██║██╔██╗ ██║   ██║   
██╔═══╝ ██║   ██║██║╚██╔╝██║██║██║╚██╗██║   ██║   
██║     ╚██████╔╝██║ ╚═╝ ██║██║██║ ╚████║   ██║   
╚═╝      ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝   ╚═╝   
    """,
}

# ------------------------
# 스킬 사용
# ------------------------
def use_skill(player, skill_name, target=None):
    if skill_name not in SKILLS:
        print("❌ 알 수 없는 스킬")
        return

    skill = SKILLS[skill_name]
    mp_cost = skill["mp"]
    cooldown = skill["cooldown"]

    # MP 체크
    if player.mp < mp_cost:
        print("❌ MP 부족")
        return

    # 쿨타임 체크
    if skill_name in player.skill_cooldowns and player.skill_cooldowns[skill_name] > 0:
        print(f"⌛ 스킬 쿨타임 {player.skill_cooldowns[skill_name]}턴 남음")
        return

    # 궁극기 사용 체크
    if skill_name == "ultimate" and player.ultimate_used:
        print("❌ 궁극기는 이미 사용했습니다.")
        return

    # 소모 처리
    player.mp -= mp_cost
    if cooldown > 0:
        player.skill_cooldowns[skill_name] = cooldown

    # 궁극기 1회 제한
    if skill_name == "ultimate":
        player.ultimate_used = True

    # 효과 적용
    if skill_name == "heal":
        heal = min(30, player.max_hp - player.hp)
        player.hp += heal
        print(ASCII_EFFECTS["heal"])
        print(f"✨ HP {heal} 회복!")
        log_event(player, f"[스킬] Heal +{heal} HP")
    elif skill_name == "fireball" and target:
        dmg = max(0, player.atk*2 - target.defense)
        target.hp -= dmg
        print(ASCII_EFFECTS["fireball"])
        print(f"🔥 Fireball! {dmg} 피해")
        log_event(player, f"[스킬] Fireball {dmg} 피해 → {target.name}")
    elif skill_name == "shield":
        player.defense += 5
        print(ASCII_EFFECTS["shield"])
        print(f"🛡️ 방어력 +5 (3턴)")
        log_event(player, "[스킬] Shield DEF+5")
    elif skill_name == "ultimate" and target:
        dmg = max(0, player.atk*5 - target.defense)
        target.hp -= dmg
        print(ASCII_EFFECTS["ultimate"])
        print(f"💥 궁극기 발동! {dmg} 피해")
        log_event(player, f"[스킬] Ultimate {dmg} 피해 → {target.name}")


# ------------------------
# 쿨타임 감소 (턴 종료 시)
# ------------------------
def tick_cooldowns(player):
    for k in list(player.skill_cooldowns.keys()):
        if player.skill_cooldowns[k] > 0:
            player.skill_cooldowns[k] -= 1


# ------------------------
# 스킬 도감
# ------------------------
def unlock_skill(player, skill_name):
    if skill_name not in SKILLS:
        return
    if skill_name not in player.skill_codex:
        player.skill_codex[skill_name] = 1
        print(f"📖 스킬 도감 해금: {skill_name}")
    if skill_name not in player.skills:
        player.skills[skill_name] = 1
        print(f"✨ 스킬 {skill_name} 습득!")


def show_skill_codex(player):
    print("\n📖 [스킬 도감]")
    unlocked = len(player.skill_codex)
    total = len(SKILLS)
    percent = int((unlocked / total) * 100)
    print(f"완성도: {unlocked}/{total} ({percent}%)")
    print("──────────────────────────")
    for s, info in SKILLS.items():
        if s in player.skill_codex:
            print(f"✅ {s} - {info['desc']} (레벨 {player.skill_codex[s]})")
        else:
            print(f"❌ {s} - ???")
    print("──────────────────────────")