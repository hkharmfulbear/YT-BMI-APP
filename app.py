import pickle
from pathlib import Path
import streamlit as st 
from PIL import Image
import pandas as pd
from utils import *
import streamlit_authenticator as stauth


# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")


# --- USER AUTHENTICATION ---
names = ['kumagai']
usernames = ['kumagai']

# load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    "sales_dashboard", "abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    # ---- READ EXCEL ----
    @st.cache
    def get_data_from_excel():
        df = pd.read_excel(
            io="supermarkt_sales.xlsx",
            engine="openpyxl",
            sheet_name="Sales",
            skiprows=3,
            usecols="B:R",
            nrows=1000,
        )
        # Add 'hour' column to dataframe
        df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
        return df

    df = get_data_from_excel()

    # ---- SIDEBAR ----
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")
    st.sidebar.header("Please Filter Here:")
    city = st.sidebar.multiselect(
        "Select the City:",
        options=df["City"].unique(),
        default=df["City"].unique()
    )

    customer_type = st.sidebar.multiselect(
        "Select the Customer Type:",
        options=df["Customer_type"].unique(),
        default=df["Customer_type"].unique(),
    )

    gender = st.sidebar.multiselect(
        "Select the Gender:",
        options=df["Gender"].unique(),
        default=df["Gender"].unique()
    )

    df_selection = df.query(
        "City == @city & Customer_type ==@customer_type & Gender == @gender"
    )

    # ---- MAINPAGE ----
    st.title(":bar_chart: Sales Dashboard")
    st.markdown("##")

    # TOP KPI's
    total_sales = int(df_selection["Total"].sum())
    average_rating = round(df_selection["Rating"].mean(), 1)
    star_rating = ":star:" * int(round(average_rating, 0))
    average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

    left_column, middle_column, right_column = st.columns(3)
    with left_column:
        st.subheader("Total Sales:")
        st.subheader(f"US $ {total_sales:,}")
    with middle_column:
        st.subheader("Average Rating:")
        st.subheader(f"{average_rating} {star_rating}")
    with right_column:
        st.subheader("Average Sales Per Transaction:")
        st.subheader(f"US $ {average_sale_by_transaction}")

    st.markdown("""---""")

    # SALES BY PRODUCT LINE [BAR CHART]
    sales_by_product_line = (
        df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
    )
    fig_product_sales = px.bar(
        sales_by_product_line,
        x="Total",
        y=sales_by_product_line.index,
        orientation="h",
        title="<b>Sales by Product Line</b>",
        color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
        template="plotly_white",
    )
    fig_product_sales.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )

    # SALES BY HOUR [BAR CHART]
    sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
    fig_hourly_sales = px.bar(
        sales_by_hour,
        x=sales_by_hour.index,
        y="Total",
        title="<b>Sales by hour</b>",
        color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
        template="plotly_white",
    )
    fig_hourly_sales.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )


    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
    right_column.plotly_chart(fig_product_sales, use_container_width=True)


    # ---- HIDE STREAMLIT STYLE ----
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
#     st.markdown(hide_st_style, unsafe_allow_html=True)
# df = pd.read_csv("weight_list.csv", index_col=0)

# st.title("wrokout log")

# # img = Image.open("bmi.jpg")
# # st.image(img)

# # Introduction

# st.subheader("登録画面")

# # Input
# date = st.date_input("日付")

# syumoku = st.text_input("メニュー")

# weight = st.number_input("重量", step = 1, format="%d")

# rep = st.number_input("回数", step = 1, format="%d")

# set = st.selectbox("セット番号", pd.DataFrame(["1セット目", "2セット目", "3セット目"]))



# rm = weight*rep/40 + weight




# st.button("保存", key=None, help=None, on_click=onClickSave, args=(df, date, syumoku, weight, rep, set, rm),)

# st.success(f"あなたの最大挙上重量は {rm}kgです。{round(rm *0.80)}kgで8回挙上することで筋力アップが見込めます")


# # Introduction

# st.subheader("可視化画面")

# # 都道府県選択セレクトボックス
# option = st.selectbox(
#     '種目',
#     pd.DataFrame(["ベンチプレス", "スクワット"]))

# # 選択した都道府県データを抽出
# df_syumoku = df[df['syumoku'] == option]
# groups = df_syumoku.groupby("date")
# date_list = []
# rm_list = []
# weight_sum_list = []
# for name, group in groups:
# 	date_list.append(group.date.iloc[0])
# 	rm_list.append(group.rm.max())
# 	weight_sum_list.append(group.weight.sum())
# rm_max_df = pd.DataFrame({"date": date_list, "rm": rm_list, "weight_sum": weight_sum_list})

# st.bar_chart(data=rm_max_df, x="date", y="rm")
# st.line_chart(data=rm_max_df, x="date", y="weight_sum")

# # Table

# st.subheader("table")
# st.table(df)

