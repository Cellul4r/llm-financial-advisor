from utils.llm_client import LLMClient
from tools.financial_health_checker_tool import FinancialHealthCheckerTool
from utils.tool_executor import ToolExecutor
from tests.test import test_tool

executor = ToolExecutor()
fhc = FinancialHealthCheckerTool()
executor.register_tools(fhc)
msg = ["please calculate my saving and investing ratio, I have 4000 rupees in savings, 5000 in investments and 3413243 in monthly incomes.",
"please calculate my net worth, I have 10000 dollars in assets and 2000 in liabilities",
"please calculate my liquidity ratio, I have 5000 dollars in assets and 2000 in liabilities",
"please calculate my emergency fund ratio, I have 2000 rupees in assets and 1000 in monthly nondiscreationary expenses",
"please calculate my financial freedom ratio, I have 6000 in passive income and 10000 in expenses",
"please calculate my financial freedom ratio, I have 6000 dollars in passive income and 10000 francs in expenses"]
test_tool(executor, msg)
# client = LLMClient(tool_executor=executor)

# input_ = input()

# b = [{"role": "user", "content": input_}]

# c = client.chat_with_tool(b)
# print(c)