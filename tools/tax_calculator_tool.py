from tools.tool import Tool

class TaxCalculatorTool(Tool):

    deduction_information = """
            Standard deductions in Thailand include:
                1. (personal_allowance) Personal allowance : 60,000 THB
                2. (father_and_mother_deduction) father and mother deduction : 30,000 baht per person (parents must be over 60 years old and have an income not exceeding 30,000 baht per year) (both parents and spouse's parents)
                3. (disabled_tax_deduction) Disabled or handicapped tax deductions (father/mother, spouse's father/mother, spouse, children): 60,000 baht per person
                If others you are caring for are disabled or handicapped, you can only claim an additional 60,000 baht (1 person maximum).
                4. (child_deduction) If you have first children: 30,000 baht 
                5. (provident_fund) Provident Fund (PVD): up to 15%% of your monthly salary, but not exceeding 500,000 baht per year.
                6. (social_security_fund) Social Security Fund: up to 9,000 baht per year.
                7. (hoam_loan_interest) Hoam Loan Interest: up to 100,000 baht per year.
                8. (life_insurance_premium) Life Insurance Premium: up to 100,000 baht per year.
                9. (personal_health_insurance_premium) Personal Health Insurance Premium: up to 25,000 baht per year.
                Life insurance and health insurance premiums combined must not exceed 100,000 baht.
                10. (parent_health_insurance_premium) Parent Health Insurance Premium: up to 15,000 baht per year.
                11. (pension_insurance_premiums) Pension insurance premiums: Not to exceed 15%% of annual income, not exceeding 200,000 baht. 
                If not using general life insurance, the total can be combined up to 300,000 baht, and combined with other funds, not to exceed 500,000 baht.
                12. (government_pension_fund) Government Pension Fund (GPF): Not exceeding 15%% of annual income and combined with other funds not exceeding 500,000 baht.
                13. (national_savings_fund) National Savings Fund (NSF): Not exceeding 13,200 baht per year.
                14. (private_teacher_fund) Private Teachers Fund: Not exceeding 15%% of the total annual income and combined with other funds and pension insurance premiums, not exceeding 500,000 baht.
                *** Donations deduction calculate after other deductions. ***
                15. (special_donation) Donations for education, sports, social development and government hospitals: Deduction of 2 times the actual amount paid, but not exceeding 10%% of net income.
                16. (normal_donation) Normal donations: As actually paid, but not exceeding 10%% of net income
                reference: https://www.kasikornbank.com/th/tax/pages/calculate_tax.aspx
            """
    
    def __init__(self):
        pass
    
    def calculate_tax(self, income: float, income_sources: list[str] = [],
                      salary_per_month: float = 0.0,
                      deduction_list: dict[str, float] = {}) -> dict[str, any]:
        
        # basic tax calculation for Thai tax system with normal salary income
        # basic income reduction 50% of income (max 100,000 THB)
        income_reduced = income - min(income * 0.5, 100_000)

        deduction_list = self.validate_deduction_list(income, salary_per_month, deduction_list)
        total_deduction = self.calculate_total_deduction(deduction_list)
        income_reduced = max(0, income_reduced - total_deduction)

        donation_deduction = self.calculate_donate_deduction(income_reduced, deduction_list)
        income_reduced = max(0, income_reduced - donation_deduction)
        print(income_reduced)
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
            "deductions_list": deduction_list,
            "deductions_total": min(income,total_deduction),
            "salary_per_month": salary_per_month,
        }
    
    def validate_deduction_list(self, income: float, salary_per_month: float, 
                                deduction_list: dict[str, float]) -> dict[str, float]:
        if not deduction_list:
            return {}
        
        valid_deductions = {}
        for k, v in deduction_list.items():
            if k == "provident_fund":
                valid_deductions[k] = min(v, salary_per_month * 12 * 0.15, 500_000)
            elif k == "social_security_fund":
                valid_deductions[k] = min(v, 9_000)
            elif k == "hoam_loan_interest" or k == "life_insurance_premium" or k == "parent_health_insurance_premium":
                valid_deductions[k] = min(v, 100_000)
            elif k == "personal_health_insurance_premium":
                valid_deductions[k] = min(v, 25_000)
            elif k == "pension_insurance_premiums" or k == "government_pension_fund" or k == "private_teacher_fund":
                valid_deductions[k] = min(v, income * 0.15, 200_000)
            elif k == "national_savings_fund":
                valid_deductions[k] = min(v, 13_200)
            else:
                valid_deductions[k] = v
        
        return valid_deductions

    def calculate_donate_deduction(self, net_income: float, deduction_list: dict[str, float]) -> float:
        if not deduction_list:
            return 0.0
        
        total_donation = 0.0
        special_donation = deduction_list.get("special_donation", 0)
        normal_donation = deduction_list.get("normal_donation", 0)
        total_donation += min(special_donation * 2, net_income * 0.1)
        total_donation += min(normal_donation, net_income * 0.1)
        return total_donation
    
    def calculate_total_deduction(self, deduction_list: dict[str, float]) -> float:
        if not deduction_list:
            return 0.0
        total_deduction = 0.0
        # pension_insurance_premiums, 
        deduction_fund = 0.0
        for k, v in deduction_list.items():
            if k == "life_insurance_premium" or k == "personal_health_insurance_premium":
                continue
            if k == "pension_insurance_premiums" or k == "provident_fund" or k == "government_pension_fund" or k == "private_teacher_fund" \
                or k == "national_savings_fund":
                continue
            total_deduction += v

        # life insurance and health insurance premiums combined must not exceed 100,000 baht.
        total_deduction += min(100_000, deduction_list.get("life_insurance_premium", 0) + deduction_list.get("personal_health_insurance_premium", 0 ))
        
        for k in ["pension_insurance_premiums", "provident_fund", "government_pension_fund", "private_teacher_fund", "national_savings_fund"]:
            deduction_fund += deduction_list.get(k, 0)
        # deduction fund must not exceed 500,000 baht.
        deduction_fund = min(500_000, deduction_fund)
        total_deduction += deduction_fund
        return total_deduction
    
    def calculate_flat_tax(self, income: float, salary_per_month: float) -> float:
        tax_rate = 0.5 / 100 # 5% tax rate
        tax = (income - (salary_per_month * 12)) * tax_rate
        if tax <= 5000:
            tax = 0
        return tax

    def calculate_progressive_tax(self, net_income: float) -> dict[str, any]:
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
        return {
                    "tax_rate": tax_rate,
                    "tax_amount": tax,
                    "formula": f"({net_income} - {lower_bound_income}) * {tax_rate} + {prev_cumulative_tax}"
                }

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
                        "deduction_list": {
                            "type": "object",
                            "description": f"If user provide you must or send None A dictionary of specific deductions and their amounts that user prompt in. You don't have to calculate % for me just sum them up\n\n Information {self.deduction_information}",
                        }
                    },
                    "required": ["income", "deduction_list"],
                }
            }
        ]
