from typing import Any, Callable, Dict, List, Optional, cast
from abc import abstractmethod
from pydantic import Field, BaseModel

# Cache are trackable only at the agent level and can be pulled from any agent
# Buffers are per agent/action for temporary storage - this is where retrieved items are stored per action

# Caches should still be different from buffers because caches are trackable and buffers are not
# Caches are agent storage and buffers are action storage
# caches just trace information from action to action

# Buffers can pull from agent caches
# This is how action can fetch history into a buffer


# Caches are the parent agent level contexts

# Create context objects to pass to actions and/or subagents
# context contains named caches and buffers
# How to include new caches in context?

# Actions don't need memory, just be given the correct inputs lol???
# So Agents need a context object that contains caches and buffers that is passed to subagents

# Agent parent action should be in charge of making sure the correct objects are passed to subagents through the context
# There should just be one shared context

# TODO: Create Context class or general context object for defaults
# TODO: Make general buffer/memory class based on a list for the base class, but can be overwritten through inherantance

# Do I even need the events named cached? Probably not if history is a dict: {action_name:{output}}
# Just needs to be designed with that in mind. So loop mode is good to test with memory done

class Memory(BaseModel):
    """Base class Agent and action Buffers"""

    @abstractmethod
    def put(self, *args, **kwargs):
        pass
    
    @abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abstractmethod
    def delete(self, *args, **kwargs):
        pass

    @abstractmethod
    def update(self, *args, **kwargs):
        pass

   