import streamlit as st
import pandas as pd
import numpy as np

# 1. 設定網頁標題與頁面設定（建議加上 icon）
st.set_page_config(page_title="我的第一個 App", page_icon="🚀")
st.title('我的第一個 Streamlit App')

# 2. 顯示文字內容
st.write('恭喜你！你已經成功架設了你的第一個網頁應用程式。')

# 3. 互動元件：輸入名字
# 使用 columns 讓版面更漂亮
user_name = st.text_input("請輸入你的名字", "訪客")

if user_name:
    st.success(f"哈囉, **{user_name}**！歡迎來到 Streamlit 的世界。")

# 4. 數據視覺化
st.divider() # 加入分隔線
st.subheader('📊 簡單的數據展示')

# 隨機產生數據
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['A', 'B', 'C']
)

# 顯示數據表格（可選）
with st.expander("查看原始數據"):
    st.write(chart_data)

# 繪製折線圖
st.line_chart(chart_data)

# 5. 側邊欄範例
with st.sidebar:
    st.header("側邊欄設定")
    st.write("這裡可以放參數設定或導覽列。")
    # 修正了原本可能的標點符號問題
    if st.button("點擊測試"):
        st.balloons() # 增加一個慶祝動畫
