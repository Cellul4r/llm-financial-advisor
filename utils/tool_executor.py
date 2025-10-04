from tools.tool import Tool

class ToolExecutor:

    def __init__(self):
        self.tools: dict[str, callable] = {}
        self.tool_schemas: list[dict] = []
    
    def register_tool(self, name: str, func: callable, schema: dict):
        self.tools[name] = func
        self.tool_schemas.append(schema)
    
    def register_tools(self, tool_obj: Tool):
        
        for schema in tool_obj.get_schemas():
            name = schema["name"]
            if hasattr(tool_obj, name):
                self.register_tool(name, getattr(tool_obj, name), schema)

    def run_tool(self, name: str, **kwargs):
        if name not in self.tools:
            raise ValueError(f"Tool {name} not registered")
        return self.tools[name](**kwargs)