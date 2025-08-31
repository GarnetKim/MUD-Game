import datetime

def log_event(player, message):
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    entry = f"[{ts}] {message}"
    if not hasattr(player,"combat_log"): player.combat_log=[]
    player.combat_log.append(entry)
    today = datetime.date.today().strftime("%Y-%m-%d")
    with open(f"combat_log_{today}.txt","a",encoding="utf-8") as f:
        f.write(entry+"\n")