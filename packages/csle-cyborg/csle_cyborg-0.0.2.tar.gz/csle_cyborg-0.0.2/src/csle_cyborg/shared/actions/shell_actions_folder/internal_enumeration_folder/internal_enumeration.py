# Copyright DST Group. Licensed under the MIT license.
from csle_cyborg.shared.actions.shell_actions_folder.shell_action import ShellAction


class InternalEnumeration(ShellAction):

    def __init__(self, session: int, agent: str = None):
        super().__init__(session, agent)

    def sim_execute(self, state):
        pass
