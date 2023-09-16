import openai
import json

from pydantic import BaseModel
from typing import Optional, Callable, List, cast
from functools import partial
from statum.LLMs import LLM


class openai_function(LLM):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tokenizer = None
        
    def forward(self, query: str, response_model: BaseModel, system_prompt: Optional[str]) -> BaseModel:
        schema = response_model.model_json_schema()
        description = schema.get("description")
        openai_function_schema = {
                "name": response_model.__name__,
                "description": str(description),
                "parameters":schema
                }
        if not system_prompt:
            self.chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo-0613", 
                                                            messages=[{"role": "user", "content": str(query)}],
                                                            functions=[openai_function_schema],
                                                            function_call={"name": response_model.__name__},
                                                            temperature=0,
                                                            )
        else:
            self.chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo-0613", 
                                                            messages=[{"role": "system", "content": system_prompt},
                                                                      {"role": "user", "content": str(query)}],
                                                            functions=[openai_function_schema],
                                                            function_call={"name": response_model.__name__},
                                                            temperature=0,
                                                            )
        output = json.loads(self.chat_completion.choices[0]["message"]["function_call"]["arguments"])
        return response_model.model_validate(output)

    @property
    def total_token_count(self):
        if self.chat_completion:
            return self.chat_completion["usage"]["total_tokens"]
        else:
            return 0
    
    @property
    def input_token_count(self):
        if self.chat_completion:
            return self.chat_completion["usage"]["input_tokens"]
        else:
            return 0
    
    @property
    def output_token_count(self):
        if self.chat_completion:
            return self.chat_completion["usage"]["output_tokens"]
        else:
            return 0