"""
Utility functions for LiteLLM integration
"""
import os
from typing import Dict, List, Any, Optional
import litellm
import json
from dotenv import load_dotenv 
from tools.tool import Tool, ToolCall

# Load environment variables
load_dotenv()

class LLMClient:
    """Wrapper class for LiteLLM operations"""


    def __init__(self, model: Optional[str] = None, temperature=0.7, max_tokens=1000):
        self.model = model or os.getenv("DEFAULT_MODEL", "gpt-3.5-turbo")
        self.temperature = temperature
        self.max_tokens = max_tokens

        # set tool schemas and functions
        self.tools: dict[str, callable] = {}
        self.tool_schemas: list[dict] = []

    # --- Tool registration ---
    def register_tool(self, name: str, func: callable, schema: dict):
        self.tools[name] = func
        self.tool_schemas.append(schema)

    def register_tools(self, tool_obj: Tool):
        for schema in getattr(tool_obj, "get_schemas", lambda: [])():
            name = schema["name"]
            if hasattr(tool_obj, name):
                self.register_tool(name, getattr(tool_obj, name), schema)

    # --- Tool execution ---
    def run_tool(self, name: str, **kwargs):
        if name not in self.tools:
            raise ValueError(f"Tool {name} not registered")
        return self.tools[name](**kwargs)

    # --- Chat with optional tool selection ---
    def completion_chat(self, messages: list[Dict[str, str]], **kwargs) -> str:
        """
        Send a chat completion request

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            **kwargs: Additional parameters for the completion

        Returns:
            str: The response content
        """
        try:
            response = litellm.completion(
                model=self.model,
                messages=messages,
                temperature=kwargs.get("temperature", self.temperature),
                max_tokens=kwargs.get("max_tokens", self.max_tokens),
                **kwargs
            )
            return response.choices[0].message.get("content", "")
        except Exception as e:
            return f"Error: {str(e)}"
        
    def chat_with_tool(self, messages: list[Dict[str, str]], max_turns: int = 10, **kwargs) -> str:
        # Use LLM function_call if tools exist
        messages.append({
                        "role": "system",
                        "content": "After you have received results from tools. Now summarize all tool outputs and "
                        "complete the user's instruction in one natural, clear message."
                    })
        
        if self.tools and self.tool_schemas:
            try:
                for turn in range(1, max_turns + 1):
                    print(f"\n=== TURN {turn} === \n{messages}")
                    resp = litellm.completion(
                        model=self.model, 
                        messages=messages, 
                        functions=self.tool_schemas, 
                        function_call="auto",
                        temperature=0.2,
                    )

                    msg = resp.choices[0].message
                    print("LLM response:", msg)
                    fc: ToolCall | None = getattr(msg, "function_call", None)
                    if not fc:
                        return getattr(msg, "content", None) or msg.get("content")
                    # INTERMEDIATE print
                    print(f"=== INTERMEDIATE (turn {turn}) ===")
                    print("name:", getattr(fc, "name", None))
                    print("arguments:", getattr(fc, "arguments", None))

                    # Execute tool
                    try:
                        args = json.loads(getattr(fc, "arguments", "{}") or "{}")
                        name = getattr(fc, "name", None)
                        result = self.run_tool(name, **args)
                        result = self.tools[name](**args) if args else self.tools[name]()
                    except Exception as e:
                        result = {"error": str(e)}
                    # Return result
                    messages.append({"role": "assistant", "content": None, "function_call": {"name": getattr(fc, "name", None), "arguments": getattr(fc, "arguments", "{}")}})
                    messages.append({"role": "function", "name": getattr(fc, "name", None), "content": json.dumps(result)})
            except Exception as e:
                # Fallback to normal chat on error
                print(f"Tool selection failed: {e}")
                return self.completion_chat(messages, **kwargs)
        else:
            # No tools registered → normal chat
            return self.completion_chat(messages, **kwargs)

def get_available_models() -> List[str]:
    """Get list of available models"""
    return [
        "gpt-3.5-turbo",
        "gpt-4",
        "gpt-4-turbo-preview",
        #"claude-3-sonnet-20240229",
        #"claude-3-haiku-20240307",
        #"gemini-pro",
        #"gemini-1.5-pro",
        "groq/llama-3.3-70b-versatile"
    ]

def format_messages(chat_history: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Format chat history for LiteLLM"""
    formatted_messages = []
    for message in chat_history:
        formatted_messages.append({
            "role": message["role"],
            "content": message["content"]
        })
    return formatted_messages
