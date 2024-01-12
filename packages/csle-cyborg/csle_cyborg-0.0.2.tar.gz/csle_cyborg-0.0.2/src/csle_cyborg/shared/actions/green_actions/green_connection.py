from csle_cyborg.shared.observation import Observation
from csle_cyborg.shared.actions.action import Action
from csle_cyborg.shared.actions.concrete_actions.blue_keep import BlueKeep
from csle_cyborg.shared.actions.concrete_actions.eternal_blue import EternalBlue
from csle_cyborg.shared.actions.concrete_actions.http_rfi import HTTPRFI
from csle_cyborg.shared.actions.concrete_actions.http_srfi import HTTPSRFI
from csle_cyborg.shared.actions.concrete_actions.ssh_brute_force import SSHBruteForce
from csle_cyborg.shared.actions.msf_actions_folder.msf_action import lo
from csle_cyborg.simulator.session import GreenAbstractSession
from csle_cyborg.simulator.state import State


class GreenConnection(Action):
    def __init__(self, session: int, agent: str, hostname: str):
        super().__init__()
        self.hostname = hostname
        self.agent = agent
        self.session = session

    def sim_execute(self, state: State) -> Observation:
        # find session inside or close to the target subnet
        session = self.session
        # Find ip address of host
        ip_map = state.ip_addresses
        for ip in ip_map:
            if ip_map[ip] == self.hostname:
                self.ip_address = ip
                break

        if type(state.sessions[self.agent][self.session]) is GreenAbstractSession and self.ip_address in \
                state.sessions[self.agent][self.session].ports:
            ports = state.sessions[self.agent][self.session].ports[self.ip_address]
            exploit_options = {EternalBlue: 2.0 if 139 in ports else 0.0,
                               BlueKeep: 1.0 if 3389 in ports else 0.0,
                               HTTPRFI: 3.0 if 80 in ports else 0.0,
                               HTTPSRFI: 4.0 if 443 in ports else 0.0,
                               SSHBruteForce: 0.1 if 22 in ports else 0.0}
            # use information to populate weights for which exploit to select

            # sample the exploit to perform from the exploit weights
            sub_action = list(exploit_options.keys())[
                list(exploit_options.values()).index(max(list(exploit_options.values())))](session=self.session,
                                                                                           agent=self.agent,
                                                                                           ip_address=self.ip_address,
                                                                                           target_session=session)
            obs = sub_action.sim_execute(state)
            if self.ip_address != lo and obs.data['success'] == True:
                hostname = obs.data[str(self.ip_address)]["System info"]["Hostname"]
                os = obs.data[str(self.ip_address)]["System info"]["OSType"]
                state.sessions[self.agent][self.session].addos(hostname, os)
        else:
            obs = Observation(success=False)
        return obs

    def __str__(self):
        return f"{self.__class__.__name__} {self.ip_address}"
