from pydantic import BaseModel
from abc import abstractmethod

from typing import Any, Callable

Parameter = BaseModel

def _forward_unimplemented(self, *input: Any) -> None:
    r"""Defines the computation performed at every call.

    Should be overridden by all subclasses.
    """
    raise NotImplementedError(f"LLM [{type(self).__name__}] is missing the required \"call\" function")
    
class LLM:

    def __init__(self, *args, **kwargs) -> None:
        """
        Initializes internal LLM state
        """
        pass

    forward: Callable[..., Any] = _forward_unimplemented
    
    def __call__(self, *args, **kwargs):
        
        return self.forward(*args, **kwargs)
    
    @abstractmethod
    def token_count(self):
        pass



## Need to add LLM name + LLM class tracking in __dict__ and/or _LLM OrderedDict