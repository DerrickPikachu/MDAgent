from langchain.agents.middleware import AgentMiddleware, AgentState
from langgraph.runtime import Runtime
from typing import Any

class LoggerMiddleware(AgentMiddleware):
    def __init__(self):
        super().__init__()
    
    def after_model(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        last_msg = state['messages'][-1].content
        # print(f'[Log] Model Response: {last_msg}')
        if isinstance(last_msg, list):
            for msg in last_msg:
                if msg['type'] != 'tool_use': continue
                print(f'[Log] Tool Call: {msg['name']}, args: {msg['input']}')
        return None
    