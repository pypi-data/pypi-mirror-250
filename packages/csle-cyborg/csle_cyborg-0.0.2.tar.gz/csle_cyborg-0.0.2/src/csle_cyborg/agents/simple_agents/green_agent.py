import random

from csle_cyborg.agents.simple_agents.base_agent import BaseAgent
from csle_cyborg.shared.actions.action import Sleep
from csle_cyborg.shared.actions.green_actions.green_ping_sweep import GreenPingSweep
from csle_cyborg.shared.actions.green_actions.green_port_scan import GreenPortScan


class GreenAgent(BaseAgent):
    def __init__(self):
        self.action_space = [
            Sleep,
            # GreenPingSweep,
            GreenPortScan,
            # GreenConnection,
        ]
        self.hostnames = [
            'User0',
            'User1',
            'User2',
            'User3',
            'User4',
            'Enterprise0',
            'Enterprise1',
            'Enterprise2',
        ]
        self.subnets = [
            'User',
            'Enterprise',
            'Operational_A',
        ]

    def get_action(self, observation, action_space):
        action = random.choice(self.action_space)
        if action == Sleep:
            return Sleep()
        elif action == GreenPingSweep:
            subnet = random.choice(self.subnets)
            return action(subnet=subnet, session=0, agent='Green')
        else:
            hostname = random.choice(self.hostnames)
            return action(hostname=hostname, session=0, agent='Green')

    def train(self, results):
        pass

    def end_episode(self):
        pass

    def set_initial_values(self, action_space, observation):
        pass
