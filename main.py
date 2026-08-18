import streamlit as st
import pandas as pd

# ===================== 页面全局基础配置 =====================
st.set_page_config(
    page_title="学生信息查询系统",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===================== 蓝紫色全局美化CSS =====================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f8f9fa 0%, #e0e7ff 100%);
}
h1 {
    color: #4338ca !important;
    font-weight: 700 !important;
    text-align: center !important;
    margin-top: 2rem !important;
    margin-bottom: 1rem !important;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}
.stContainer {
    background-color: rgba(255, 255, 255, 0.8) !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
    box-shadow: 0 4px 12px rgba(67, 56, 202, 0.15) !important;
    border: 1px solid #c7d2fe !important;
}
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
.stTextInput>div>div>input {
    border-radius: 8px !important;
    border: 1px solid #a5b4fc !important;
    padding: 0.5rem !important;
}
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

# ===================== 会话状态初始化 =====================
if "login_success" not in st.session_state:
    st.session_state.login_success = False
# 存储最新表格，登录后持久保存无需重复上传
if "df_data" not in st.session_state:
    st.session_state.df_data = None

# ===================== 登录账号密码 =====================
ADMIN_USER = "15705181210"
ADMIN_PWD = "1210www"

# ===================== 登录页面 =====================
if not st.session_state.login_success:
    st.markdown("<h1>🔐 系统登录</h1>", unsafe_allow_html=True)
    st.divider()
    with st.container():
        username = st.text_input("账号", placeholder="请输入登录账号")
        password = st.text_input("密码", placeholder="请输入登录密码", type="password")
        login_btn = st.button("登录", type="primary")
        if login_btn:
            if username == ADMIN_USER and password == ADMIN_PWD:
                st.session_state.login_success = True
                st.rerun()
            else:
                st.error("账号或密码错误，请重新输入！")
    st.stop()

# ===================== 登录后主界面 =====================
# 标题+右上角【更新数据】按钮同一行
col_title, col_btn = st.columns([9, 1])
with col_title:
    st.markdown("<h1>📖 学生信息查询系统</h1>", unsafe_allow_html=True)
with col_btn:
    pass
st.divider()

# 右上角折叠展开上传面板（替代st.modal弹窗，兼容旧版本）
with st.expander("📁 更新Excel数据"):
    upload_file = st.file_uploader("仅支持xlsx文件", type=["xlsx"])
    if upload_file is not None:
        try:
            # 第二行作为表头，保留Unnamed、空值显示None
            new_df = pd.read_excel(upload_file, header=1)
            st.session_state.df_data = new_df
            st.success("✅数据更新完成！收起面板即可查询最新数据")
            st.dataframe(new_df.head(10), height=200, use_container_width=True)
        except Exception as e:
            st.error(f"读取失败：{e}")

# 退出登录按钮
if st.button("退出登录"):
    st.session_state.login_success = False
    st.session_state.df_data = None
    st.rerun()

# ========== 兜底：仓库自带Excel（第一次登录没上传时使用） ==========
if st.session_state.df_data is None:
    try:
        st.session_state.df_data = pd.read_excel("student.xlsx", header=1)
    except Exception:
        st.info("首次使用请点开上方【📁 更新Excel数据】上传表格")
        st.stop()

df = st.session_state.df_data

# ========== 核心查询区域（不用点开更新面板，直接查询） ==========
with st.container(border=True):
    st.subheader("🔍 学生信息检索")
    col1, col2 = st.columns(2)
    with col1:
        input_id = st.text_input("请输入学号", placeholder="输入完整学号")
    with col2:
        input_name = st.text_input("请输入姓名", placeholder="输入学生姓名")
    search_btn = st.button("开始查询", type="primary")

if search_btn:
    res_df = df[(df["学号"].astype(str) == input_id) & (df["姓名"] == input_name)]
    if not res_df.empty:
        st.success("✅ 查询成功，匹配信息如下：")
        st.dataframe(res_df, height=350, use_container_width=True)
    else:
        st.warning("⚠️ 未找到对应学生，请核对学号和姓名")

# 底部说明
st.markdown("""
<div style='text-align: center; color: #64748b; margin-top: 2rem; font-size: 0.9rem;'>
学生信息查询系统 | 点开上方更新Excel，更新后会话内永久生效无需重复上传
</div>
""", unsafe_allow_html=True)
