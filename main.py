import streamlit as st
import pandas as pd

st.title("学生信息查询系统")

df = pd.read_excel("student.xlsx", header=1)

input_xuehao = st.text_input("请输入学号")
input_name = st.text_input("请输入姓名")

if st.button("查询"):
    mask = (df["学号"].astype(str) == str(input_xuehao)) & (df["姓名"] == input_name)
    res = df[mask]
    if len(res) > 0:
        st.dataframe(res)
    else:
        st.warning("未查询到该学生信息，请核对学号、姓名！")
