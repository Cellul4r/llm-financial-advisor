# wait for implementation streamlit!!!
"""
Basic Chat Application with LiteLLM
A simple chat interface demonstrating LLM integration with Streamlit
"""
import streamlit as st
import sys
import os
from pathlib import Path
from datetime import datetime
from PIL import Image
# Add project root to path
project_root = Path(__file__).parent
print(project_root)
sys.path.insert(0, str(project_root))
from utils.llm_client import LLMClient
from utils.tool_executor import ToolExecutor
from tools.financial_health_checker_tool import FinancialHealthCheckerTool
from tools.currency_converter_tool import CurrencyTools
from tools.financial_institution_tool import FinancialInstitutionTool
from tools.financial_loan_tool import FinancialLoanTool
from tools.investment_saving_tool import InvestmentSavingTool
from tools.investment_saving_tool import RiskOfInvestment
from tools.tax_calculator_tool import TaxCalculatorTool
from pathlib import Path
import base64

tool_executor = ToolExecutor()
tool_executor.register_tools(FinancialHealthCheckerTool())
tool_executor.register_tools(CurrencyTools())
tool_executor.register_tools(FinancialInstitutionTool())
tool_executor.register_tools(FinancialLoanTool())
tool_executor.register_tools(InvestmentSavingTool())
tool_executor.register_tools(RiskOfInvestment())
tool_executor.register_tools(TaxCalculatorTool())

def init_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "llm_client" not in st.session_state:
        st.session_state.llm_client = None
    if "example_query" not in st.session_state:
        st.session_state.example_query = None
    if "current_mode" not in st.session_state:
        st.session_state.current_mode = "default"


