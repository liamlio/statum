from pydantic import BaseModel, Field
from actions import Action
from typing import List, Tuple, Optional
from LLM.openai_function import openai_function

LLM = openai_function

class PRD(BaseModel):
    pass


class WritePRD(Action):
    
    def __init__(self, response_model: BaseModel = PRD, system_prompt: Optional[str] = None):
        super().__init__()
        self.system_prompt = system_prompt
        self.response_model = response_model
    

    def forward(self, query: str):
        response = LLM(query=query, responseModel=self.response_model, system_prompt=self.system_prompt)
        return response