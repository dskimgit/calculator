import streamlit as st
import math
import random
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="다기능 웹앱", page_icon="🌎", layout="wide")

# 🌟 사이드바 메뉴
st.sidebar.title("🔍 기능 선택")
menu = st.sidebar.radio("메뉴를 선택하세요:", ["계산기", "확률 시뮬레이터", "연도별 세계인구 분석"])

# ---------------------------------------------------
# 🧮 계산기
# ---------------------------------------------------
if menu == "계산기":
    st.title("🧮 다기능 계산기")
    operation = st.selectbox("연산 종류 선택:", ("사칙연산 (+, −, ×, ÷)", "나머지 연산 (%)", "지수 연산 (^)", "로그 연산 (logₐb)"))
    st.markdown("---")

    if operation == "사칙연산 (+, −, ×, ÷)":
        num1 = st.number_input("첫 번째 수:", value=0.0)
        num2 = st.number_input("두 번째 수:", value=0.0)
        op = st.radio("연산 기호:", ["+", "−", "×", "÷"])
    elif operation == "나머지 연산 (%)":
        num1 = st.number_input("피제수:", value=0.0)
        num2 = st.number_input("제수:", value=1.0)
    elif operation == "지수 연산 (^)":
        num1 = st.number_input("밑(base):", value=0.0)
        num2 = st.number_input("지수(exponent):", value=0.0)
    elif operation == "로그 연산 (logₐb)":
        num1 = st.number_input("밑(a):", value=10.0)
        num2 = st.number_input("진수(b):", value=1.0)

    if st.button("계산하기"):
        try:
            if operation == "사칙연산 (+, −, ×, ÷)":
                result = {"+" : num1 + num2, "−": num1 - num2, "×": num1 * num2, "÷": num1 / num2 if num2 != 0 else None}.get(op)
                if result is None: st.error("0으로 나눌 수 없습니다.")
                else: st.success(f"✅ 결과: {result:.6f}")
            elif operation == "나머지 연산 (%)":
                if num2 == 0: st.error("0으로 나눌 수 없습니다.")
                else: st.success(f"✅ 결과: {num1 % num2:.6f}")
            elif operation == "지수 연산 (^)":
                st.success(f"✅ 결과: {num1 ** num2:.6f}")
            elif operation == "로그 연산 (logₐb)":
                if num1 <= 0 or num2 <= 0 or num1 == 1: st.error("밑과 진수는 양수, 밑은 1이 될 수 없습니다.")
                else: st.success(f"✅ 결과: {math.log(num2, num1):.6f}")
        except Exception as e:
            st.error(f"오류: {e}")

# ---------------------------------------------------
# 🎲 확률 시뮬레이터
# ---------------------------------------------------
elif menu == "확률 시뮬레이터":
    st.title("🎲 확률 시뮬레이터")
    sim_type = st.radio("시뮬레이션 종류:", ["주사위 🎲", "동전 🪙"])
    n = st.number_input("시행 횟수:", min_value=1, value=1000, step=100)

    if st.button("시뮬레이션 시작"):
        if sim_type == "주사위 🎲":
            results = [random.randint(1, 6) for _ in range(n)]
        else:
            results = [random.choice(["앞면", "뒷면"]) for _ in range(n)]

        df = pd.DataFrame({"결과": results})
        counts = df["결과"].value_counts().sort_index()
        fig = px.bar(x=counts.index, y=counts.values, text=counts.values,
                     labels={"x": "결과", "y": "빈도"}, title=f"{sim_type} {n}회 시뮬레이션 결과")
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

        probs = (counts / n * 100).round(2)
        st.markdown("#### 📊 확률 요약")
        for k, v in probs.items():
            st.write(f"**{k}** → {v}%")

# ---------------------------------------------------
# 🌍 연도별 세계인구 분석
# ---------------------------------------------------
elif menu == "연도별 세계인구 분석":
    st.title("🌍 연도별 세계인구 분석")

    # CSV 불러오기
    df = pd.read_csv("world_population.csv")

    # 대소문자 무시하도록 컬럼 이름 통일
    df.columns = [c.strip() for c in df.columns]
    rename_map = {}
    for c in df.columns:
        if c.lower() == "code": rename_map[c] = "Code"
        if c.lower() == "country": rename_map[c] = "Country"
    df = df.rename(columns=rename_map)

    # 불필요한 열 제거
    if "World Population Percentage" in df.columns:
        df = df.drop(columns=["World Population Percentage"])

    years = ["1970", "1980", "1990", "2000", "2010", "2015", "2020", "2022"]
    year = st.selectbox("연도를 선택하세요:", years)

    if all(col in df.columns for col in ["Country", "Code", year]):
        df_year = df[["Country", "Code", year]].rename(columns={year: "Population"})
        df_year["Population"] = pd.to_numeric(df_year["Population"], errors="coerce").fillna(0)

        fig = px.choropleth(df_year,
                            locations="Code",
                            color="Population",
                            hover_name="Country",
                            color_continuous_scale="YlOrRd",
                            title=f"🌏 {year}년 세계 인구 분포",
                            labels={"Population": "인구수"})
        fig.update_layout(geo=dict(showframe=False, showcoastlines=True, projection_type="natural earth"))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("CSV 열 이름을 확인하세요. (Code, Country, 연도별 컬럼이 필요합니다)")
