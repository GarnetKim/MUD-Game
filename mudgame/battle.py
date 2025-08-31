import random

class Monster:
    def __init__(self, name, hp, atk, defense, effects=None):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.atk = atk
        self.defense = defense
        self.effects = effects or {}

    def is_alive(self):
        return self.hp > 0


def start_battle(player, monster, log_func):
    """전투 시작 세션 초기화"""
    log_func(f"⚔️ 전투 시작! {monster.name}이(가) 나타났다!")
    return {
        "player_hp": player.hp,
        "monster_hp": monster.hp,
        "monster": monster,
        "turn": 1,
        "in_battle": True
    }


def battle_turn(player, state, action, log_func):
    """턴 진행 (버튼으로 선택된 action 기반)"""
    monster = state["monster"]

    if not monster.is_alive():
        log_func(f"🎉 {monster.name}은(는) 이미 쓰러져 있습니다!")
        state["in_battle"] = False
        return state

    # 플레이어 행동
    if action == "attack":
        dmg = max(1, player.atk - monster.defense)
        monster.hp -= dmg
        log_func(f"🗡️ {player.name}의 공격! {monster.name}에게 {dmg} 피해 (남은 HP {monster.hp})")
    elif action == "skill":
        dmg = max(1, player.atk * 2 - monster.defense)
        monster.hp -= dmg
        log_func(f"🔥 {player.name}의 스킬 발동! {monster.name}에게 {dmg} 피해 (남은 HP {monster.hp})")
    elif action == "run":
        log_func(f"🏃‍♂️ {player.name}은(는) 도망쳤다!")
        state["in_battle"] = False
        return state

    # 몬스터 생존 체크
    if monster.hp <= 0:
        log_func(f"🎉 {monster.name} 처치 성공! 전투 승리!")
        player.gold += 10
        state["in_battle"] = False
        return state

    # 몬스터 반격
    dmg = max(1, monster.atk - player.defense)
    player.hp -= dmg
    log_func(f"💥 {monster.name}의 반격! {player.name}이(가) {dmg} 피해 (남은 HP {player.hp})")

    # 패배 체크
    if player.hp <= 0:
        log_func(f"💀 {player.name}은(는) 쓰러졌다... 게임 오버!")
        state["in_battle"] = False

    state["turn"] += 1
    return state