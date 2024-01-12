# Copyright DST Group. Licensed under the MIT license.

from csle_cyborg.shared.enums import QueryType
from csle_cyborg.shared.observation import Observation
from .velociraptor_action import VelociraptorAction


class GetOSInfo(VelociraptorAction):

    def __init__(self, session: int, agent: str):
        super().__init__(session=session,
                         query_type=QueryType.ASYNC,
                        agent=agent)
        self.agent = agent

    def sim_execute(self, state):
        obs = Observation()
        return obs
