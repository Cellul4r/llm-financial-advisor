from utils.llm_client import LLMClient
from tools.financial_loan_tool import FinancialLoanTool
from utils.tool_executor import ToolExecutor
from tests.test import test_tool

executor = ToolExecutor()
fit = FinancialLoanTool()
executor.register_tools(fit)

msg = [
    # Test 1: Basic monthly payment calculation (years)
    #"Calculate my monthly payment for a 500000 baht loan at 5% interest for 5 years",

    #"Calculate my monthly payment for a 500000 baht loan at 0.05 interest for 5 years",
    # Test 2: Monthly payment with months input
   #"What's the monthly payment for a 300000 dollar loan at 4.5% interest for 36 months?",
    
    # Test 3: Monthly payment with bank name
    #"Calculate monthly payment for 1000000 baht loan from SCB at 6% for 10 years",
    
    # Test 4: Monthly payment with flat rate
    #"Calculate monthly payment for 200000 dollar loan at 8% flat rate for 3 years",
    
    # Test 5: Total interest calculation
    #"Calculate total interest for a 500000 baht loan at 5% for 5 years",
    
    # Test 6: Total interest with months
    #"What's the total interest I'll pay on a 400000 dollar loan at 6% for 48 months?",
    
    # Test 7: Compare two loan plans (years)
    #"Compare two loans: Plan A is 500000 baht at 5% for 5 years from KTB, Plan B is 500000 at 4.5% for 6 years from SCB",
    
    # Test 8: Compare loans (months)
    #"Compare 300000 loan at 6% for 36 months vs 300000 at 5.5% for 48 months",
    
    # Test 9: Compare with flat vs effective
    #"Compare Bangkok Bank 200000 at 7% flat rate for 3 years vs Kasikorn 200000 at 7% effective rate for 3 years",
    
    # Test 10: Mixed years and months comparison
    #"Compare loan A: 1000000 baht at 5% for 5 years, loan B: 1000000 at 4.8% for 72 months"
]

test_tool(executor, msg)
