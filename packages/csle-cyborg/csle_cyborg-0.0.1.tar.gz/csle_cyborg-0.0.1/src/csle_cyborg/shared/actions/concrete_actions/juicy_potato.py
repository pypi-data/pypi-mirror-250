## The following code contains work of the United States Government and is not subject to domestic copyright protection under 17 USC § 105.
## Additionally, we waive copyright and related rights in the utilized code worldwide through the CC0 1.0 Universal public domain dedication.

"""
pertaining to the Juicy Potato permissions escalation action
"""
# pylint: disable=invalid-name
from typing import Tuple

from csle_cyborg.shared.observation import Observation
from csle_cyborg.shared.actions.concrete_actions.escalate_action import EscalateAction
from csle_cyborg.shared.enums import OperatingSystemType
from csle_cyborg.simulator.host import Host
from csle_cyborg.simulator.process import Process
from csle_cyborg.simulator.state import State


class JuicyPotato(EscalateAction):
    """
    Implements the Juicy Potato permissions escalation action
    """
    def sim_execute(self, state: State) -> Observation:
        return self.sim_escalate(state, "SYSTEM")

    def emu_execute(self) -> Observation:
        raise NotImplementedError

    def test_exploit_works(self, target_host: Host) ->\
            Tuple[bool, Tuple[Process, ...]]:
        # the exact patches and OS distributions are described here:
        return target_host.os_type == OperatingSystemType.WINDOWS, ()
