"""
Utility functions for LiteLLM integration
"""
import os
from typing import Dict, List, Any, Optional
import litellm
import json
from dotenv import load_dotenv 
from tools.tool import Tool, ToolCall
from utils.tool_executor import ToolExecutor

# Load environment variables
load_dotenv()

class LLMClient:
    """Wrapper class for LiteLLM operations"""


    def __init__(self, model: Optional[str] = None, tool_executor: ToolExecutor = ToolExecutor(), 
                 temperature=0.7, max_tokens=1000):
        self.model = model or os.getenv("DEFAULT_MODEL", "gpt-3.5-turbo")
        self.temperature = temperature
        self.max_tokens = max_tokens

        # set tool executor for tool selection
        self.tool_executor: ToolExecutor = tool_executor

        # Set API keys
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            os.environ["OPENAI_API_KEY"] = openai_key
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if anthropic_key:
            os.environ["ANTHROPIC_API_KEY"] = anthropic_key
        google_key = os.getenv("GOOGLE_API_KEY")
        if google_key:
            os.environ["GOOGLE_API_KEY"] = google_key
        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key:
            os.environ["GROQ_API_KEY"] = groq_key

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
            "content": (
                "You are a professional financial advisor. "
                "You have access to specialized financial calculation tools and should use them whenever they can help you answer the user's question accurately. "
                "Do not explain that you are using a tool. Instead, incorporate the tool's output naturally into your response.\n\n"
                "When answering:\n"
                "1. Briefly restate or clarify the user's question or goal.\n"
                "2. Use tools when needed to perform calculations or gather structured information.\n"
                "3. Present the result in a clear, structured, and educational way.\n\n"
                "Guidelines:\n"
                "- Use simple and clear language suitable for non-experts.\n"
                "- Focus on accuracy and clarity, not verbosity.\n"
                "- Do not provide personalized legal or investment advice.\n"
                "- Do not describe the tool-calling process itself."
            )
        })

        try:
            for turn in range(1, max_turns + 1):
                #print(f"\n=== TURN {turn} === \n{messages}")
                resp = litellm.completion(
                    model=self.model, 
                    messages=messages, 
                    functions=self.tool_executor.tool_schemas, 
                    function_call="auto",
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                )

                msg = resp.choices[0].message
                # print("LLM response:", msg)
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
                    if args is None:
                        args = {}
                    name = getattr(fc, "name", None)
                    result = self.tool_executor.run_tool(name, **args)
                except Exception as e:
                    result = {"error": str(e)}
                    print(result)
                # Return result
                messages.append({"role": "assistant", "content": None, "function_call": {"name": getattr(fc, "name", None), "arguments": getattr(fc, "arguments", "{}")}})
                messages.append({"role": "function", "name": getattr(fc, "name", None), "content": json.dumps(result)})
        except Exception as e:
            # Fallback to normal chat on error
            print(f"Tool selection failed: {e}")
            return self.completion_chat(messages, **kwargs)

def get_available_models() -> List[str]:
    """Get list of available models"""
    return [
        # "gpt-3.5-turbo",
        # "gpt-4",
        # "gpt-4-turbo-preview",
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
