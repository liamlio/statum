from pydantic import BaseModel
from collections import OrderedDict

from typing import Any, Callable

def _forward_unimplemented(self, *input: Any) -> None:
    r"""Defines the computation performed at every call.

    Should be overridden by all subclasses.

    .. note::
        Although the recipe for forward pass needs to be defined within
        this function, one should call the :class:`LLM` instance afterwards
        instead of this since the former takes care of running the
        registered hooks while the latter silently ignores them.
    """
    raise NotImplementedError(f"LLM [{type(self).__name__}] is missing the required \"call\" function")
    
class LLM(BaseModel):
    name: str

    def __init__(self, *args, **kwargs) -> None:
        """
        Initializes internal LLM state
        """
        super().__setattr__('_parameters', OrderedDict())

    forward: Callable[..., Any] = _forward_unimplemented

    def __getattr__(self, name: str) -> Any:
        if '_LLMs' in self.__dict__:
            LLMs = self.__dict__['_LLMs']
            if name in LLMs:
                return LLMs[name]
    
    def __call__(self, *args, **kwargs):
        
        return self.forward(*args, **kwargs)
