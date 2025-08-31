import random

class Monster:
    def __init__(self, name, hp, atk, defense, is_boss=False):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.atk = atk
        self.defense = defense
        self.is_boss = is_boss

    def is_alive(self):
        return self.hp > 0


def start_battle(player, monster, log):
    log(f"⚔️ {monster.name} 전투 시작!")
    return {"player": player, "monster": monster, "turn": 1, "in_battle": True}


def battle_turn(player, state, action, log):
    monster = state["monster"]

    if not monster.is_alive():
        log(f"🎉 {monster.name}은 이미 쓰러졌습니다!")
        state["in_battle"] = False
        return state

    # 행동 처리
    if action == "attack":
        dmg = max(1, player.atk - monster.defense)
        monster.hp -= dmg
        log(f"🗡️ {player.name} 공격 → {monster.name}에게 {dmg} 피해 (HP {monster.hp})")
    elif action == "skill":
        dmg = max(1, player.atk * 2 - monster.defense)
        monster.hp -= dmg
        player.mp -= 5
        log(f"🔥 스킬 발동! {monster.name}에게 {dmg} 피해 (HP {monster.hp})")
    elif action == "run":
        log("🏃 도망쳤다!")
        state["in_battle"] = False
        return state

    if monster.hp <= 0:
        log(f"🎉 {monster.name} 처치 성공!")
        state["in_battle"] = False

        # 보상 처리
        if monster.is_boss:
            reward_gold = 200
            player.add_gold(reward_gold, log)

            # 전설 아이템 보상
            legendary = Item("보스의 전설 검", "weapon", "전설", attack=15, durability=200, price=500)
            player.add_item(legendary, log)

            log("🏆 보스를 쓰러뜨려 전설 보상을 획득했습니다!")
        else:
            reward_gold = 30
            player.add_gold(reward_gold, log)

        return state

    # 몬스터 반격
    dmg = max(1, monster.atk - player.defense)
    player.hp -= dmg
    log(f"💥 {monster.name} 반격! {dmg} 피해 (HP {player.hp})")

    if player.hp <= 0:
        log("💀 플레이어가 쓰러졌습니다... 게임 오버")
        state["in_battle"] = False

    state["turn"] += 1
    return state