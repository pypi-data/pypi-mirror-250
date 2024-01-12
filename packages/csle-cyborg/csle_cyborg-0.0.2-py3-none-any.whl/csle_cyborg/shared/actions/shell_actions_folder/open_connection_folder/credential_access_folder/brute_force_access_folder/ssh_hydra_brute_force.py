# Copyright DST Group. Licensed under the MIT license.
from csle_cyborg.shared.actions.shell_actions_folder.open_connection_folder.credential_access_folder.brute_force_access_folder.brute_force_access import BruteForceAccess


class SSHHydraBruteForce(BruteForceAccess):
    def __init__(self, session, agent):
        super().__init__(session, agent)

    def sim_execute(self, state):
        pass