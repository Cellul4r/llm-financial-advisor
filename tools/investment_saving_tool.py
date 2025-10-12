from tools.tool import Tool
import math
class InvestmentSavingTool(Tool):
    # Implementation of the financial health checker tool
    def get_compound_interest(self, year, rate, principal: float) -> float:
        ans = round((principal*((1+(rate/100))**year)), 2)
        print(ans)
        return {"year": year , "rate": rate, "principal": principal, "converted": ans}
    
    def get_seventy_two_rules(self, interest_rate: float) -> float:
        year_for_month = 72/(interest_rate)
        year = math.floor(year_for_month)
        month_for_day= (year_for_month - year)*12
        month = math.floor(month_for_day)
        return {"interest_rate": interest_rate, "year": year, "month": month}
    
    def resolve_month_annuities(principal, rate: float, principal_month: bool=True, rate_month: bool=True) -> dict:

        if principal_month:
            principal = principal * 12
        else:
            principal = principal

        if rate_month:
            annual_rate = ((1 + (rate/100))**12 - 1) * 100
        else:
            annual_rate = rate
        return {"principal": principal, "rate": annual_rate, "rate_month": rate_month, "principal_month": principal_month}
    
    def resolve_month_get_principal(future_money, rate: float, future_money_month: bool=True, rate_month: bool=True) -> dict:

        if future_money_month:
            future_money = future_money * 12
        else:
            future_money = future_money

        if rate_month:
            annual_rate = ((1 + (rate/100))**12 - 1) * 100
        else:
            annual_rate = rate
        return {"future_money": future_money, "rate": annual_rate, "rate_month": rate_month, "future_money_month": future_money_month}
    
    def get_annuities(self, year,principal,rate: float,rate_annual: bool=True) -> float:
        rate = rate/100
        if rate_annual:
            n = 1
        else:
            n = 1
        a = principal*((1+(rate/n))**(n*year) - 1)/(rate/n)
        result = round(a, 2)
        # print(result)
        return {"n": n, "year": year , "rate": rate, "principal": principal, "rate_annual": rate_annual, "converted": result}

    def get_principal(self, year, future_money, rate: float,rate_annual: bool=True) ->float:
        rate = rate/100
        if rate_annual:
            n = 1
        else:
            n = 1
        a = future_money/(((1+(rate/n))**(n*year) - 1)/(rate/n))
        result_principal = round(a, 2)
        # print(result)
        return {"n": n, "year": year , "rate": rate, "future_money": future_money, "rate_annual": rate_annual, "converted": result_principal}
        
    def get_schemas(self) -> list[dict]:
        return [
            {
                "name": "get_compound_interest",
                "description": "Use ONLY when the user deposits a single lump sum (principal one time) and wants to know how much it will grow with compound interest. Do not use if the user is saving every month or every year. Example: 'If I put 10,000 at 5% for 10 years, how much will it be?",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "year": {"type": "number",},
                        "rate": {"type": "number"},
                        "principal": {"type": "number"}
                    },
                    "additionalProperties": False,
                    "required": ["year", "rate", "principal"]
                }
            },
            {
                "name": "get_seventy_two_rules",
                "description": "calculate 72 divide by interest rate to return for calvulate ans to number of year, month, and day that money will double or liability will increase in what time period",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "interest_rate": {"type": "number"}
                    },
                    "additionalProperties": False,
                    "required": ["interest_rate"]
                },
                "strict": True
            },
            {
                "name": "get_annuities",
                "description":  "Use this after resolve_month (if the user provided monthly input) or directly (if the user provided yearly input) and if user do give principal then use this function. This function always expects yearly principal and yearly rate as input. Do not try to resolve monthly values inside this function.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "year": {"type": "number","description":"use as a year only"},
                        "rate": {"type": "number", "description": "yearly rate in percent"},
                        "principal": {"type": "number", "description": "yearly saving amount"},
                        "rate_annual": {"type": "boolean", "description": "if user give a year, rate_annual has a value as True. If not, it's False"}
                    },
                    "additionalProperties": False,
                    "required": ["year", "rate", "principal", "rate_annual"]
                },
                "strict": True
            },
            {
                "name": "resolve_month_annuities",
                "description": "Use ONLY if the user explicitly mentions monthly savings or monthly interest rate. This function wiil be called just one and it converts monthly principal and/or monthly interest into equivalent yearly values. It must be called exactly once before get_annuities. Do not call this if the user already provides yearly saving and yearly rate.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "rate": {"type": "number", "description": "monthly rate in percent"},
                        "principal": {"type": "number", "description": "monthly saving amount"},
                        "rate_month": {"type": "boolean", "description": "if user give a year, rate_month has a value as True. If not, it's False"},
                        "principal_month": {"type": "boolean", "description": "if user give a year, principal_month has a value as True. If not, it's False"},
                    },
                    "additionalProperties": False,
                    "required": ["rate", "principal", "rate_month", "principal_month"]
                },
                "strict": True
            },
            {
                "name": "resolve_month_get_principal",
                "description": "Use ONLY if the user explicitly mentions monthly savings or monthly interest rate. This function wiil be called just one and it converts monthly future_money and/or monthly interest into equivalent yearly values. It must be called exactly once before get_principal. Do not call this if the user already provides yearly saving and yearly rate.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "rate": {"type": "number", "description": "monthly rate in percent"},
                        "future_money": {"type": "number", "description": "monthly future money amount"},
                        "rate_month": {"type": "boolean", "description": "if user give a year, rate_month has a value as True. If not, it's False"},
                        "future_money_month": {"type": "boolean", "description": "if user give a year, future_money_month has a value as True. If not, it's False"},
                    },
                    "additionalProperties": False,
                    "required": ["rate", "future_money", "rate_month", "future_money_month"]
                },
                "strict": True
            },
            {
                "name": "get_principal",
                "description":  "Use this after resolve_month (if the user provided monthly input) or directly (if the user provided yearly input) and if user do not give principal then use this function. This function always expects yearly principal and yearly rate as input. Do not try to resolve monthly values inside this function.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "year": {"type": "number","description":"use as a year only"},
                        "rate": {"type": "number", "description": "yearly rate in percent"},
                        "future_money": {"type": "number", "description": "yearly saving amount"},
                        "rate_annual": {"type": "boolean", "description": "if user give a year, rate_annual has a value as True. If not, it's False"}
                    },
                    "additionalProperties": False,
                    "required": ["year", "rate", "future_money", "rate_annual"]
                },
                "strict": True
            }
        ]
