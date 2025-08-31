import streamlit as st
from mudgame.shop import SHOP_STOCK, get_price, buy_item, sell_item

def shop_ui(player, log):
    st.subheader("🏪 상점")

    for idx, (name, data) in enumerate(SHOP_STOCK.items(), 1):
        price = get_price(name)
        stock = data["stock"]
        discount = " (할인!)" if price < data["price"] else ""
        col1, col2, col3 = st.columns([3,1,1])
        with col1:
            st.write(f"{idx}. {name} - {price} Gold [재고:{stock}]{discount}")
        with col2:
            if st.button(f"구매 {idx}"):
                buy_item(player, name)  # 기존 로직 재사용
                log(f"🛒 {name} 구매 시도!")
        with col3:
            # 인벤토리에 있을 경우만 판매 버튼 노출
            if any(it.name == name for it in player.inventory):
                if st.button(f"판매 {idx}"):
                    item = next(it for it in player.inventory if it.name == name)
                    sell_item(player, item)  # 기존 로직 재사용
                    log(f"💰 {name} 판매 시도!")

    st.write(f"보유 Gold: {player.gold}")
    if st.button("⬅️ 상점 나가기"):
        st.session_state.shop_open = False