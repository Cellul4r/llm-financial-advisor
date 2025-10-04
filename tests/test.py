from utils.tool_executor import ToolExecutor
from utils.llm_client import LLMClient
from tools.currency_converter_tool import CurrencyTools
def test_tool(tool_executor: ToolExecutor,values: list[str]) -> None:
    llm_c = LLMClient(tool_executor=tool_executor)
    for v in values:
        msg = [{"role": "user", "content": v}]
        print(v)
        print(llm_c.chat_with_tool(msg))
        print("-"*30 + "finish" +"-"*30)

# msg1 = ["convert 10 US to THB", "convert 300 THB to EUR"]
# tool_executor = ToolExecutor()
# currency_tool = CurrencyTools()
# tool_executor.register_tools(currency_tool)

# test_tool(tool_executor, msg1)
