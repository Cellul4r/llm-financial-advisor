#!/usr/bin/env python3

from utils.llm_client import LLMClient
from tools.financial_institution_tool import FinancialInstitutionTool
from utils.tool_executor import ToolExecutor
from tests.test import test_tool


msg1 = ["Which bank gives the best interest rate for 12 month fixed deposit?"]
msg2 = ["Which bank gives the best saving account interest rate?"]
msg3 = ["Between scb and KTB, which one gives better 6 month fixed deposit interest rate?"]
msg4 = ["Which bank gives the best fixed_12m deposit rate?"]
msg5 = ["What is the highest interest rate for fixed_3m?"]
msg6 = ["Which bank has the best 12 month fixed deposit rate?"]
msg7 = ["Best 1 year fixed deposit bank?"]
msg8 = ["Who offers the highest 3 month fixed deposit interest?"]
msg9 = ["Show me the best interest for 2 year fixed deposit."]
msg10 = ["Which bank has the best 15 month fixed deposit rate?"]
msg11 = ["Which is best for fixed deposit"]

tool_executor = ToolExecutor()
my_tool = FinancialInstitutionTool()
tool_executor.register_tools(my_tool)

#test_tool(tool_executor, msg1)
#test_tool(tool_executor, msg2)
#test_tool(tool_executor, msg3)
#test_tool(tool_executor, msg4)
#test_tool(tool_executor, msg5)
test_tool(tool_executor, msg6)
#test_tool(tool_executor, msg7)
#test_tool(tool_executor, msg8)
#test_tool(tool_executor, msg9)
#test_tool(tool_executor, msg10)
#test_tool(tool_executor, msg11)




