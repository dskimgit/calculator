import streamlit as st
import math

# 앱 제목
st.set_page_config(page_title="AI Calculator", page_icon="🧮", layout="centered")
st.title("🧮 Multi-Function Calculator")

st.markdown("### Choose an operation and input your numbers below 👇")

# 사용자 입력
num1 = st.number_input("Enter the first number:", value=0.0, step=1.0)
num2 = st.number_input("Enter the second number:", value=0.0, step=1.0)

# 연산 선택
operation = st.selectbox(
    "Select operation:",
    ("Addition (+)", "Subtraction (−)", "Multiplication (×)", "Division (÷)",
     "Modular (%)", "Exponentiation (^)", "Logarithm (logₐb)")
)

# 계산 버튼
if st.button("Calculate"):
    try:
        if operation == "Addition (+)":
            result = num1 + num2
        elif operation == "Subtraction (−)":
            result = num1 - num2
        elif operation == "Multiplication (×)":
            result = num1 * num2
        elif operation == "Division (÷)":
            if num2 == 0:
                st.error("❌ Cannot divide by zero!")
                result = None
            else:
                result = num1 / num2
        elif operation == "Modular (%)":
            if num2 == 0:
                st.error("❌ Cannot take modulo with zero!")
                result = None
            else:
                result = num1 % num2
        elif operation == "Exponentiation (^)":
            result = num1 ** num2
        elif operation == "Logarithm (logₐb)":
            if num1 <= 0 or num2 <= 0 or num1 == 1:
                st.error("❌ Base and argument must be positive, and base ≠ 1.")
                result = None
            else:
                result = math.log(num2, num1)
        else:
            result = None

        if result is not None:
            st.success(f"✅ Result: **{result:.6f}**")

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Footer
st.markdown("---")
st.caption("Developed with ❤️ using Streamlit and Python")

