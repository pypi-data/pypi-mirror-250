# Copyright DST Group. Licensed under the MIT license.n
from csle_cyborg.shared.actions.shell_actions_folder.open_connection_folder.credential_access_folder.credential_access import (
    CredentialAccess)


class BruteForceAccess(CredentialAccess):
    def __init__(self, session, agent):
        super().__init__(session, agent)

    def sim_execute(self, state):
        pass
