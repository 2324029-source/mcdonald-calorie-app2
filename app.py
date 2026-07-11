import streamlit as st
import pandas as pd

# -------------------
# ページ設定
# -------------------
st.set_page_config(
    page_title="マクドナルド カロリー計算アプリ",
    page_icon="🍔",
    layout="wide"
)

st.title("🍔 マクドナルド カロリー計算アプリ")
st.write("マクドナルド公式サイトの栄養情報をもとに作成")

# -------------------
# CSV読み込み
# -------------------
df = pd.read_csv("mcdonald_calorie.csv")

# カロリーを数値化
df["カロリー(kcal)"] = pd.to_numeric(df["カロリー(kcal)"])

# -------------------
# カート作成
# -------------------
if "cart" not in st.session_state:
    st.session_state.cart = []

# -------------------
# 商品選択
# -------------------
st.header("商品を追加")

categories = sorted(df["カテゴリー"].unique())

category = st.selectbox(
    "カテゴリー",
    categories
)

filtered = df[df["カテゴリー"] == category]

item = st.selectbox(
    "商品",
    filtered["商品名"].tolist()
)

if st.button("➕ 商品を追加"):
    st.session_state.cart.append(item)
    st.success(f"{item} を追加しました！")

# -------------------
# カート表示
# -------------------
st.divider()

st.header("🛒 選択した商品")

if len(st.session_state.cart) == 0:

    st.info("まだ商品が追加されていません。")

else:

    result = []

    total = 0

    for item in sorted(set(st.session_state.cart)):

        count = st.session_state.cart.count(item)

        calorie = int(
            df.loc[df["商品名"] == item, "カロリー(kcal)"].iloc[0]
        )

        subtotal = calorie * count

        total += subtotal

        result.append({
            "商品名": item,
            "数量": count,
            "カロリー": calorie,
            "小計": subtotal
        })

    result_df = pd.DataFrame(result)

    st.write(result_df)

    st.metric(
        "🔥 合計カロリー",
        f"{total} kcal"
    )

# -------------------
# ボタン
# -------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("🗑️ 全て削除"):
        st.session_state.cart = []
        st.rerun()

with col2:
    if st.button("➖ 最後の商品を削除"):
        if len(st.session_state.cart) > 0:
            st.session_state.cart.pop()
            st.rerun()
