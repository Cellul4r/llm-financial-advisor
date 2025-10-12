from tests.test import test_tool
from utils.tool_executor import ToolExecutor
from utils.llm_client import LLMClient
from tools.tax_calculator_tool import TaxCalculatorTool

input_msgs = [
    "Calculate the tax for an income of 3,000,000 deductions of 200,000.",
    "นาย A มีเงินเดือน 50,000 บาท/เดือน (รายได้ทั้งปี 600,000 บาท) รายได้จากทางอื่นอีก  2,000,000 บาท มีค่าลดหย่อนส่วนตัว 60,000 บาท และประกันสังคม 9,000 บาท",
    """นางสาวสุรีย์ (สมรส มีบุตร 1 คน)
        รายได้ต่อปี: 900,000 บาท โบนัส: 100,000 บาท รวมรายได้: 1,000,000 บาท
        ค่าใช้จ่าย: 100,000 บาท (หักเหมา 50% ของรายได้ แต่ไม่เกิน 100,000 บาท)
        ค่าลดหย่อนส่วนตัว: 60,000 บาท ค่าลดหย่อนบุตร: 30,000 บาท
        ค่าลดหย่อนบิดา-มารดา: 60,000 บาท (30,000 บาท/คน)
        ค่าลดหย่อนประกันสังคม: 9,000 บาท
        ค่าลดหย่อนกองทุนสำรองเลี้ยงชีพ: 30,000 บาท
        ค่าลดหย่อนประกันสุขภาพ: 25,000 บาท 
        Calculate tax please""",
    "My annual income is 600,000 baht from salary only. Can you calculate how much tax I need to pay?",
    "I earn 40,000 baht per month, plus 200,000 baht per year from freelance work. How much tax would that be?",
    "I make 900,000 baht a year and donate 50,000 baht to a temple. What’s my tax?",
    "I earn 1,200,000 baht annually. I contribute 10,000 baht to the social security fund and 60,000 baht to a provident fund. Please calculate my tax.",
    "My income is 850,000 baht. I paid 80,000 baht for life insurance, 20,000 baht for health insurance, and 90,000 baht for home loan interest",
    "My salary is 70,000 baht per month, and I donated 30,000 baht to a government hospital. How much tax will I pay?",
    "I earn 50,000 baht monthly, plus 300,000 baht from freelance. I donate 20,000 baht to charity and contribute 100,000 baht to a private teacher fund",
    "My total income is 900,000 baht. I support both my parents and 2 children. How much tax will I owe?",
    "I earned 1,500,000 baht. I paid 200,000 baht for pension insurance premiums and 120,000 baht for life insurance. How much tax do I need to pay?",
    "I make 3,000,000 baht a year. I pay 100,000 baht to the provident fund, 100,000 baht life insurance, 25,000 baht health insurance, and 30,000 baht for donations."
]

tool_executor = ToolExecutor()
tax_tool = TaxCalculatorTool()
tool_executor.register_tools(tax_tool)
llm_client = LLMClient(tool_executor=tool_executor)

test_tool(tool_executor, input_msgs)