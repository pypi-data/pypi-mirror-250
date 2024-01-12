# Copyright DST Group. Licensed under the MIT license.
from csle_cyborg.shared.actions.msf_actions_folder.msf_action import MSFAction
from csle_cyborg.simulator.state import State


class MSFScanner(MSFAction):
    def __init__(self, session, agent):
        super().__init__(session, agent)

    def sim_execute(self, state: State):
        pass
