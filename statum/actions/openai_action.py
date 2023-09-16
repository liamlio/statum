from typing import Optional
from pydantic import BaseModel
from statum.actions import Action






class OpenAIFunctionAction(Action):


    def __init__(self, response_model: BaseModel, system_prompt: Optional[str] ) -> None:
        super().__init__()