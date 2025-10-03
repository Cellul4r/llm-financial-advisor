from utils.llm_client import LLMClient
from tools.financial_health_checker_tool import FinancialHealthCheckerTool

a = LLMClient()

b = FinancialHealthCheckerTool()
a.register_tools(b)
c = input()
c = [{"role": "user", "content": c}]
print(a.chat(c))