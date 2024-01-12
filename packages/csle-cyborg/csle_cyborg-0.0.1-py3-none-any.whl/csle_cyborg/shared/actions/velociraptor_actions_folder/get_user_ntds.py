# Copyright DST Group. Licensed under the MIT license.

from csle_cyborg.shared.enums import QueryType
from csle_cyborg.shared.observation import Observation
from .velociraptor_action import VelociraptorAction


class GetUserNTDS(VelociraptorAction):
    """Get the NT Directory Services file"""

    def __init__(self, session: int, agent: str, hostname: str, username: str):
        super().__init__(session=session,
                         query_type=QueryType.ASYNC,
                         tag=agent)
        self.agent = agent
        self.hostname = hostname
        self.username = username

    def sim_execute(self, state):
        obs = Observation()
        return obs

    def emu_execute(self,
                    session_handler,
                    *args,
                    **kwargs):
        """Execute and action in emulator environment

        Parameters
        ----------
        session_handler : SessionHandler
           session handler object for game session of action (i.e. that
           matches session_id)

        Returns
        -------
        Observation
            Result of performing action
        """
        raise NotImplementedError
