from utils.llm_client import LLMClient
from utils.tool_executor import ToolExecutor
from tools.investment_saving_tool import InvestmentSavingTool 

tool = ToolExecutor()
b = InvestmentSavingTool()
tool.register_tools(b)
a = LLMClient(tool_executor=tool)

m = input()
m =[{"role": "user", "content": m}]
print(a.chat_with_tool(m))
