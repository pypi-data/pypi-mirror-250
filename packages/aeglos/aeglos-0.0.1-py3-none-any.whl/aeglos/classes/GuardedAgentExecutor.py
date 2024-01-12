from .PromptChecker.PromptChecker import PromptChecker
from langchain.agents import AgentExecutor,Agent
from langchain.tools import BaseTool
from typing import Type

from ..interfaces.GlobalMessages import malicious_input_found_message, suspicious_message_on_invoke

class GuardedAgentExecutor(AgentExecutor):
    prompt_checker = PromptChecker() 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    
    def invoke(self, data):
        """
        Overwriting the invoke function to check for malicious activity.
        Note: this syntax takes in a dictionary as input in the form of input:{input_prompt}
        """
        
        if data["input"] and self.prompt_checker.concurrent_contains_known_attack(data["input"]):
            return {"output":suspicious_message_on_invoke}
        return super().invoke(data)
    
    
def create_secure_tool(tool_instance: BaseTool) -> Type[BaseTool]:

    class SecureTool(tool_instance.__class__):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
        def _run(self, *args, **kwargs):
            """
            Checks the output of the tool for any malicious content recieved.
            If malicious content found, return the error_message
            """
            result=super()._run(*args, **kwargs)
            prompt_checker=PromptChecker()
            if result and prompt_checker.concurrent_contains_known_attack(result):
                return malicious_input_found_message
            
            return result
    
    secure_tool = SecureTool(**tool_instance.dict())
    return secure_tool
    


def guard(agent:Agent, tools:list):
    secure_tools=[create_secure_tool(tool) for tool in tools]
    return GuardedAgentExecutor(agent=agent,tools=secure_tools,verbose=True)