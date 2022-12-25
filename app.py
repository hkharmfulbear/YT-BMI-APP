import streamlit as st 
from PIL import Image
import pandas as pd
from utils import *

df = pd.read_csv("weight_list.csv", index_col=0)

st.title("wrokout log")

# img = Image.open("bmi.jpg")
# st.image(img)

# Introduction

st.subheader("登録画面")

# Input
date = st.date_input("日付")

syumoku = st.text_input("メニュー")

weight = st.number_input("重量", step = 1, format="%d")

rep = st.number_input("回数", step = 1, format="%d")

set = st.selectbox("セット番号", pd.DataFrame(["1セット目", "2セット目", "3セット目"]))



rm = weight*rep/40 + weight




st.button("保存", key=None, help=None, on_click=onClickSave, args=(df, date, syumoku, weight, rep, set, rm),)

st.success(f"あなたの最大挙上重量は {rm}kgです。{round(rm *0.80)}kgで8回挙上することで筋力アップが見込めます")


# Introduction

st.subheader("可視化画面")

# 都道府県選択セレクトボックス
option = st.selectbox(
    '種目',
    pd.DataFrame(["ベンチプレス", "スクワット"]))

# 選択した都道府県データを抽出
df_syumoku = df[df['syumoku'] == option]
groups = df_syumoku.groupby("date")
date_list = []
rm_list = []
weight_sum_list = []
for name, group in groups:
	date_list.append(group.date.iloc[0])
	rm_list.append(group.rm.max())
	weight_sum_list.append(group.weight.sum())
rm_max_df = pd.DataFrame({"date": date_list, "rm": rm_list, "weight_sum": weight_sum_list})

st.bar_chart(data=rm_max_df, x="date", y="rm")
st.line_chart(data=rm_max_df, x="date", y="weight_sum")

# Table

st.subheader("table")
st.table(df)

