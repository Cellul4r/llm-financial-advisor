from tools.tool import Tool

class FinancialInstitutionTool(Tool):

    BANK_ALIASES = {
        "ktb": "krungthai",
        "krung thai": "krungthai",
        "bkk bank": "krungthep",
        "bangkok bank": "krungthep",
        "scb": "scb",
        "kasikorn": "kasikorn",
        "ttb": "ttb",
        "uob": "UOB",
        "cimb": "CIMB",
    }
    SUPPORTED_BANK = ["krungthep", "krungthai", "kasikorn", "scb", "krungsri", "ttb", "UOB", "CIMB"]

    DEPOSIT_ALIASES = {
        "3 month fixed deposit": "fixed_3m",
        "6 month fixed deposit": "fixed_6m",
        "12 month fixed deposit": "fixed_12m",
        "1 year fixed deposit": "fixed_12m",
        "2 year fixed deposit": "fixed_24m",
        "saving": "saving",
    }
    SUPPORTED_DEPOSITS = {"saving", "fixed_3m", "fixed_6m", "fixed_12m", "fixed_24m"}


    def __init__(self):
        self.interest_data = {
            "krungthep": {"saving": 0.25, "fixed_3m": 0.80, "fixed_6m": 0.85, "fixed_12m": 1.10, "fixed_24m": 1.15},
            "krungthai": {"saving": 0.25, "fixed_3m": 0.80, "fixed_6m": 0.85, "fixed_12m": 1.10, "fixed_24m": 1.10},
            "kasikorn": {"saving": 0.25, "fixed_3m": 0.80, "fixed_6m": 0.85, "fixed_12m": 1.10, "fixed_24m": 1.10},
            "scb": {"saving": 0.25, "fixed_3m": 0.80, "fixed_6m": 0.85, "fixed_12m": 1.10, "fixed_24m": 1.10},
            "krungsri": {"saving": 0.25, "fixed_3m": 0.80, "fixed_6m": 0.90, "fixed_12m": 1.15, "fixed_24m": 1.10},
            "ttb": {"saving": 0.125, "fixed_3m": 0.80, "fixed_6m": 0.90, "fixed_12m": 1.00, "fixed_24m": 1.05},
            "UOB": {"saving": 0.25, "fixed_3m": 0.80, "fixed_6m": 0.85, "fixed_12m": 1.00, "fixed_24m": 1.00},
            "CIMB": {"saving": 0.25, "fixed_3m": 0.80, "fixed_6m": 1.00, "fixed_12m": 1.00, "fixed_24m": 1.10}
        }
        

    
    def resolve_bank(self, name_or_alias: str) -> str:
        key = (name_or_alias or "").strip().lower()
        if key in self.SUPPORTED_BANK:
            return key
        return self.BANK_ALIASES.get((name_or_alias or "").strip().lower(), "UNKNOWN")


    def resolve_deposit(self, term: str) -> str:
        if not term:
            return None

        key = (term or "").strip().lower()

        if key in self.SUPPORTED_DEPOSITS:
            return key

        if key in self.DEPOSIT_ALIASES:
            return self.DEPOSIT_ALIASES[key]

        cleaned = key
        for word in ["deposit", "fixed", "months", "month", "years", "year"]:
            cleaned = cleaned.replace(word, "")
        cleaned = cleaned.strip()

        parts = cleaned.split()
        if parts and parts[0].isdigit():
            return f"fixed_{parts[0]}m"

        return None


    def get_best_fixed(self, deposit_type: str):
        # Step 1: Convert natural language to deposit code (e.g. "12 month fixed deposit" -> "fixed_12m")
        dtype = self.resolve_deposit(deposit_type)

        # Step 2: If we can't resolve it, return an error
        if not dtype:
            return {"error": f"Unknown deposit type '{deposit_type}'"}

        # Step 3: Find the maximum interest rate for this deposit type
        max_rate = -1
        for bank_name, data in self.interest_data.items():
            if dtype in data:
                if data[dtype] > max_rate:
                    max_rate = data[dtype]

        # Step 4: If no bank had this deposit type
        if max_rate == -1:
            return {"error": f"No rates found for deposit type '{deposit_type}'"}

        # Step 5: Collect all banks that offer the max_rate
        best_banks = []
        for bank_name, data in self.interest_data.items():
            if dtype in data and data[dtype] == max_rate:
                best_banks.append(bank_name)

        # Step 6: Return the result
        return {"banks": best_banks, "rate": max_rate}


    def get_best_saving(self):
        # Step 1: Define the deposit type for saving accounts
        dtype = "saving"

        # Step 2: Find the maximum interest rate across all banks
        max_rate = -1
        for bank_name, data in self.interest_data.items():
            if dtype in data:
                if data[dtype] > max_rate:
                    max_rate = data[dtype]

        # Step 3: If no saving rates were found
        if max_rate == -1:
            return {"error": "No saving account rates found."}

        # Step 4: Collect all banks that offer the max_rate
        best_banks = []
        for bank_name, data in self.interest_data.items():
            if dtype in data and data[dtype] == max_rate:
                best_banks.append(bank_name)

        # Step 5: Return result
        return {"banks": best_banks, "rate": max_rate}



    def compare_deposit(self, banks: list[str], deposit_type: str):
        dtype = self.resolve_deposit(deposit_type)
        rate_map = {}
        for b in banks:
            resolved_bank = self.resolve_bank(b)
            bank_data = self.interest_data.get(resolved_bank)
            if not bank_data:
                return {"error": f"Bank '{b}' not found"}
            if dtype not in bank_data:
                return {"error": f"Deposit type '{dtype}' not found for bank '{resolved_bank}'"}
            rate_map[resolved_bank] = bank_data[dtype]

        max_rate = max(rate_map.values())
        best_banks = [b for b, r in rate_map.items() if r == max_rate]
        return {"rates": rate_map, "best_rate": max_rate, "better": best_banks}

    def get_schemas(self) -> list[dict]:
        return [
            {
                "name": "get_best_fixed",
                "description": (
                    "Get the bank(s) offering the best interest rate for a given fixed deposit type. "
                    "The 'deposit_type' parameter can be provided either in code form (e.g. 'fixed_12m') "
                    "or in natural language (e.g. '12 month fixed deposit'). "
                    "If the input is not already formatted, call 'resolve_deposit' to normalize it before comparing rates."),
                "parameters": { 
                    "type": "object",
                    "properties": {
                        "deposit_type": {"type": "string"}
                    },
                    "required": ["deposit_type"],
                    "additionalProperties": False
                },
                "strict" : True
            },
            {
                "name": "get_best_saving",
                "description": "Get the bank(s) offering the best saving account interest rate.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False
                },
                "strict": True 
            },
            {
                "name": "compare_deposit",
                "description": "Compare interest rates for a given deposit type among multiple banks (supports aliases like 'KTB' or natural language like '12 month fixed deposit').",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "banks": {
                            "type": "array",
                            "items": {"type": "string"},
                            "minItems": 2
                        },
                        "deposit_type": {"type": "string"}
                    },
                    "required": ["banks", "deposit_type"],
                    "additionalProperties": False
                }
            }
        ]
