from typing import Any, Dict, List
# This tool file for test purpose only, not for production use
RATE_TABLE: Dict[str, float] = {
    "USD->THB": 35.0,
    "THB->USD": 0.0286,
    "THB->EUR": 0.025,
    "EUR->THB": 40.0,
    "USD->EUR": 0.92,
    "EUR->USD": 1.087,
}
SUPPORTED = ["USD", "THB", "EUR", "JPY"]
NAME_TO_ISO = {"baht": "THB", "dollar": "USD", "euro": "EUR", "yen": "JPY"}

class CurrencyTools:
    """Currency utilities exposed as tools."""

    # --- Tool 1: list_supported (PROVIDED) ---
    def list_supported(self) -> List[str]:
        return SUPPORTED

    # --- Tool 2: resolve_currency (PROVIDED) ---
    def resolve_currency(self, name_or_code: str) -> str:
        code = (name_or_code or "").strip().upper()
        if code in SUPPORTED:
            return code
        return NAME_TO_ISO.get((name_or_code or "").strip().lower(), "UNKNOWN")

    # --- Tool 3: convert (YOU implement) ---
    def convert(self, amount: float, base: str, quote: str) -> Dict[str, Any]:
        """STUDENT_TODO: use RATE_TABLE to compute result.
        Return dict like: {"rate": , "converted": }.
        If missing rate -> return {"error": f"No rate for {base}->{quote}"}
        """
        rate_str = f"{base}->{quote}"
        if rate_str not in RATE_TABLE:
            print({"error": f"No rate for {rate_str}"})
            return {"error": f"No rate for {rate_str}"}

        rate = RATE_TABLE[rate_str]
        converted_amount: float = amount * rate
        converted_schema: Dict[str, Any] = {
                "amount": amount, 
                "base": base,
                "quote": quote,
                "rate": rate, 
                "converted": converted_amount
                }
        # print json summary formatted
        print("\nParsed: ", converted_schema)
        return converted_schema

    @classmethod
    def get_schemas(cls) -> List[dict]:
        """Return tool schemas (OpenAI-compatible). Fill the TODO for convert."""
        return [
            # 1) list_supported - schema COMPLETE
            {
                "name": "list_supported",
                "description": "Return supported currency ISO codes",
                "parameters": {"type": "object", "properties": {}},
            },
            # 2) resolve_currency - schema COMPLETE
            {
                "name": "resolve_currency",
                "description": "Map currency name or code to ISO code (e.g., 'baht'->'THB')",
                "parameters": {
                    "type": "object",
                    "properties": {"name_or_code": {"type": "string"}},
                    "required": ["name_or_code"],
                    "additionalProperties": False
                },
                "strict": True
            },
            # 3) convert - STUDENT_TODO: COMPLETE THIS SCHEMA
            {
                "name": "convert",
                "description": "Convert amount from base to quote using given fixed RATE_TABLE, don't guess rate or anything else",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "amount": {"type": "number"},
                        "base":   {"type": "string"},
                        "quote":  {"type": "string"},
                    },
                    "required": ["amount", "base", "quote"],
                    "additionalProperties": False
                },
                "strict": True
            }
        ]