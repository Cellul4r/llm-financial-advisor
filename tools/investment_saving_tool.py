from tools.tool import Tool
import math
class InvestmentSavingTool(Tool):
    # Implementation of the financial health checker tool
    def get_compound_interest(self, year, rate, principal: float) -> float:
        ans = round((principal*((1+(rate/100))**year)), 2)
        return {"year": year , "rate": rate, "principal": principal, "converted": ans}
    
    def get_seventy_two_rules(self, interest_rate: float) -> float:
        year_for_month = 72/(interest_rate)
        year = math.floor(year_for_month)
        month_for_day= (year_for_month - year)*12
        month = math.floor(month_for_day)
        # day = (month_for_day - month)*7
        # year float = 72 / rate
        # year = floor(year float)
        # moth = (year float - year) * 12
        return {"interest_rate": interest_rate, "year": year, "month": month}
    
    def get_schemas(self) -> list[dict]:
        return [
            {
                "name": "get_compound_interest",
                "description": "calculate compound interest and return 2 decimal places",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "year": {"type": "number"},
                        "rate": {"type": "number"},
                        "principal": {"type": "number"}
                    },
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
                    "required": ["interest_rate"]
                }
            }
        ]