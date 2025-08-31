import random

# ------------------------
# 스킬 정의
# ------------------------
SKILLS = {
    "Heal": {"mp": 8, "cooldown": 3, "desc": "HP 30 회복"},
    "Fireball": {"mp": 10, "cooldown": 2, "desc": "ATK*2 피해"},
    "Shield Bash": {"mp": 6, "cooldown": 3, "desc": "방어력 +5 (3턴)"},
    "Ultimate": {"mp": 30, "cooldown": 0, "desc": "궁극기 (1회 제한)"},
}

# ------------------------
# ASCII 이펙트
# ------------------------
ASCII_EFFECTS = {
    "Heal": """
      ✨✨✨
     ✨  +HP  ✨
      ✨✨✨
    """,
    "Fireball": """
      🔥🔥🔥
     🔥  BOOM!  🔥
      🔥🔥🔥
    """,
    "Shield Bash": """
      🛡️🛡️🛡️
     🛡️ DEF+ 🛡️
      🛡️🛡️🛡️
    """,
    "Ultimate": """
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
def use_skill(player, skill_name, target=None, log=None):
    if skill_name not in SKILLS:
        if log: log("❌ 알 수 없는 스킬")
        return

    skill = SKILLS[skill_name]
    mp_cost = skill["mp"]
    cooldown = skill["cooldown"]

    # MP 체크
    if player.mp < mp_cost:
        if log: log("❌ MP 부족")
        return

    # 쿨타임 체크
    if skill_name in getattr(player, "skill_cooldowns", {}) and player.skill_cooldowns[skill_name] > 0:
        if log: log(f"⌛ 스킬 쿨타임 {player.skill_cooldowns[skill_name]}턴 남음")
        return

    # 궁극기 체크
    if skill_name == "Ultimate" and getattr(player, "ultimate_used", False):
        if log: log("❌ 궁극기는 이미 사용했습니다.")
        return

    # 소모 처리
    player.mp -= mp_cost
    if not hasattr(player, "skill_cooldowns"):
        player.skill_cooldowns = {}
    if cooldown > 0:
        player.skill_cooldowns[skill_name] = cooldown

    if skill_name == "Ultimate":
        player.ultimate_used = True

    # 효과 적용
    if skill_name == "Heal":
        heal = min(30, player.max_hp - player.hp)
        player.hp += heal
        if log: log(ASCII_EFFECTS["Heal"]); log(f"✨ HP {heal} 회복!")
    elif skill_name == "Fireball" and target:
        dmg = max(0, player.atk * 2 - target.defense)
        target.hp -= dmg
        if log: log(ASCII_EFFECTS["Fireball"]); log(f"🔥 Fireball! {dmg} 피해 → {target.name}")
    elif skill_name == "Shield Bash":
        player.defense += 5
        if log: log(ASCII_EFFECTS["Shield Bash"]); log("🛡️ 방어력 +5 (3턴)")
    elif skill_name == "Ultimate" and target:
        dmg = max(0, player.atk * 5 - target.defense)
        target.hp -= dmg
        if log: log(ASCII_EFFECTS["Ultimate"]); log(f"💥 궁극기 발동! {dmg} 피해 → {target.name}")

# ------------------------
# 쿨타임 감소
# ------------------------
def tick_cooldowns(player):
    if not hasattr(player, "skill_cooldowns"):
        player.skill_cooldowns = {}
    for k in list(player.skill_cooldowns.keys()):
        if player.skill_cooldowns[k] > 0:
            player.skill_cooldowns[k] -= 1

# ------------------------
# 스킬 도감
# ------------------------
def unlock_skill(player, skill_name, log=None):
    if skill_name not in SKILLS:
        return
    if skill_name not in player.codex["skills"]:
        player.codex["skills"].add(skill_name)
        if log: log(f"📖 스킬 도감 해금: {skill_name}")
    if skill_name not in player.skills:
        player.skills[skill_name] = {"level": 1, "cooldown": SKILLS[skill_name]["cooldown"], "mp": SKILLS[skill_name]["mp"]}
        if log: log(f"✨ 스킬 {skill_name} 습득!")

def show_skill_codex(player, log=None):
    unlocked = len(player.codex["skills"])
    total = len(SKILLS)
    percent = int((unlocked / total) * 100)
    if log:
        log(f"📖 스킬 도감 {unlocked}/{total} ({percent}%) 완성")
    return unlocked, total, percent