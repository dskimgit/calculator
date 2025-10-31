import streamlit as st
import math

# 페이지 설정
st.set_page_config(page_title="다기능 계산기", page_icon="🧮", layout="centered")

# 앱 제목
st.title("🧮 다기능 계산기")

st.markdown("#### 아래에서 원하는 연산을 선택하세요 👇")

# 1️⃣ 연산 선택
operation = st.selectbox(
    "연산 종류 선택:",
    ("사칙연산 (+, −, ×, ÷)", "나머지 연산 (%)", "지수 연산 (^)", "로그 연산 (logₐb)")
)

st.markdown("---")

# 2️⃣ 입력창 표시 (연산에 따라 다르게)
if operation == "사칙연산 (+, −, ×, ÷)":
    st.subheader("🔢 사칙연산")
    st.write("두 수를 입력하세요.")
    num1 = st.number_input("첫 번째 수:", value=0.0, step=1.0)
    num2 = st.number_input("두 번째 수:", value=0.0, step=1.0)
    op_symbol = st.radio("연산 기호를 선택하세요:", ["+", "−", "×", "÷"])

elif operation == "나머지 연산 (%)":
    st.subheader("🔢 나머지 연산")
    st.write("두 수를 입력하세요. 첫 번째 수를 두 번째 수로 나눈 나머지를 계산합니다.")
    num1 = st.number_input("피제수(나누어지는 수):", value=0.0, step=1.0)
    num2 = st.number_input("제수(나누는 수):", value=1.0, step=1.0)

elif operation == "지수 연산 (^)":
    st.subheader("🔢 지수 연산")
    st.write("밑(base)과 지수(exponent)를 입력하세요. (예: 2의 3제곱 = 8)")
    num1 = st.number_input("밑(base):", value=0.0, step=1.0)
    num2 = st.number_input("지수(exponent):", value=0.0, step=1.0)

elif operation == "로그 연산 (logₐb)":
    st.subheader("🔢 로그 연산")
    st.write("밑(a)과 진수(b)를 입력하세요. logₐb 값을 계산합니다.")
    num1 = st.number_input("밑 (a):", value=10.0, step=1.0)
    num2 = st.number_input("진수 (b):", value=1.0, step=1.0)

# 3️⃣ 계산 버튼
if st.button("계산하기"):
    try:
        if operation == "사칙연산 (+, −, ×, ÷)":
            if op_symbol == "+":
                result = num1 + num2
            elif op_symbol == "−":
                result = num1 - num2
            elif op_symbol == "×":
                result = num1 * num2
            elif op_symbol == "÷":
                if num2 == 0:
                    st.error("❌ 0으로 나눌 수 없습니다.")
                    result = None
                else:
                    result = num1 / num2

        elif operation == "나머지 연산 (%)":
            if num2 == 0:
                st.error("❌ 0으로 나머지 연산을 할 수 없습니다.")
                result = None
            else:
                result = num1 % num2

        elif operation == "지수 연산 (^)":
            result = num1 ** num2

        elif operation == "로그 연산 (logₐb)":
            if num1 <= 0 or num2 <= 0 or num1 == 1:
                st.error("❌ 밑과 진수는 양수여야 하며, 밑은 1이 될 수 없습니다.")
                result = None
            else:
                result = math.log(num2, num1)
        else:
            result = None

        if result is not None:
            st.success(f"✅ 계산 결과: **{result:.6f}**")

    except Exception as e:
        st.error(f"⚠️ 오류가 발생했습니다: {e}")

# Footer
st.markdown("---")
st.caption("© 2025 다기능 계산기 | Streamlit과 Python으로 제작")

