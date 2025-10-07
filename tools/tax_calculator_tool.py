from tools.tool import Tool

class TaxCalculatorTool(Tool):

    def __init__(self):
        pass
    
    def calculate_tax(self, income: float, expenses: float, 
                      salary_per_month: float = 0.0, deductions: float = 0.0) -> dict[str, any]:
        flat_tax = self.calculate_flat_tax(income, salary_per_month)
        progessive_tax = self.calculate_progressive_tax(income, expenses, deductions)

        return {
            "description": """Finally The tax has 2 type flat and progressive tax use the 
            one with the higher value. If which one is zero tell user that get exception for that type of tax""",
            "flat_tax": flat_tax,
            "progressive tax": progessive_tax,
            "income": income,
            "expenses": expenses,
            "deductions": deductions,
            "salary_per_month": salary_per_month,
        }
    
    def calculate_flat_tax(self, income: float, salary_per_month: float) -> float:
        tax_rate = 0.5 / 100 # 5% tax rate
        tax = (income - (salary_per_month * 12)) * tax_rate
        if tax <= 5000:
            tax = 0
        return tax

    def calculate_progressive_tax(self, income: float, expenses: float, deductions: float = 0.0) -> float:
        """
        Calculate the Thai progessive tax based on income, expenses, and deductions.

        Args:
            income (float): The income amount.
            expenses (float): The total expenses amount.
            deductions (float): The total deductions amount."""
        
        net_income = income - expenses - deductions
        if net_income < 0:
            return {
                "error": "Net income is negative, Your expenses is more than your income. no tax applicable."
            }
        
        if net_income >= 5_000_001:
            tax_rate = 0.35
            prev_cumulative_tax = 1_265_000
            lower_bound_income = 5_000_000
        elif net_income >= 2_000_001:
            tax_rate = 0.30
            prev_cumulative_tax = 365_000
            lower_bound_income = 2_000_000
            lower_bound_income = 2_000_000
        elif net_income >= 1_000_001:
            tax_rate = 0.25
            prev_cumulative_tax = 115_000
            lower_bound_income = 1_000_000
        elif net_income >= 750_001:
            tax_rate = 0.20
            prev_cumulative_tax = 65_000
            lower_bound_income = 750_000
        elif net_income >= 500_001:
            tax_rate = 0.15
            prev_cumulative_tax = 27_500
            lower_bound_income = 500_000
        elif net_income >= 300_001:
            tax_rate = 0.10
            prev_cumulative_tax = 7_500
            lower_bound_income = 300_000
        elif net_income >= 150_001:
            tax_rate = 0.05
            prev_cumulative_tax = 0
            lower_bound_income = 150_000
        else:
            tax_rate = 0.0
            prev_cumulative_tax = 0
            lower_bound_income = 0
        
        tax = (net_income - lower_bound_income) * tax_rate + prev_cumulative_tax
        return tax

    @classmethod
    def get_schemas(self) -> list[dict]:
        return [
            {
                "name": "calculate_tax",
                "description": "Calculate the Thai personal tax based on income, expenses, salary per month, and deductions.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "income": {
                            "type": "number",
                            "description": "The income amount.",
                        },
                        "expenses": {
                            "type": "number",
                            "description": "The total expenses amount.",
                        },
                        "salary_per_month": {
                            "type": "number",
                            "description": "The salary per month amount. Default is 0.0.",
                        },
                        "deductions": {
                            "type": "number",
                            "description": "The total deductions amount. Default is 0.0.",
                        },
                    },
                    "required": ["income", "expenses"],
                    "additionalProperties": False
                }
            }
        ]
