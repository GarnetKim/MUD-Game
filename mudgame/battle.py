import random
import datetime
from mudgame.log_system import log_event
from mudgame.utils import hp_gauge, mp_gauge
from mudgame.save_load import save_game

# ------------------------
# 몬스터 클래스
# ------------------------
class Monster:
    def __init__(self, name, hp, atk, defense, exp_reward=20, gold_reward=10, status_attack=None, is_boss=False):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.atk = atk
        self.defense = defense
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward
        self.status_attack = status_attack  # ex: {"poison":30}
        self.is_boss = is_boss

    def is_dead(self):
        return self.hp <= 0


# ------------------------
# 내성 계산 (장비 합산)
# ------------------------
def calculate_total_resistances(player):
    total = {}
    equipped = [player.weapon, player.armor]
    for item in equipped:
        if item and item.resistances:
            for k, v in item.resistances.items():
                total[k] = min(100, total.get(k, 0) + v)
    return total


# ------------------------
# 상태이상 적용
# ------------------------
def apply_status(player, status):
    resistances = calculate_total_resistances(player)
    if status in resistances:
        chance = resistances[status]
        roll = random.randint(1, 100)
        if roll <= chance:
            print(f"🛡️ {status.upper()} 면역 발동! ({chance}%)")
            log_event(player, f"[저항 발동] {status} 면역 ({chance}%)")
            return False
    # 내성 실패 → 적용
    if status not in player.status_effects:
        player.status_effects.append(status)
        print(f"☠️ {status.upper()} 상태이상에 걸렸습니다!")
        log_event(player, f"[상태이상] {status} 발동")
    return True


# ------------------------
# 레벨업 처리
# ------------------------
def level_up(player):
    player.level += 1
    player.exp = 0
    player.exp_to_next = int(player.exp_to_next * 1.5)
    player.max_hp += 20
    player.max_mp += 10
    player.hp = player.max_hp
    player.mp = player.max_mp
    player.atk += 5
    player.defense += 3
    print("🌟 LEVEL UP! 새로운 힘이 깨어납니다!")
    print("───────────────")
    print("❤️ HP, 🔮 MP 완전 회복!")
    print("───────────────")
    log_event(player, f"[레벨업] {player.level} 달성")


# ------------------------
# EXP 게이지 출력
# ------------------------
def exp_bar(player):
    ratio = player.exp / player.exp_to_next if player.exp_to_next else 1
    filled = int(ratio * 20)
    return "📊" * filled + "⬛" * (20 - filled) + f" {player.exp}/{player.exp_to_next}"


# ------------------------
# 전투 루프
# ------------------------
def battle(player, monster: Monster):
    print(f"⚔️ 전투 시작! {monster.name} 등장 (HP {monster.hp}/{monster.max_hp})")
    log_event(player, f"[전투 시작] {monster.name}")
    turn = 1

    while player.hp > 0 and not monster.is_dead():
        print(f"\n─── 턴 {turn} ───")
        print(f"👤 {player.name}: {hp_gauge(player)} | {mp_gauge(player)}")
        print(f"👹 {monster.name}: HP {monster.hp}/{monster.max_hp}")

        cmd = input("행동 선택 (attack / skill / item / run): ").strip()

        if cmd == "attack":
            damage = max(0, player.atk - monster.defense)
            monster.hp -= damage
            print(f"⚔️ {player.name}의 공격! {damage} 피해")
            log_event(player, f"[공격] {damage} 피해 → {monster.name}")

        elif cmd == "skill":
            if "fireball" in player.skills and player.mp >= 10:
                player.mp -= 10
                damage = max(0, player.atk*2 - monster.defense)
                monster.hp -= damage
                print(f"🔥 Fireball 발동! {damage} 피해 (MP-10)")
                log_event(player, f"[스킬] Fireball {damage} 피해 → {monster.name}")
            elif "heal" in player.skills and player.mp >= 8:
                player.mp -= 8
                heal = min(player.max_hp - player.hp, 30)
                player.hp += heal
                print(f"✨ Heal 발동! HP {heal} 회복 (MP-8)")
                log_event(player, f"[스킬] Heal HP+{heal}")
            else:
                print("❌ 사용할 수 있는 스킬이 없거나 MP 부족")

        elif cmd == "item":
            print("🎒 아이템 사용은 추후 구현 연결 (포션, 해제제)")

        elif cmd == "run":
            print("🏃 전투에서 도망쳤습니다.")
            log_event(player, "[전투] 도망 성공")
            return False

        else:
            print("❌ 잘못된 명령어입니다.")

        # 몬스터 반격 (죽었는지 확인 후)
        if not monster.is_dead():
            m_dmg = max(0, monster.atk - player.defense)
            player.hp -= m_dmg
            print(f"👹 {monster.name}의 공격! {m_dmg} 피해")
            log_event(player, f"[피해] {player.name} {m_dmg} 피해")

            # 상태이상 공격 판정
            if monster.status_attack:
                for status, chance in monster.status_attack.items():
                    if random.randint(1, 100) <= chance:
                        apply_status(player, status)

        turn += 1

    # 전투 종료
    if monster.is_dead():
        print(f"\n🎉 {monster.name} 처치! 전투 승리")
        log_event(player, f"[전투 승리] {monster.name}")
        reward(player, monster)
        save_game(player)  # 자동 저장
        return True
    else:
        print("💀 전투 패배...")
        log_event(player, f"[전투 패배] {monster.name}")
        return False


# ------------------------
# 전투 보상
# ------------------------
def reward(player, monster: Monster):
    player.gold += monster.gold_reward
    player.exp += monster.exp_reward

    print(f"💰 전리품 획득: {monster.gold_reward} Gold")
    print(f"⭐ 경험치 획득: {monster.exp_reward}")
    print(exp_bar(player))

    # 레벨업 확인
    if player.exp >= player.exp_to_next:
        level_up(player)

    # 보스 처치 특수 연출
    if monster.is_boss:
        print("🎆🎇 보스 처치! EXP 폭죽이 터집니다!")
        ascii_fireworks()


# ------------------------
# ASCII 연출 (보스 처치용)
# ------------------------
def ascii_fireworks():
    art = r"""
          .''.       •✦•    
  .''.      .        •  
 •✦•    *''*    :_\/_:     .
•  •  :_\/_:   : /\/\ :  •✦• 
   *  : /\/\ :  '..'  *  
      '..'   *''*    
           * 
    """
    print(art)