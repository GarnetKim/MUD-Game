import streamlit as st
from mudgame.shop import SHOP_STOCK, get_price, buy_item, sell_item

def shop_ui(player, log):
    st.subheader("🏪 상점")
    for idx, (name, data) in enumerate(SHOP_STOCK.items(), 1):
        col1, col2, col3 = st.columns([3,1,1])
        with col1:
            st.write(f"{idx}. {name} - {data['price']} Gold [재고:{data['stock']}]")
        with col2:
            if st.button(f"구매 {idx}"):
                msg = buy_item(player, name)
                log(msg)
        with col3:
            if any(it.name == name for it in player.inventory):
                if st.button(f"판매 {idx}"):
                    item = next(it for it in player.inventory if it.name == name)
                    msg = sell_item(player, item)
                    log(msg)
    st.write(f"보유 Gold: {player.gold}")
    if st.button("⬅️ 상점 나가기"):
        st.session_state.shop_open = False