from tools.tool import Tool

class TaxCalculatorTool(Tool):

    def __init__(self):
        pass
    
    def calculate_flat_tax(self, income: float, salary_per_month: float) -> float:
        tax_rate = 0.5 / 100 # 5% tax rate
        tax = (income - (salary_per_month * 12)) * tax_rate
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
        pass
