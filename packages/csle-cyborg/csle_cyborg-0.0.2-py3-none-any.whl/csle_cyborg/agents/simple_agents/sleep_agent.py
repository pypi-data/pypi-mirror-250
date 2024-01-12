# Copyright DST Group. Licensed under the MIT license.
from csle_cyborg.agents.simple_agents.base_agent import BaseAgent
from csle_cyborg.shared.actions.action import Sleep


class SleepAgent(BaseAgent):
    def __init__(self):
        pass

    def train(self, results):
        pass

    def get_action(self, observation, action_space):
        return Sleep()

    def end_episode(self):
        pass

    def set_initial_values(self, action_space, observation):
        pass
