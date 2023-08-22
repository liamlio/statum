from collections import OrderedDict
from typing import Optional, Any, List 
from statum.agents import Agent


# WIP

class StateMachine(Agent):
    def __init__(self, *args, **kwargs) -> None:
        super().__setattr__('_agents', OrderedDict())
        self.subscribers = {}  # pub/sub system

    def forward(self, agents: List['Agent']):
        for agent in agents:
            agent.forward()

    def __call__(self, query: str):
        if self._agents:
            first_agent = next(iter(self._agents.values()))
            first_agent(query)

    def subscribe(self, agent: 'Agent', action: str):
        if agent not in self.subscribers:
            self.subscribers[agent] = []
        self.subscribers[agent].append(action)

    def _notify(self, agent: 'Agent', action: str):
        if agent in self.subscribers and action in self.subscribers[agent]:
            for subscriber in self.subscribers[agent]:
                subscriber(action)
