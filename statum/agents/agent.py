from collections import OrderedDict
from pydantic import BaseModel
from typing import  Any, Callable, Optional


def _forward_unimplemented(self, *input: Any) -> None:
    """
    Defines the computation performed at every call.
    This function should be overridden by all subclasses.

    Note:
        The recipe for forward pass needs to be defined within
        this function. Call the :class:`agent` instance afterwards
        instead of this since the former takes care of running the
        registered hooks while the latter silently ignores them.
    """
    raise NotImplementedError(f"agent [{type(self).__name__}] is missing the required \"forward\" function")
    
class Agent(BaseModel):
    forward_hook: Optional[Callable[..., Any]] = None
    backward_hook: Optional[Callable[..., Any]] = None
    hook: Optional[Callable[..., Any]] = None

    def __init__(self, *args, **kwargs) -> None:
        """
        Initializes internal agent state and sets up hooks.
        """
        super().__setattr__('_agents', OrderedDict())
        self.forward_hook = kwargs.get('forward_hook')
        self.backward_hook = kwargs.get('backward_hook')
        self.hook = kwargs.get('hook')

    forward: Callable[..., Any] = _forward_unimplemented

    def add_agent(self, name: str, agent: Optional['Agent']) -> None:
        """
        Adds a child agent to the current agent.
        The agent can be accessed as an attribute using the given name.

        Args:
            name (str): name of the child agent. The child agent can be
                accessed from this agent using the given name
            agent (Agent): child agent to be added to the agent.
        """
        if not isinstance(agent, Agent) and agent is not None:
            raise TypeError(f"{type(agent)} is not a Agent subclass")
        elif not isinstance(name, str):
            raise TypeError(f"agent name should be a string. Got {type(name)}")
        elif hasattr(self, name) and name not in self._agents:
            raise KeyError(f"attribute '{name}' already exists")
        elif '.' in name:
            raise KeyError(f"agent name can't contain \".\", got: {name}")
        elif name == '':
            raise KeyError("agent name can't be empty string \"\"")
        self._agents[name] = agent
        if hasattr(agent, 'forward_hook'):
            agent.forward_hook = self.forward_hook
        if hasattr(agent, 'backward_hook'):
            agent.backward_hook = self.backward_hook
        if hasattr(agent, 'hook'):
            agent.hook = self.hook

    def __getattr__(self, name: str) -> Any:
        if '_agents' in self.__dict__:
            agents = self.__dict__['_agents']
            if name in agents:
                return agents[name]
    
    def __call__(self, *args, **kwargs):
        if self.forward_hook:
            self.forward_hook(*args, **kwargs)
        result = self.forward(*args, **kwargs)
        if self.backward_hook:
            result = self.backward_hook(result)
        return result
