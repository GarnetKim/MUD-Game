import random
from mudgame.battle import Monster, start_battle

EVENTS = ["monster", "chest", "trap", "merchant", "boss"]

def explore_room(player, log):
    event = random.choice(EVENTS)

    if event == "monster":
        m = Monster("던전 슬라임", 20, 6, 1)
        log(f"👾 몬스터 {m.name} 출현!")
        return ("battle", m)

    elif event == "chest":
        gold = random.randint(10, 50)
        player.gold += gold
        log(f"💰 보물상자 발견! {gold} Gold 획득")
        return ("chest", None)

    elif event == "trap":
        dmg = random.randint(5, 15)
        player.hp -= dmg
        log(f"💥 함정 발동! {dmg} 피해 (HP {player.hp})")
        return ("trap", None)

    elif event == "merchant":
        log("🧑‍🦱 던전 속 상인을 만났다!")
        return ("merchant", None)

    elif event == "boss":
        m = Monster("던전 보스", 100, 15, 5, is_boss=True)
        log("👹 보스룸에 들어섰다!")
        return ("battle", m)

    return (None, None)