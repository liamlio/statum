from statum.memory import Memory
from collections import OrderedDict
from pydantic import BaseModel, Field
from typing import Any, Callable, Dict, List, Optional, cast



class Metadata(BaseModel):
    token_count: int = Field(default=0, alias="token_count")
    action_count: int = Field(default=0, alias="action_count")
    latest_action: str = Field(default=None, alias="latest_action")

class History(Memory):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._history = OrderedDict()
        self.metadata = Metadata()

    def put(self, name, value):
        self._history[name] = value
    
    def get(self, name):
        return self._history[name]

    def delete(self, name):
        self._history[name] = None
    
    def reset(self):
        self._history = OrderedDict()
        self.metadata = Metadata()

    def initialize(self):
        self.reset()
    
    def update_metadata(self, metadata:BaseModel):
        self.metadata.token_count += metadata.token_count
        self.metadata.action_count += metadata.action_count
        self.metadata.latest_action = metadata.latest_action
    
    @classmethod
    def from_default(cls, default: Dict[str, Any]) -> 'History':
        cls = cls()._history = default
        return cls




   

