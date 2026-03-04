import streamlit as st
import gspread
import pandas as pd

# ==========================================
# 1. 建立 Google Sheets 連線
# ==========================================
@st.cache_resource
def init_connection():
    # 確保 st.secrets 中有 gcp_service_account 資訊
    credentials = dict(st.secrets["gcp_service_account"])
    gc = gspread.service_account_from_dict(credentials)
    return gc

gc = init_connection()

# ==========================================
# 2. 設定試算表資訊
# ==========================================
# 請將下方更換為你的試算表網址或名稱
SHEET_INPUT = "https://docs.google.com/spreadsheets/d/10vzFUpqcuySKnDOXNnYlm6oFY-LrcvwwGOQXNSWSH5k/edit?gid=0#gid=0" 
WORKSHEET_NAME = "工作表1"

try:
    if SHEET_INPUT.startswith("http://") or SHEET_INPUT.startswith("https://"):
        sh = gc.open_by_url(SHEET_INPUT)
    else:
        sh = gc.open(SHEET_INPUT)
    worksheet = sh.worksheet(WORKSHEET_NAME)
except Exception as e:
    st.error(f"無法開啟試算表！\n請確認：\n1. 網址是否正確\n2. 服務帳號 ({gc.auth.signer_email}) 已被加入共用編輯者權限。\n\n錯誤訊息：{e}")
    st.stop()

st.title("📊 Google Sheets 讀寫測試儀表板")

# ==========================================
# 3. 讀取資料 (Read)
# ==========================================
st.header("1️⃣ 目前資料列表")

data = worksheet.get_all_records()

if data:
    df = pd.DataFrame(data)
    # 插入列數顯示（從第 2 列開始，因為第 1 列是標題）
    df.insert(0, "試算表列數", range(2, len(data) + 2))
    st.dataframe(df, use_container_width=True)
else:
    st.info("目前工作表中沒有資料。請確保工作表的第一列有標題（例如：姓名, 數量）")

st.divider()

# ==========================================
# 4. 新增資料 (Create)
# ==========================================
st.header("2️⃣ 新增資料")

with st.form("add_data_form", clear_on_submit=True):
    col1 = st.text_input("姓名", key="add_name")
    col2 = st.number_input("數量", min_value=0, value=1, key="add_qty")
    submitted = st.form_submit_button("寫入 Google Sheet")

    if submitted:
        if col1.strip() == "":
            st.warning("請填寫姓名！")
        else:
            with st.spinner("正在寫入資料中..."):
                worksheet.append_row([col1, col2])
            st.success("資料已成功寫入！")
            st.rerun()

st.divider()

# 只有在有資料的時候，才顯示修改與刪除的區塊
if data:
    # 建立選項清單
    row_options = {f"第 {i + 2} 列: {row.get('姓名', '未知')}": i + 2 for i, row in enumerate(data)}
    
    col_update, col_delete = st.columns(2)

    # ==========================================
    # 5. 修改資料 (Update)
    # ==========================================
    with col_update:
        st.header("3️⃣ 修改資料")
        selected_option_update = st.selectbox("選擇要修改的資料", options=list(row_options.keys()), key="update_select")
        selected_row_update = row_options[selected_option_update]

        # 獲取當前選中列的資料 (index = row - 2)
        current_data = data[selected_row_update - 2]

        with st.form("update_data_form"):
            new_name = st.text_input("新姓名", value=current_data.get("姓名", ""))
            new_qty = st.number_input("新數量", min_value=0, value=int(current_data.get("數量", 0)))
            update_submitted = st.form_submit_button("更新資料")

            if update_submitted:
                if new_name.strip() == "":
                    st.warning("請填寫姓名！")
                else:
                    with st.spinner("正在更新資料中..."):
                        # 更新對應儲存格 (gspread 的 cell index 從 1 開始)
                        worksheet.update_cell(selected_row_update, 1, new_name)
                        worksheet.update_cell(selected_row_update, 2, new_qty)
                    st.success("資料已成功更新！")
                    st.rerun()

    # ==========================================
    # 6. 刪除資料 (Delete)
    # ==========================================
    with col_delete:
        st.header("4️⃣ 刪除資料")
        selected_option_del = st.selectbox("選擇要刪除的資料", options=list(row_options.keys()), key="delete_select")
        selected_row_del = row_options[selected_option_del]

        st.write(f"⚠️ 即將刪除：**{selected_option_del}**")

        if st.button("🗑️ 確認刪除", type="primary"):
            with st.spinner("正在刪除資料中..."):
                worksheet.delete_rows(selected_row_del)
            st.success("資料已成功刪除！")
            st.rerun()
