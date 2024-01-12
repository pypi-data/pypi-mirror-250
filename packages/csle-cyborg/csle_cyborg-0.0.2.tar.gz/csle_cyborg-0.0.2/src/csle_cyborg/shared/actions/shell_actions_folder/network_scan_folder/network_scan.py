# Copyright DST Group. Licensed under the MIT license.
from csle_cyborg.shared.actions.shell_actions_folder.shell_action import ShellAction


class NetworkScan(ShellAction):
    def __init__(self, session, agent, subnet):
        super().__init__(session, agent)
        self.subnet = subnet

    def sim_execute(self, state):
        pass
