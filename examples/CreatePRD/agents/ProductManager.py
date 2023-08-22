from statum.agents import Agent
from pydantic import BaseModel, Field
from LLM.openai_function import openai_function
from actions import WritePRD, ReviewPRD, ApprovePRD

LLM = openai_function

class ProductManager(Agent):
    
    def __init__(self):
        super().__init__()
        self.system_prompt: str = ""
    

    def forward(self, query: str):
        
        return 
    
    def monitor(self, action: ReviewPRD):
        pass