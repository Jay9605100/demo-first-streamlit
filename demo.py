import streamlit as st
import pandas as pd

# 假設這是你的原始數據
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame([{"品項": "蘋果", "數量": 10}])

st.title("庫存修改系統")

# 模擬選擇一筆資料
selected_item = st.selectbox("選擇要修改的品項", st.session_state.df["品項"])
current_data = st.session_state.df[st.session_state.df["品項"] == selected_item].iloc[0]

# --- 關鍵修正區塊 ---
with st.form("edit_form"):
    st.write(f"正在編輯：{selected_item}")
    
    # 使用 .get() 或是先檢查欄位，避免 KeyError
    default_qty = int(current_data["數量"]) if "數量" in current_data else 0
    
    new_qty = st.number_input("新數量", min_value=0, value=default_qty)
    
    # 必須加上這行，否則會出現你遇到的 "Missing Submit Button" 警告
    submitted = st.form_submit_button("確認修改")
    
    if submitted:
        # 執行更新邏輯
        idx = st.session_state.df[st.session_state.df["品項"] == selected_item].index
        st.session_state.df.at[idx[0], "數量"] = new_qty
        st.success("資料已更新！")
        st.rerun()
