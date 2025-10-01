from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class ToolCall:
    name: str
    arguments: str

class Tool(ABC):

    @abstractmethod
    def get_schemas(self) -> list[dict]:
        """Return tool schemas for LLM function calling."""
        pass