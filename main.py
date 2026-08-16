import streamlit as st
import pandas as pd

# ===================== 1. 页面全局配置（蓝紫色调基础）=====================
st.set_page_config(
    page_title="学生信息查询系统",  # 浏览器标签标题
    page_icon="📖",                 # 标签小图标
    layout="wide",                  # 宽屏布局，不挤在中间
    initial_sidebar_state="collapsed" # 收起侧边栏，界面更干净
)

# ===================== 2. 蓝紫色系全局样式注入 =====================
st.markdown("""
<style>
/* 全局背景色：浅蓝紫渐变 */
.stApp {
    background: linear-gradient(135deg, #f8f9fa 0%, #e0e7ff 100%);
}
/* 主标题样式：蓝紫色、居中、加大加粗 */
h1 {
    color: #4338ca !important;
    font-weight: 700 !important;
    text-align: center !important;
    margin-top: 2rem !important;
    margin-bottom: 1rem !important;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}
/* 卡片样式：圆角、浅蓝背景、阴影 */
.stContainer {
    background-color: rgba(255, 255, 255, 0.8) !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
    box-shadow: 0 4px 12px rgba(67, 56, 202, 0.15) !important;
    border: 1px solid #c7d2fe !important;
}
/* 按钮样式：蓝紫色渐变、圆角、 hover效果 */
.stButton>button {
    background: linear-gradient(90deg, #4338ca 0%, #6366f1 100%) !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 0.5rem 2rem !important;
    font-weight: 600 !important;
    border: none !important;
    transition: all 0.3s ease !important;
}
.stButton>button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 16px rgba(67, 56, 202, 0.3) !important;
}
/* 输入框样式：蓝紫色边框、圆角 */
.stTextInput>div>div>input {
    border-radius: 8px !important;
    border: 1px solid #a5b4fc !important;
    padding: 0.5rem !important;
}
/* 表格样式：表头蓝紫色、行交替底色 */
.stDataFrame thead tr th {
    background-color: #4338ca !important;
    color: white !important;
    font-weight: 600 !important;
}
.stDataFrame tbody tr:nth-child(even) {
    background-color: #f1f5f9 !important;
}
.stDataFrame tbody tr:nth-child(odd) {
    background-color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ===================== 3. 读取Excel【不清理，保留Unnamed、保留None】=====================
@st.cache_data
def load_data():
    df = pd.read_excel("student.xlsx")
    # 删掉两行清理代码，不删除空列、不替换空值
    # df = df.dropna(axis=1, how="all")  注释/删除
    # df = df.fillna("")                 注释/删除
    return df

df = load_data()

# ===================== 4. 界面布局 =====================
st.markdown("<h1>📖 学生信息查询系统</h1>", unsafe_allow_html=True)
st.divider()

with st.container(border=True):
    st.subheader("🔍 学生查询")
    col1, col2 = st.columns(2)
    with col1:
        stu_id = st.text_input("请输入学号", placeholder="请输入完整学号")
    with col2:
        stu_name = st.text_input("请输入姓名", placeholder="请输入学生姓名")
    btn_query = st.button("开始查询", type="primary")

# ===================== 5. 查询逻辑 =====================
if btn_query:
    query_df = df[(df["学号"].astype(str) == stu_id) & (df["姓名"] == stu_name)]
    if not query_df.empty:
        st.success("✅ 查询成功！以下是匹配到的学生信息：")
        st.dataframe(query_df, height=350, use_container_width=True)
    else:
        st.warning("⚠️ 未匹配到该学生信息，请检查学号和姓名是否正确")

# 底部文字
st.markdown("""
<div style='text-align: center; color: #64748b; margin-top: 2rem; font-size: 0.9rem;'>
--- 学生信息查询系统 · 数据仅供参考 ---
</div>
""", unsafe_allow_html=True)
