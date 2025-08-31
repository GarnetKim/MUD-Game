def hp_gauge(player):
    ratio = player.hp/player.max_hp
    filled = int(ratio*20)
    return "🟥"*filled + "⬛"*(20-filled) + f" {player.hp}/{player.max_hp}"

def mp_gauge(player):
    ratio = player.mp/player.max_mp
    filled = int(ratio*20)
    return "🟦"*filled + "⬛"*(20-filled) + f" {player.mp}/{player.max_mp}"