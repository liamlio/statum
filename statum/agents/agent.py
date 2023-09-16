from collections import OrderedDict
from typing import  Any, Callable, Optional, Union, List
from statum.actions import Action
from statum.types import Metadata

def _forward_unimplemented(self, *input: Any) -> None:
    """
    Defines the computation performed at every call.
    This function should be overridden by all subclasses.
    """
    raise NotImplementedError(f"agent [{type(self).__name__}] is missing the required \"forward\" function")
    

class Agent: # How to make BaseModel meaningful? Can I in the init action set the BaseModel for FastAPI use?

    def __init__(self, validators:List[Callable]=[], *args, **kwargs) -> None:
        """
        Initializes internal agent state and sets up validators.
        """
        super().__setattr__('_agents', OrderedDict())
        super().__setattr__('_actions', OrderedDict())
        super().__setattr__('history', OrderedDict())
        self.metadata = Metadata()
        self.validators = validators
        
        self._add_validators(self.validators)
        
        if self._agents:
            for agent in self._agents.values():
                agent._add_validators(self.validators)
        
        if self.metadata:
            self._set_metadata()

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
        self._set_metadata()
    
    def add_action(self, name: str, action: Optional['Action']) -> None:
        """
        initialize an action to the current agent.
        The action can be accessed as an attribute using the given name.

        Args:
            name (str): name of the action. The action can be
                accessed from this agent using the given name
            action (Agent): action to be added to the agent.
        """
        if not isinstance(action, Action) and action is not None:
            raise TypeError(f"{type(action)} is not an Action subclass")
        elif not isinstance(name, str):
            raise TypeError(f"action name should be a string. Got {type(name)}")
        elif hasattr(self, name) and name not in self._actions:
            raise KeyError(f"attribute '{name}' already exists")
        elif '.' in name:
            raise KeyError(f"action name can't contain \".\", got: {name}")
        elif name == '':
            raise KeyError("action name can't be empty string \"\"")
        self._actions[name] = action
        self._set_metadata()

    def __getattr__(self, name: str) -> Any:
        if '_agents' in self.__dict__:
            agents = self.__dict__['_agents']
            if name in agents:
                return agents[name]
        if '_actions' in self.__dict__:
            actions = self.__dict__['_actions']
            if name in actions:
                return actions[name]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
    
    def __call__(self, *args, **kwargs):
        return self.forward(*args, **kwargs)
    

    def __setattr__(self, name: str, value: Union[Any, 'Agent']) -> None:
        def remove_from(*dicts_or_sets):
            for d in dicts_or_sets:
                if name in d:
                    if isinstance(d, dict):
                        del d[name]
                    else:
                        d.discard(name)

        agents = self.__dict__.get('_agents')
        if isinstance(value, Agent):
            if agents is None:
                raise AttributeError(
                    "cannot assign agent before Module.__init__() call")
            remove_from(self.__dict__, self._agents, self._actions)
            agents[name] = value
        elif agents is not None and name in agents:
            if value is not None:
                raise TypeError("cannot assign '{}' as child agent '{}' "
                                "(statum.Agent or None expected)"
                                .format(type(value), name))
            agents[name] = value
        else:
            actions = self.__dict__.get('_actions')
            if isinstance(value, Action):
                if agents is None:
                    raise AttributeError(
                        "cannot assign action before Module.__init__() call")
                remove_from(self.__dict__, self._agents, self._actions)
                actions[name] = value
            elif actions is not None and name in actions:
                if value is not None and not isinstance(value, Action):
                    raise TypeError("cannot assign '{}' as action '{}' "
                                    "(statum.Action or None expected)"
                                    .format(type(value), name))
                actions[name] = value
            else:
                super().__setattr__(name, value)

    def __delattr__(self, name):
        if name in self._agents:
            del self._agents[name]
        elif name in self._actions:
            del self._actions[name]
        else:
            super().__delattr__(name)

    def _add_validators(self, validators:List[Callable]):
        for validator in validators:
            for action in self._actions.values():
                action.validators.append(validator)
        pass

    def add_validator(self, validator:Callable):
        if validator not in self.validators:
            self.validators.append(validator)
            for action in self._actions.values():
                action.add_validator(validator)
        pass

    def _set_metadata(self):
        for agent in self._agents.values():
            agent.metadata = self.metadata
            agent._set_action_metadata()
        for action in self._actions.values():
            action.set_agent_metadata(self.metadata)
        


# Add subagent
# Set forward, backward, and validate validators to each agent and then action in agent
# Need _agents and _actions dict
# set named caches events and history
# Any use in a caches class in development version? Long term yes for setting custom cache objects and sources
# How to give subagents access to the same caches? -> Set caches iteratively to each agent in _agent? OR 
# Give them all the same cache object from the parent? <- this one

# Don't need retriever class in development
# Add api functionality and all agents have a post method