from collections import OrderedDict
from pydantic import BaseModel
from typing import Any, Callable, Optional

Parameter = BaseModel

def _forward_unimplemented(self, *input: Any) -> None:
    """
    Defines the computation performed at every call.
    This function should be overridden by all subclasses.

    Note:
        The recipe for forward pass needs to be defined within
        this function. Call the :class:`action` instance afterwards
        instead of this since the former takes care of running the
        registered hooks while the latter silently ignores them.
    """
    raise NotImplementedError(f"action [{type(self).__name__}] is missing the required \"forward\" function")
    
class Action(BaseModel):
    name: str
    forward_hook: Optional[Callable[..., Any]] = None
    backward_hook: Optional[Callable[..., Any]] = None
    hook: Optional[Callable[..., Any]] = None

    def __init__(self, *args, **kwargs) -> None:
        """
        Initializes internal action state.
        """

        """
        Calls super().__setattr__('a', a) instead of the typical self.a = a
        to avoid action.__setattr__ overhead. action's __setattr__ has special
        handling for parameters, subactions, and caches but simply calls into
        super().__setattr__ for all other attributes.
        """
        super().__setattr__('_parameters', OrderedDict())
        self.forward_hook = kwargs.get('forward_hook')
        self.backward_hook = kwargs.get('backward_hook')
        self.hook = kwargs.get('hook')

    forward: Callable[..., Any] = _forward_unimplemented

    def __getattr__(self, name: str) -> Any:
        """
        Returns the attribute of the action if it exists.
        """
        if '_actions' in self.__dict__:
            actions = self.__dict__['_actions']
            if name in actions:
                return actions[name]
    
    def __call__(self, *args, **kwargs):
        """
        Calls the forward function of the action.
        """
        if self.hook:
            args = self.hook(*args)
        if self.forward_hook:
            args = self.forward_hook(*args)
        result = self.forward(*args, **kwargs)
        if self.backward_hook:
            result = self.backward_hook(result)
        if self.hook:
            result = self.hook(result)
        return result
