import openai
import json

from pydantic import BaseModel
from typing import Optional
from statum.LLMs import LLM



class openai_function(LLM):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def forward(self, query: str, responseModel: BaseModel, systemPrompt: Optional[str]) -> BaseModel:
        Model = responseModel
        schema = Model.model_json_schema()
        description = schema.get("description")
        openai_function_schema = {
                "name": responseModel.__name__,
                "description": str(description),
                "parameters":schema
                }
        if not systemPrompt:
            chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo-0613", 
                                                            messages=[{"role": "user", "content": str(query)}],
                                                            functions=[openai_function_schema],
                                                            function_call={"name": responseModel.__name__},
                                                            temperature=0,
                                                            )
        else:
            chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo-0613", 
                                                            messages=[{"role": "system", "content": systemPrompt},
                                                                      {"role": "user", "content": str(query)}],
                                                            functions=[openai_function_schema],
                                                            function_call={"name": responseModel.__name__},
                                                            temperature=0,
                                                            )
        output = json.loads(chat_completion.choices[0]["message"]["function_call"]["arguments"])
        return Model.model_validate(output)
