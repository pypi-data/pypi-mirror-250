# Copyright DST Group. Licensed under the MIT license.
from csle_cyborg.shared.observation import Observation
from csle_cyborg.shared.actions.global_actions.global_action import GlobalAction


class GlobalEcho(GlobalAction):

    def __init__(self, echo_cmd):
        super().__init__()
        self.cmd = echo_cmd

    def emu_execute(self, team_server) -> Observation:
        raise ValueError("Not implemented")