def display_chat_messages():
    """Display all messages from session state"""
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        timestamp = message.get("timestamp", "")
        image = message.get("image", None)
        
        if role == "assistant":
            st.markdown(
                f"""
                <div style='text-align: left; background-color: #F0F0F0;
                            padding: 10px 15px; border-radius: 18px; margin: 4px 0; max-width: 70%;'>
                    {content}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""<div style='text-align: left; color: #888; font-size: 13px;'>{timestamp}</div>
                """,
                unsafe_allow_html=True
            )
        
        elif role == "user":
            st.markdown(
                f"""
                <div style='text-align: right;'>
                    <div style='display: inline-block; background-color: #DCF8C6;
                                padding: 10px 15px; border-radius: 18px; margin: 4px 0; max-width: 70%; word-wrap: break-word;'>
                        {content}
                    </div>
                    <div style='text-align: right; color: #999; font-size: 13px;'>{timestamp}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        if image:
                st.image(image, width=250)


# --- Global Singleton LLMClient ---
LLM_CLIENT = None

def get_llm_client(model_name=None) -> LLMClient:
    global LLM_CLIENT

    if LLM_CLIENT is None:
        LLM_CLIENT = LLMClient(tool_executor=tool_executor)

    if model_name:
        LLM_CLIENT.set_model(model_name)

    return LLM_CLIENT

def main():
    st.set_page_config(
        page_title="Financial Advisor",
        page_icon="💬",
        layout="wide"
    )
    
    # Apply custom background styling
        # Background styling
    st.markdown("""
    <style>
        /* พื้นหลังหลักของแอป */
        .stApp {
            background-color: #f1f9f5;
            padding-top: 0px;
            header[data-testid="stHeader"], div[data-testid="stHeader"]{ background: transparent !important; box-shadow: none !important; }
        }

        /* container ของเนื้อหาทั้งหมด */
        section.main > div {
            background-color: #f1f9f5;
        }

        div.block-container {
            background-color: #f1f9f5;
        }

        /* กล่องข้อความแชท */
        .element-container:has(.stChatMessage) {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 10px;
            margin-bottom: 10px;
            box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.25);
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #fefee0;
            box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.50);
        }
    </style>
    """, unsafe_allow_html=True)

    # แปลง GIF เป็น base64
    gif_path = Path("./resource/img/money.gif")
    with open(gif_path, "rb") as f:
        gif_bytes = f.read()
    gif_base64 = base64.b64encode(gif_bytes).decode()

    # แสดง header พร้อม GIF
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');
        
        .header-container {{
            display: flex;
            justify-content: center; /* center horizontally */
            align-items: center;
        }}
        .header-container img {{
            width: 100px;
            transition: transform 0.3s;
        }}
        .header-container img:hover {{
            transform: scale(1.1);
        }}
        .header-container h1 {{
            margin: 0;
            color: #1a237e;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.2);
        }}
        .description-text {{
            display: flex;
            justify-content: center; /* center horizontally */
            align-items: center;
            font-size: 18px;
            color: #555555;
            font-family: 'Roboto', sans-serif;
        }}
        </style>

        <div class="header-container">
            <img src="data:image/gif;base64,{gif_base64}" alt="Financial Advisor GIF"/>
            <h1>Financial Advisor</h1>
        </div>
        <p class="description-text">
            Chat with <strong>Tanny</strong> — Your intelligent financial advisor, guiding every decision with clarity and confidence.
        </p>
    """, unsafe_allow_html=True)


    # Initialize session state
    init_session_state()
    

    # Sidebar configuration
    with st.sidebar:

        st.markdown("""
        <style>
        /* เลือก header ใน sidebar */
        section[data-testid="stSidebar"] h2 {
            background-color: #4e6e58;  /* สีพื้นหลังเขียวอ่อน */
            padding: 10px 15px;
            border-radius: 20px;
            color: #ffffff;  /* สีตัวอักษร */
            font-weight: 700;
            box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.75);
        }
            /* สไตล์สำหรับ subheader (h3) ใน sidebar */
        section[data-testid="stSidebar"] h3 {
            background-color: #4e6e58;  /* สีเขียวอ่อนกว่าเล็กน้อย */
            padding: 8px 12px;
            border-radius: 15px;
            color: #ffffff;
            font-weight: 700;
            margin-top: 10px;
            box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.75);
        }
        </style>
        """, unsafe_allow_html=True)

        st.header("📖 Category")

        st.markdown(" ")

        st.markdown("""
        <style>
        /* Style เฉพาะปุ่มใน sidebar */
        .stSidebar .stButton>button {
            background-color: #b8ddc3;  /* สีเขียวเข้ม */
            color: darkgreen;               /* สีตัวอักษร */
            border-radius: 16px;        /* ขอบโค้ง */
            padding: 8px 16px;          /* เพิ่มพื้นที่ภายใน */
            border: 2px solid #b8ddc3; /* ขอบเส้น */
            width: 100%;                /* ให้เต็มความกว้างของ sidebar */
            margin-bottom: 8px;         /* เว้นระยะระหว่างปุ่ม */
            font-weight: 1000;           /* ตัวหนา */
            box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.50);
        }

        .stSidebar .stButton>button:hover {
            background-color: #ffffff;  /* สีเข้มขึ้นเมื่อ hover */
        }
        </style>
        """, unsafe_allow_html=True)
        mode_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if st.button("Financial Health Checkup"):
            st.session_state.current_mode = "health"
            health_prompt = """
                You are a professional personal finance analyst specialized in evaluating overall financial health.

                Objective:
                - Help users assess their financial well-being through key financial health ratios.
                - Provide clear, personalized insights into users’ financial stability, liquidity, savings habits, and progress toward financial independence.

                Capabilities:
                - Calculate and interpret important financial ratios:
                    • Emergency Fund Ratio = Current Assets / Monthly Non-Discretionary Expenses
                    • Net Worth = Total Assets - Total Liabilities
                    • Liquidity Ratio = Current Assets / Current Liabilities
                    • Saving & Investing Ratio = (Savings + Investments) / Monthly Income
                    • Financial Freedom Ratio = Passive Income / Total Expenses
                - Explain what each ratio means and how to improve it.
                - Provide benchmarks or healthy ranges for each ratio (e.g., Emergency Fund Ratio ≥ 3–6 months).
                - Give guidance on how to balance spending, saving, and investing to achieve financial stability.

                Example Interpretation:
                - If Emergency Fund Ratio < 3 → You may need to increase your emergency savings.
                - If Financial Freedom Ratio ≥ 1 → You are financially independent.
                - If Liquidity Ratio < 1 → You might struggle to cover short-term liabilities.

                Input Examples:
                - "Calculate my emergency fund ratio. I have 120,000 baht in cash and spend 25,000 per month on necessities."
                - "My assets are 900,000 and liabilities are 350,000. What is my net worth?"
                - "I have 200,000 in savings, 100,000 in investments, and earn 30,000 per month. What’s my saving and investing ratio?"
                - "My passive income is 15,000 and total monthly expenses are 20,000. Am I financially free?"
                - "Evaluate my overall financial health based on these numbers..."

                """

            st.session_state.messages.append({"role": "assistant", "content": health_prompt, "image": "resource/img/tanny_present.png", "timestamp": mode_time})
        
        if st.button("Best Banks for Saving"):
            st.session_state.current_mode = "banks"
            banks_prompt = """
                You are a professional financial advisor specializing in banking products and savings optimization.

                Objective:
                - Help users identify which banks offer the best saving and fixed deposit interest rates.
                - Explain and compare deposit options among major Thai banks clearly and accurately.
                - Assist users in making decisions based on interest rate, deposit type, and duration.

                Capabilities:
                - Retrieve the highest saving account interest rate across all supported Thai banks.
                - Find and compare the best fixed deposit rates for 3-month, 6-month, 12-month, or 24-month terms.
                - Compare interest rates among specific banks (e.g. SCB vs KTB for 12-month fixed deposit).
                - Explain differences between saving and fixed deposit accounts and their benefits.
                - Adapt explanations to user goals (e.g. short-term liquidity vs long-term growth).

                Supported Banks:
                - Krungthai (KTB)
                - Bangkok Bank (BKK Bank)
                - Kasikorn Bank (KBank)
                - Siam Commercial Bank (SCB)
                - Krungsri
                - TTB
                - UOB
                - CIMB

                Supported Deposit Types:
                - "saving"
                - "3 month fixed deposit"
                - "6 month fixed deposit"
                - "12 month fixed deposit"
                - "24 month fixed deposit"

                Input Examples:
                - "Which bank gives the best saving account interest rate?"
                - "Find the best 12 month fixed deposit rate among all banks."
                - "Compare SCB, KTB, and TTB for 6 month fixed deposit."
                - "Which banks have the same best saving rate?"
                - "Explain which bank is best for saving long-term."

                """
            st.session_state.messages.append({"role": "assistant", "content": banks_prompt, "image": "resource/img/tanny_present.png", "timestamp": mode_time})
        
        if st.button("Loan Calculator"):
            st.session_state.current_mode = "loan"
            loan_calculator_prompt = """
                You are a professional financial assistant specialized in loans and personal finance.

                Objective:
                - Help users calculate, analyze, and compare loan options for various financial goals.
                - Provide clear guidance on monthly payments, total interest, and overall cost, considering different loan types and repayment methods.

                Capabilities:
                - Calculate monthly payments for loans with flat or effective (reducing balance) interest rates.
                - Compute total interest and total payment over the life of a loan.
                - Compare multiple loan plans from different banks or with different terms, highlighting the most cost-effective option.
                - Explain loan terms and financial concepts in clear, concise language.
                - Adapt advice to the user's loan amount, interest rate, repayment period, and local banking practices.

                Input Examples:
                - "Calculate my monthly payment for a 500000 baht loan at 5% interest for 5 years"
                - "What's the total interest I'll pay on a 400,000 dollar loan at 6% for 48 months?"
                - "Compare two loans: Plan A is 500,000 baht at 5% for 5 years from KTB, Plan B is 500,000 at 4.5% for 6 years from SCB."
                - "Calculate monthly payment for 200,000 dollar loan at 8% flat rate for 3 years."
                """

            st.session_state.messages.append({"role": "assistant", "content": loan_calculator_prompt, "image": "resource/img/tanny_present.png", "timestamp": mode_time})
            
        if st.button("Investments & Savings"):
            st.session_state.current_mode = "invest"
            investments_savings_prompt = """
                You are a professional financial assistant specialized in investments, savings, and portfolio management.

                Objective:
                - Help users understand, plan, and optimize their investments and savings strategies according to their financial goals and risk tolerance.

                Capabilities:
                - Explain different types of investments (stocks, bonds, mutual funds, ETFs, real estate, commodities, crypto, etc.)

                - Provide expected returns, associated risks, and historical performance insights

                - Suggest diversification strategies and portfolio allocation based on risk tolerance

                - Compare savings options (savings accounts, fixed deposits, money market funds) and explain expected returns and liquidity

                - Assess investment risk and provide guidance for both short-term and long-term planning

                - Explain financial terms in clear, concise, and approachable language

                Input Examples:
                - "Which investment is better for me: a fixed deposit or a growth stock over 5 years?"
                - "Compare risk and return between large-cap stocks and mid-cap stocks."
                - "How should I diversify my portfolio with $50,000 in Thailand?"
                - "Explain the difference between bonds and bond mutual funds and their expected returns."
                """
            st.session_state.messages.append({"role": "assistant", "content": investments_savings_prompt, "image": "resource/img/tanny_present.png", "timestamp": mode_time})
            
        if st.button("Tax Calculator"):
            
            st.session_state.current_mode = "tax"
            tax_calculator_prompt = """
                You are a professional financial assistant specialized in personal and corporate tax analysis.

                Objective:
                - Help users calculate and optimize their tax obligations accurately, clearly, and legally.

                Capabilities:
                - Calculate income tax, VAT, and capital gains tax based on user inputs.
                - Support both personal and business taxation.
                - Provide breakdowns of taxable income, deductions, allowances, and final payable tax.
                - Explain each step of the calculation in clear, concise language.
                - Adapt to different tax systems (e.g., Thai, US, UK) when specified by the user.
                - Suggest legal tax-saving options (e.g., deductions, exemptions, credits).

                Input Examples:
                - "Calculate my Thai personal income tax with 1,200,000 THB annual income and 60,000 THB expenses."
                - "Estimate my corporate tax in the US for $500,000 profit."
                - "Compare tax before and after investment deduction."
                """

            st.session_state.messages.append({"role": "assistant", "content": tax_calculator_prompt, "image": "resource/img/tanny_present.png", "timestamp": mode_time})

        st.markdown("""
        - **Category** is used when the user wants to choose a specific mode to ask questions related to that topic.
        """)

        st.subheader("⚙️ Configuration")
        st.markdown(" ")
        if st.button("Default Question"):
            st.session_state.current_mode = "default"
        st.markdown("""
         - **Default Question** is used when the user wants to see an example sentence on the start page again.
        """)

        st.divider()

        # Clear chat button
        st.subheader("🗑 Clear Chat")
        st.markdown(" ")
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()  # Refresh the app to show cleared chat

        st.divider()
        st.markdown("### 📚 About")
        st.markdown(" ")
        st.markdown("""
        **Welcome to Financial AI Advisor**:
        
        a chat-based platform designed to help you manage and understand your personal finances:
        Through conversation, you can ask questions, explore financial topics, and get instant, easy-to-understand answers.

        The assistant responds naturally to your questions, guiding you step by step so you can make confident and informed financial decisions 
        - all within a single, conversational space
        """)


    # Main chat interface
    # if not st.session_state.llm_client:
    #     st.warning("⚠️ Please initialize a model in the sidebar first!")
    #     return
    st.markdown("""
    <style>
    div.stButton > button {
        background-color: #ffffff;  /* สีเขียวเข้ม */
        color: black;               /* ตัวอักษรขาว */
        border-radius: 18px;        /* ขอบโค้ง */
        border: 0px solid #ffffff;  /* เส้นขอบเข้ม */
        padding: 8px 16px;          /* ระยะห่างภายในปุ่ม */
        font-weight: 600;
        width: 100%;
        transition: all 0.2s ease-in-out;
    }

    div.stButton > button:hover {
        background-color: #e3f2fd;  /* สีเข้มขึ้นเมื่อ hover */
        transform: scale(1.03);     /* ขยายเล็กน้อยตอน hover */
    }
    </style>
    """, unsafe_allow_html=True)

    # Chat input

    # if prompt := st.text_input("Ask Tanny anything...Tanny will automatically search when you need current info! 💸💰"):
    #     input_user(prompt)

    st.markdown(
        """
        <style>
        /* เปลี่ยนสีพื้นหลังของ chat input */
        div[data-testid="stChatInput"] textarea {
            background-color: #4e6e58;  /* สีพื้นหลัง */
            color: #ffffff;             /* สีตัวอักษร */
            border-radius: 18px;        /* ปรับมุมให้โค้ง */
            padding: 9px;        /* ปรับขอบกล่องด้านบน*/
            font-size: 16px;
        }
        /* เปลี่ยน placeholder ให้จางลง */
        div[data-testid="stChatInput"] textarea::placeholder {
            color: rgba(255, 255, 255, 0.65); /* สีขาว 50% ความโปร่งใส */
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    if prompt := st.chat_input("Ask Tanny anything...Tanny will automatically search when you need current info! 💸💰"):
        input_user(prompt)

    
    display_chat_messages()


    # Display existing chat messages

        # --- Example query section ---
    # st.divider()

    mode = st.session_state.current_mode

    if mode == "tax":
        example_queries = [
            "Calculate my income tax for 1,200,000 THB income and 60,000 THB expenses.",
            "Explain how tax deductions work in Thailand.",
            "Compare corporate tax between Thailand and Singapore."
        ]
    elif mode == "invest":
        example_queries = [
            "Is a mixed mutual fund a good choice for moderate investors?",
            "What is the risk of investing in large-cap stocks?",
            "Compare risk and return between bonds and crypto."
        ]
    elif mode == "banks":
        example_queries = [
            "Which bank in Thailand offers the best savings rate?",
            "Compare savings account interest between SCB and KBank.",
            "What are the safest banks for long-term deposits?"
        ]
    elif mode == "loan":
        example_queries = [
            "Calculate my monthly payment for 500,000 baht loan at 5% for 5 years.",
            "Compare loan plans from KBank and SCB.",
            "How much interest will I pay on a 400,000 dollar loan at 6%?"
        ]
    elif mode == "health":
        example_queries = [
            "Check my financial health if I earn 30,000 THB/month and spend 20,000 THB.",
            "How can I improve my debt-to-income ratio?",
            "What’s a healthy emergency fund size?"
        ]
    else:
        example_queries = [
            "🏦 What is tax and why is it important in our daily life",
            "💵 Investing in foreign currencies (Forex)",
            "📈 Comparing Large-Cap Stocks and Mid-Cap Stocks"
        ]

    cols = st.columns(3)
    for i, q in enumerate(example_queries[:3]):
        with cols[i]:
            if st.button(q):
                st.session_state.example_query = q
            

    if st.session_state.example_query:
        input_user(st.session_state.example_query)
        st.session_state.example_query = None
        st.rerun()

def input_user(prompt: str):

    user_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt, "timestamp": user_time})

    # Display user message
    # with st.chat_message("user"):
    st.markdown(
        f"""
        <div style='text-align: right;'>
            <div style='display: inline-block; background-color: #DCF8C6;
                        padding: 10px 15px; border-radius: 18px;
                        margin: 4px 0; max-width: 70%; word-wrap: break-word;'>
                {prompt}
            </div>
        </div>
        <div style='text-align: right; color: #999; font-size: 13px; margin-top: 2px;'>{user_time}</div>
        """,
        unsafe_allow_html=True
    )
        
    # with st.chat_message("assistant"): ทำให้หน้าbot กล่องข้อความมันหาย
    st.image("resource/img/tanny_think.png", width=250)  
    with st.spinner("Tanny is considering..."):
        # Prepare messages for LLM

        messages = [{"role": msg["role"], "content": msg["content"]}
                    for msg in st.session_state.messages]

        # Get response from LLM
        # response = st.session_state.llm_client.chat_with_tool(messages)
        assistant_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        llm_client = get_llm_client()

        try:
            response = llm_client.chat_with_tool(messages)
        except Exception as e:
            response = f"⚠️ Error: {e}"

        # clean up response first จะได้ไม่มีตัวอักษแปลกๆ
        response = response.replace("−", " ")  # แทนที่ minus sign ด้วย space
        response = response.replace("–", " ")  # แทนที่ en dash
        response = response.replace("—", " ")  # แทนที่ em dash

        # Display response
        st.markdown(response)
        st.markdown(
                f"<div style='text-align: left; color: #888; font-size: 13px; margin-top: 5px;'>{assistant_time}</div>",
                unsafe_allow_html=True
        )
        
        # Add assistant response to chat history
        st.session_state.messages.append(
            {"role": "assistant", "content": response,"image": "resource/img/tanny_present.png", "timestamp": assistant_time})
        
if __name__ == "__main__":
    main()