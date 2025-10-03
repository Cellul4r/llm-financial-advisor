"""
Utility functions for LiteLLM integration
"""
import os
from typing import Dict, List, Any, Optional
import litellm
import json
from dotenv import load_dotenv 

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

    def register_tools(self, tool_obj):
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
    def chat(self, messages: list[dict], **kwargs):
        # Use LLM function_call if tools exist
        if self.tools and self.tool_schemas:
            try:
                resp = litellm.completion(
                    model=self.model,
                    messages=messages,
                    functions=self.tool_schemas,
                    function_call="auto",  # auto-select tool if needed
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    **kwargs
                )
                msg = resp.choices[0].message
                fc = getattr(msg, "function_call", None)

                # If LLM wants to call a tool
                if fc and getattr(fc, "name", None) in self.tools:
                    args = json.loads(getattr(fc, "arguments", "{}") or "{}")
                    result = self.run_tool(getattr(fc, "name"), **args)
                    # Return tool result as string for simplicity
                    return f"[Tool: {fc.name} executed] Result: {result}"

                # Otherwise, fallback to normal chat
                return getattr(msg, "content", None) or msg.get("content")
            except Exception as e:
                # Fallback to normal chat on error
                print(f"Tool selection failed: {e}")
                return litellm.completion(
                    model=self.model,
                    messages=messages,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    **kwargs
                ).choices[0].message.content
        else:
            # No tools registered → normal chat
            return litellm.completion(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                **kwargs
            ).choices[0].message.content
    

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
