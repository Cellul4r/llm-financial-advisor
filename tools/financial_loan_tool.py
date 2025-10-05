from tools.tool import Tool

class FinancialLoanTool(Tool):
 
    SUPPORTED = ["flat", "effective"]
    NAME_TO_ISO = {"fixed": "flat", 
                   "reducing": "effective"
                    }

    def resolve_rate_type(self, name_or_type: str) -> str:
        type = (name_or_type or "").strip().upper()
        if type in self.SUPPORTED:
            return type
        return self.NAME_TO_ISO.get((name_or_type or "").strip().lower(), "UNKNOWN")
  
    def cal_monthly_payment(self,loan_amount: float,interest_rate: float,years: int=  None,months: int = None,rate_type: str = None,bank: str = None):
        # Auto resolve rate type if user didn't pick exact word
        if months is not None:
            n = months
        else:
            n = years * 12

        if rate_type == "flat":
            total_interest = loan_amount * (interest_rate / 100) * years
            total_payment = loan_amount + total_interest
            monthly_payment = total_payment / n
            print("monthly_payment is", monthly_payment)
        else:  # effective / reducing balance
            monthly_rate = interest_rate / 100 / 12
            if monthly_rate == 0:   
                monthly_payment = loan_amount / n
            else:
                factor = (1 + monthly_rate) ** n
                monthly_payment = loan_amount * (monthly_rate * factor) / (factor - 1)

        result = {
            "monthly_payment": round(monthly_payment, 2),
            "rate_type": rate_type
        }
        if bank:
            result["bank"] = bank
        return result


    def cal_total_interest(self, loan_amount: float, interest_rate: float, years: int, rate_type: str = "effective"):
        if rate_type == "flat":
            # Total interest for flat = P × r × t
            total_interest = loan_amount * (interest_rate / 100) * years
            total_paid = loan_amount + total_interest
            monthly_payment = total_paid / (years * 12)
        else:
            # Effective (reducing balance)
            monthly_payment = self.cal_monthly_payment(
                loan_amount=loan_amount,
                interest_rate=interest_rate,
                years=years,
                rate_type="effective"
            )["monthly_payment"]
            total_paid = monthly_payment * years * 12
            total_interest = total_paid - loan_amount

        return {
            "total_interest": round(total_interest, 2),
            "total_paid": round(total_paid, 2)
        }

    
    def compare_loan_plans(self, plan1: dict, plan2: dict):
        bank1_name = plan1.get("bank") or "Plan 1"
        bank2_name = plan2.get("bank") or "Plan 2"

        result1 = self.calculate_total_interest(
            plan1["loan_amount"], plan1["interest_rate"], plan1["years"]
        )
        result2 = self.calculate_total_interest(
            plan2["loan_amount"], plan2["interest_rate"], plan2["years"]
        )

        better_bank = bank1_name if result1["total_paid"] < result2["total_paid"] else bank2_name

        return {
            "plan1": {
                "name": bank1_name,
                **result1
            },
            "plan2": {
                "name": bank2_name,
                **result2
            },
            "better_plan": better_bank
        }

    def get_schemas(self) -> list[dict]:
            return [
                {
                    "name": "cal_monthly_payment",
                    "description": """Calculate the monthly payment for a loan. If the rate type (string) is not provided, infer the most likely one from user context (e.g., home loans usually use 'effective'"
                    or car/personal loan usually be "flat"). The bank name is optional.""",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "bank": {"type": "string", "description": "Optional name of the bank."},
                            "loan_amount": {"type": "number", "description": "Total amount of the loan."},
                            "interest_rate": {"type": "number", "description": "Annual interest rate in percent (e.g., 5 for 5%)."},
                            "years": {"type": "integer", "description": "Number of years for the loan."},
                            "rate_type": {"type": "string"}
                        },
                        "required": ["loan_amount", "interest_rate", "years", "rate_type"],
                    }
                                  
                },
                {
                    "name": "cal_total_interest",
                    "description": "Calculate the total interest and total amount paid over the full term of the loan. If the rate type (string) is not provided, infer the most likely one from user context (e.g., home loans usually use 'effective' or car/personal loan usually be 'flat'). The bank name is optional.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "loan_amount": {"type": "number"},
                            "interest_rate": {"type": "number"},
                            "years": {"type": "integer"},
                            "rate_type": {"type": "string"}
                        },
                        "required": ["loan_amount", "interest_rate", "years"]
                    }
                },
                {
                    "name": "compare_loan_plans",
                    "description": "Compare loan offers from two plans or banks. Bank name is optional for both.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "plan1": {
                                "type": "object",
                                "properties": {
                                    "bank": {"type": "string", "description": "Optional name of the first bank."},
                                    "loan_amount": {"type": "number"},
                                    "interest_rate": {"type": "number"},
                                    "years": {"type": "integer"}
                                },
                                "required": ["loan_amount", "interest_rate", "years"]
                            },
                            "plan2": {
                                "type": "object",
                                "properties": {
                                    "bank": {"type": "string", "description": "Optional name of the second bank."},
                                    "loan_amount": {"type": "number"},
                                    "interest_rate": {"type": "number"},
                                    "years": {"type": "integer"}
                                },
                                "required": ["loan_amount", "interest_rate", "years"]
                            }
                        },
                        "required": ["plan1", "plan2"]
                    }
                }
            ]
