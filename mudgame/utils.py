def format_item(item):
    return f"{item.display_name()} ({item.rarity})"

def gauge_bar(current, max_value, symbol="🟩", length=10):
    filled = int((current/max_value)*length)
    return symbol*filled + "⬛"*(length-filled)