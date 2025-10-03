from tools.tool import Tool

class FinancialHealthCheckerTool(Tool):
    # Implementation of the financial health checker tool

    def cal_emergency_fund_ratio(current_assets: float, monthly_nondiscreationary_expenses: float):
        return current_assets / monthly_nondiscreationary_expenses

    def cal_net_worth(assets: float, liabilities: float):
        return assets - liabilities

    def cal_liquidity_ratio(current_assets: float, current_liabilities):
        return current_assets / current_liabilities

    def cal_saving_and_investing_ratio(savings: float, investments: float, monthly_income: float):
        return (savings + investments) / monthly_income

    def cal_financial_freedom_ratio(passive_income: float, expenses: float):
        return passive_income / expenses

    def get_schemas(self) -> list[dict]:
        return [

            # Calculate an emergency fund ratio
            {
                "name": "cal_emergency_fund_ratio",
                "description": "Calculate your emergency fund ratio",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "current_assets": {"type": "number"},
                        "monthly_nondiscreationary_expenses": {"type": "number"}
                    },
                    "required": ["current_assets", "monthly_nondiscreationary_expenses"],
                    "additionalProperties": False                    
                },
                "strict": True
            }

            # Calculate a net worth
            {
                "name": "cal_net_worth",
                "description": "Calculate your net worth",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "assets": {"type": "number"},
                        "liabilities": {"type": "number"}
                    },
                    "required": ["assets", "liabilities"],
                    "additionalProperties": False                    
                },
                "strict": True
            }


            # Calculate a liquidity ratio
            {
                "name": "cal_liquidity_ratio",
                "description": "Calculate your liquidity ratio",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "current_assets": {"type": "number"},
                        "current_liabilities": {"type": "number"}
                    },
                    "required": ["current_assets", "current_liabilities"],
                    "additionalProperties": False                    
                },
                "strict": True
            }

            # Calculate a saving and investing ratio
            {
                "name": "cal_saving_and_investing_ratio",
                "description": "Calculate your saving and investing ratio",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "savings": {"type": "number"},
                        "investments": {"type": "number"},
                        "monthly_income": {"type": "number"}
                    },
                    "required": ["savings", "investments", "monthly_income"],
                    "additionalProperties": False                    
                },
                "strict": True
            }


            # Calculate a financial freedom ratio
            {
                "name": "cal_financial_freedom_ratio",
                "description": "Calculate your financial freedom ratio",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "passive_income": {"type": "number"},
                        "expenses": {"type": "number"}
                    },
                    "required": ["passive_income", "expenses"],
                    "additionalProperties": False                    
                },
                "strict": True
            }

        ]
