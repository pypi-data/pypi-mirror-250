# Copyright DST Group. Licensed under the MIT license.
from csle_cyborg.shared.actions.shell_actions_folder.shell_action import ShellAction


class ServiceManipulation(ShellAction):
    def __init__(self, session, agent):
        super().__init__(session, agent)

    def sim_execute(self, state):
        pass