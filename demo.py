import streamlit as st
import pandas as pd
import numpy as np

# 1. 頁面基礎設定
st.set_page_config(page_title="Streamlit 測試", layout="centered")

# 2. 標題與簡介
st.title('🚀 我的第一個 Streamlit App')
st.write('恭喜你！這是一個乾淨、無錯誤的程式版本。')

# 3. 互動元件
user_name = st.text_input("請輸入你的名字", "訪客")

if user_name:
    st.success(f"哈囉, **{user_name}**！歡迎來到 Streamlit 的世界。")

# 4. 數據視覺化區塊
st.divider()
st.subheader('📊 隨機數據折線圖')

# 建立隨機資料
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['A', 'B', 'C']
)

# 顯示圖表
st.line_chart(chart_data)

# 5. 側邊欄
with st.sidebar:
    st.header("⚙️ 設定面板")
    st.info("這是在側邊欄的提示訊息。")
    if st.button("點擊慶祝"):
        st.balloons()
