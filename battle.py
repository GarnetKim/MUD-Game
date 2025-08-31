import random
from log_system import log_event

def apply_status(player, status, resistances):
    if status in resistances:
        chance = resistances[status]
        roll = random.randint(1,100)
        if roll <= chance:
            print(f"🛡️ {status.upper()} 면역 발동! ({chance}%)")
            log_event(player, f"[저항 발동] {status} 면역 ({chance}%)")
            return False
    player.status_effects.append(status)
    print(f"☠️ {status.upper()} 상태이상에 걸렸습니다!")
    log_event(player, f"[상태이상] {status} 발동")
    return True