class RiskOfInvestment(Tool):
    def __init__(self):
        self.investments = {
            "ฝากประจำ": {"risk": "ต่ำ", "expected_return": 1.5},
            "ฝากออมทรัพย์": {"risk": "ต่ำ", "expected_return": 0.5},
            "พันธบัตรรัฐบาล": {"risk": "ต่ำ-ปานกลาง", "expected_return": 2.5},
            "ตราสารหนี้เอกชน": {"risk": "ต่ำ-ปานกลาง", "expected_return": 4.0},
            "หุ้นใหญ่": {"risk": "ปานกลาง", "expected_return": 5.0},
            "หุ้นขนาดกลาง": {"risk": "ปานกลาง-สูง", "expected_return": 9.0},
            "หุ้นขนาดเล็ก": {"risk": "สูง", "expected_return": 12.0},
            "หุ้นเติบโต": {"risk": "สูง", "expected_return": 10.0},
            "คริปโต": {"risk": "สูงมาก", "expected_return": 20.0},
            "สกุลเงินดิจิตัล": {"risk": "สูงมาก", "expected_return": 20.0},
            "อสังหาริมทรัพย์": {"risk": "ปานกลาง", "expected_return": 6.0},
            "กองทุนอสังหาริมทรัพย์": {"risk": "ปานกลาง", "expected_return": 6.5},
            "กองทุนรวมหุ้น": {"risk": "สูงมาก", "expected_return": 15.0},
            "กองทุนรวมตลาดเงิน": {"risk": "ต่ำ", "expected_return": 1.5},
            "กองทุนรวมตราสารหนี้": {"risk": "ต่ำ-ปานกลาง", "expected_return": 3.5},
            "กองทุนทรัพย์สินทางเลือก": {"risk": "สูงมาก", "expected_return": 12.0},
            "กองทุนรวมผสม": {"risk": "ปานกลาง-สูง", "expected_return": 7.0},
            "กองทุนรวมดัชนี": {"risk": "ปานกลาง", "expected_return": 6.5},
            "กองทุนรวมตราสารหนี้ระยะสั้น": {"risk": "ต่ำ", "expected_return": 2.0},
            "กองทุนรวมตราสารหนี้ระยะยาว": {"risk": "ต่ำ-ปานกลาง", "expected_return": 4.0},
            "สินค้าโภคภัณฑ์": {"risk": "ปานกลาง-สูง", "expected_return": 7.0},
            "สกุลเงินต่างประเทศ (Forex)": {"risk": "สูง", "expected_return": 15.0},
            "Fixed Deposit": {"risk": "Low",  "expected_return": 1.5},
            "Savings Account": {"risk": "Low", "expected_return": 0.5},
            "Government Bonds": {"risk": "Low-Medium", "expected_return": 2.5},
            "Corporate Bonds": {"risk": "Low-Medium", "expected_return": 4.0},
            "Large-Cap Equities": {"risk": "Medium", "expected_return": 5.0},
            "Mid-Cap Equities": {"risk": "Medium-High", "expected_return": 9.0},
            "Small-Cap Equities": {"risk": "High", "expected_return": 12.0},
            "Growth Equities": {"risk": "High", "expected_return": 10.0},
            "Cryptocurrencies": {"risk": "Very High", "expected_return": 20.0},
            "Real Estate": {"risk": "Medium", "expected_return": 6.0},
            "Real Estate Investment Funds": {"risk": "Medium", "expected_return": 6.5},
            "Equity Mutual Funds": {"risk": "Very High", "expected_return": 15.0},
            "Money Market Funds": {"risk": "Low", "expected_return": 1.5},
            "Bond Mutual Funds": {"risk": "Low-Medium", "expected_return": 3.5},
            "Alternative Investment Funds": {"risk": "Very High", "expected_return": 12.0},
            "Balanced Mutual Funds": {"risk": "Medium-High", "expected_return": 7.0},
            "Index Funds": {"risk": "Medium", "expected_return": 6.5},
            "Short-Term Bond Funds": {"risk": "Low", "expected_return": 2.0},
            "Long-Term Bond Funds": {"risk": "Low-Medium", "expected_return": 4.0},
            "Commodities": {"risk": "Medium-High", "expected_return": 7.0},
            "Foreign Exchange (Forex)": {"risk": "High", "expected_return": 15.0},
        }
    def get_investment_info(self, investment_name: str) -> dict[str, dict[str,any]]:
       
        return {"investment_name": investment_name, "info": self.investments.get(investment_name, None)}

    def compare_investments(self, invest1: str, invest2: str) -> dict:

        info1 = self.get_investment_info(invest1)
        info2 = self.get_investment_info(invest2)

        return {
            "investment_1": {"name": invest1, "info": info1},
            "investment_2": {"name": invest2, "info": info2},
        }
    
    def get_schemas(self):
            return [
                {
                    "name": "get_risk_info",
                    "description": "Give info of risk and expected_return of each type of investments",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "investment_name": {"type": "string"}
                        },
                        "required": ["investment_name"],
                        "additionalProperties": False
                    },
                },
                {
                    "name": "compare_investments",
                    "description": "Give info of risk and expected_return of each type of investments and let it compares to find what is better",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "invest1": {"type": "string"},
                            "invest2": {"type": "string"}
                        },
                        "required": ["invest1", "invest2"],
                        "additionalProperties": False
                    },
                },

            ]
