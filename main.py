import streamlit as st
import math
import random
import pandas as pd
import plotly.express as px

# 🌍 페이지 기본 설정
st.set_page_config(page_title="다기능 웹앱", page_icon="🌎", layout="wide")

# 🌟 사이드바 메뉴
st.sidebar.title("🔍 기능 선택")
menu = st.sidebar.radio(
    "메뉴를 선택하세요:",
    ["계산기", "확률 시뮬레이터", "연도별 세계인구 분석"]
)

# --------------------------------------------------
# 🧮 계산기 기능
# --------------------------------------------------
if menu == "계산기":
    st.title("🧮 다기능 계산기")
    st.markdown("#### 아래에서 원하는 연산을 선택하세요 👇")

    operation = st.selectbox(
        "연산 종류 선택:",
        ("사칙연산 (+, −, ×, ÷)", "나머지 연산 (%)", "지수 연산 (^)", "로그 연산 (logₐb)")
    )

    st.markdown("---")

    if operation == "사칙연산 (+, −, ×, ÷)":
        st.subheader("🔢 사칙연산")
        num1 = st.number_input("첫 번째 수:", value=0.0, step=1.0)
        num2 = st.number_input("두 번째 수:", value=0.0, step=1.0)
        op_symbol = st.radio("연산 기호 선택:", ["+", "−", "×", "÷"])

    elif operation == "나머지 연산 (%)":
        st.subheader("🔢 나머지 연산")
        num1 = st.number_input("피제수(나누어지는 수):", value=0.0, step=1.0)
        num2 = st.number_input("제수(나누는 수):", value=1.0, step=1.0)

    elif operation == "지수 연산 (^)":
        st.subheader("🔢 지수 연산")
        num1 = st.number_input("밑(base):", value=0.0, step=1.0)
        num2 = st.number_input("지수(exponent):", value=0.0, step=1.0)

    elif operation == "로그 연산 (logₐb)":
        st.subheader("🔢 로그 연산")
        num1 = st.number_input("밑(a):", value=10.0, step=1.0)
        num2 = st.number_input("진수(b):", value=1.0, step=1.0)

    if st.button("계산하기"):
        try:
            if operation == "사칙연산 (+, −, ×, ÷)":
                if op_symbol == "+": result = num1 + num2
                elif op_symbol == "−": result = num1 - num2
                elif op_symbol == "×": result = num1 * num2
                elif op_symbol == "÷":
                    if num2 == 0: st.error("❌ 0으로 나눌 수 없습니다."); result = None
                    else: result = num1 / num2
            elif operation == "나머지 연산 (%)":
                if num2 == 0: st.error("❌ 0으로 나눌 수 없습니다."); result = None
                else: result = num1 % num2
            elif operation == "지수 연산 (^)":
                result = num1 ** num2
            elif operation == "로그 연산 (logₐb)":
                if num1 <= 0 or num2 <= 0 or num1 == 1:
                    st.error("❌ 밑과 진수는 양수여야 하며, 밑은 1이 될 수 없습니다."); result = None
                else: result = math.log(num2, num1)
            else:
                result = None

            if result is not None:
                st.success(f"✅ 계산 결과: **{result:.6f}**")

        except Exception as e:
            st.error(f"⚠️ 오류가 발생했습니다: {e}")

    st.markdown("---")
    st.caption("© 2025 다기능 계산기 | Streamlit & Python")

# --------------------------------------------------
# 🎲 확률 시뮬레이터 기능
# --------------------------------------------------
elif menu == "확률 시뮬레이터":
    st.title("🎲 확률 시뮬레이터")
    st.markdown("#### 주사위 또는 동전을 선택하고 시행 횟수를 입력하세요 👇")

    sim_type = st.radio("시뮬레이션 종류 선택:", ["주사위 🎲", "동전 🪙"])
    n = st.number_input("시행 횟수:", min_value=1, value=1000, step=100)

    if st.button("시뮬레이션 시작"):
        results = []

        if sim_type == "주사위 🎲":
            results = [random.randint(1, 6) for _ in range(n)]
            df = pd.DataFrame({"결과": results})
            counts = df["결과"].value_counts().sort_index()
            fig = px.bar(
                x=counts.index,
                y=counts.values,
                text=counts.values,
                labels={"x": "주사위 눈", "y": "빈도"},
                title=f"주사위 {n}회 시뮬레이션 결과"
            )
            fig.update_traces(textposition='outside')

        elif sim_type == "동전 🪙":
            results = [random.choice(["앞면", "뒷면"]) for _ in range(n)]
            df = pd.DataFrame({"결과": results})
            counts = df["결과"].value_counts()
            fig = px.bar(
                x=counts.index,
                y=counts.values,
                text=counts.values,
                labels={"x": "결과", "y": "빈도"},
                title=f"동전 {n}회 시뮬레이션 결과"
            )
            fig.update_traces(textposition='outside')

        st.plotly_chart(fig, use_container_width=True)
        probs = (counts / n * 100).round(2)
        st.markdown("#### 📊 확률 요약")
        for k, v in probs.items():
            st.write(f"**{k}** → {v}%")

    st.markdown("---")
    st.caption("© 2025 확률 시뮬레이터 | Streamlit & Plotly")

# --------------------------------------------------
# 🌍 연도별 세계인구 분석 기능
# --------------------------------------------------
elif menu == "연도별 세계인구 분석":
    st.title("🌍 연도별 세계인구 분석")
    st.markdown("#### 연도를 선택하면 해당 연도의 세계 인구를 색으로 구분하여 보여줍니다.")

    # CSV 파일 읽기
    df = pd.read_csv("world_population.csv")

    # 연도 선택
    years = ["1970", "1980", "1990", "2000", "2010", "2015", "2020", "2022"]
    year = st.selectbox("연도를 선택하세요:", years)

    # 데이터 확인
    if "Country" in df.columns and year in df.columns:
        df_year = df[["Country", "Code", year]].rename(columns={year: "Population"})

        # 지도 시각화
        fig = px.choropleth(
            df_year,
            locations="Code",
            color="Population",
            hover_name="Country",
            color_continuous_scale="YlOrRd",
            title=f"🌏 {year}년 세계 인구 분포",
            labels={"Population": "인구수"}
        )

        fig.update_layout(
            geo=dict(showframe=False, showcoastlines=True, projection_type="natural earth"),
            coloraxis_colorbar=dict(title="인구수")
        )

        st.plotly_chart(fig, use_container_width=True)

        # 구간별 인구 요약
        st.markdown("### 📊 인구 구간 요약")
        bins = [0, 1_000_000, 10_000_000, 50_000_000, 100_000_000, 500_000_000, 1_500_000_000]
        labels = ["100만 미만", "1천만 미만", "5천만 미만", "1억 미만", "5억 미만", "15억 이상"]
        df_year["구간"] = pd.cut(df_year["Population"], bins=bins, labels=labels, include_lowest=True)
        summary = df_year["구간"].value_counts().sort_index()
        st.bar_chart(summary)
    else:
        st.error("CSV 파일의 형식이 올바르지 않습니다. (Country, Code, 연도별 컬럼이 필요합니다)")

    st.markdown("---")
    st.caption("© 2025 세계인구 분석 | Plotly Choropleth Map")

