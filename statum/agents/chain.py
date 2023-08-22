from statum.agents import Agent
from collections import OrderedDict
from typing import Dict, overload

class Chain(Agent):
    _agents: Dict[str, Agent]

    @overload
    def __init__(self, *args: Agent) -> None:
        ...

    @overload
    def __init__(self, arg: 'OrderedDict[str, Agent]') -> None:
        ...

    def __init__(self, *args):
        super().__init__()
        if len(args) == 1 and isinstance(args[0], OrderedDict):
            for key, agent in args[0].items():
                self.add_agent(key, agent)
        else:
            for idx, agent in enumerate(args):
                self.add_agent(str(idx), agent)

    def forward(self, input):
        for _, agent in self._agents.items():
            input = agent(input)
        return input

    def append(self, agent: Agent) -> 'Chain':
        r"""Appends a given agent to the end.

        Args:
            agente (Agent): agent to append
        """
        self.add_agent(str(len(self)), agent)
        return self