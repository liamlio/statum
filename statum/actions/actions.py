from collections import OrderedDict
from typing import Any, Callable, Optional, Dict, Union, List
from pydantic import BaseModel
from statum.types import Metadata

def _forward_unimplemented(self, *input: Any) -> None:
    """
    Defines the computation performed at every call.
    This function should be overridden by all subclasses.
    """
    raise NotImplementedError(f"action [{type(self).__name__}] is missing the required \"forward\" function")

class Action:
    
    def __init__(self, validators:List[Callable]=[], *args, **kwargs) -> None:
        """
        Initializes internal action state.
        """
        self.validators = validators
        self.LLM = None

    forward: Callable[..., Any] = _forward_unimplemented

    
    def __call__(self, *args: Any, **kwargs: Any):
        """
        Calls the forward function of the action.
        """
        
        # Loop through callbacks and validates at the end

        if not self.validators:
            return self.forward(*args, **kwargs)

        result = self.forward(*args, **kwargs)

        if self.validators:
            for validator in self.validators:
                validator(result)

        self.update_agent_metadata(self, result)
        
        return result

    def add_validator(self, validator:List[Callable]):
        if validator not in self.validators:
            self.validators.append(validator)

    def update_agent_metadata(self, result):
        self.agent_metadata.update_metadata(self, result)
    
    def set_agent_metadata(self, metadata:Metadata):
        self.agent_metadata = metadata
