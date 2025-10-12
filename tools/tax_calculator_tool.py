from tools.tool import Tool

class TaxCalculatorTool(Tool):

    def __init__(self):
        pass
    
    def calculate_tax(self, income: float, income_sources: list[str] = [],
                      salary_per_month: float = 0.0, deductions: float = 0.0) -> dict[str, any]:
        # basic tax calculation for Thai tax system with normal salary income
        print(income_sources)
        # basic income reduction 50% of income (max 100,000 THB)
        income_reduced = income - min(income * 0.5, 100_000)
        flat_tax = self.calculate_flat_tax(income, salary_per_month)
        progessive_tax = self.calculate_progressive_tax(income_reduced)

        return {
            "description": """"This function calculates personal income tax according to the Thai tax system. "
            "There are two methods: flat tax and progressive tax. "
            "The progressive tax is calculated based on Thailand’s progressive income tax brackets, "
            "which apply increasing tax rates to different portions of taxable income after "
            "deducting allowable expenses and deductions. The flat tax is based on a fixed rate "
            "applied to income plus salary. The final tax amount is determined by taking the "
            "higher of the two calculated taxes. If one of the tax types is zero, it indicates "
            "that the taxpayer is exempt from that tax type.
            reference tax calculator program: https://www.kasikornbank.com/th/tax/pages/calculate_tax.aspx""",
            "flat_tax": flat_tax,
            "progressive tax": progessive_tax,
            "income": income,
            "deductions": deductions,
            "salary_per_month": salary_per_month,
        }
    
    def calculate_flat_tax(self, income: float, salary_per_month: float) -> float:
        tax_rate = 0.5 / 100 # 5% tax rate
        tax = (income - (salary_per_month * 12)) * tax_rate
        if tax <= 5000:
            tax = 0
        return tax

    def calculate_progressive_tax(self, net_income: float) -> float:
        """
        Calculate the Thai progessive tax based on income, expenses, and deductions.

        Args:
            net income (float): The total net income amount after deductions.
        """
        
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
                            "description": "Total income from all sources eg. Sum of salry, bonus, freelance, etc.",
                        },
                        "income_sources": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
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
                    "required": ["income"],
                    "additionalProperties": False
                }
            }
        ]
