from utils.llm_client import LLMClient
from tools.financial_health_checker_tool import FinancialHealthCheckerTool
from utils.tool_executor import ToolExecutor

executor = ToolExecutor()
fhc = FinancialHealthCheckerTool()
executor.register_tools(fhc)
client = LLMClient(tool_executor=executor)

input_ = input()

b = [{"role": "user", "content": input_}]

c = client.chat_with_tool(b)
print(c)