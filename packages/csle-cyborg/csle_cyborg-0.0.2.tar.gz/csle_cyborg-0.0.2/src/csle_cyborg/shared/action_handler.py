# Copyright DST Group. Licensed under the MIT license.
from csle_cyborg.shared.actions.action import Action
from csle_cyborg.shared.observation import Observation


class ActionHandler:
    def __init__(self):
        pass

    def perform(self, action: Action) -> Observation:
        raise NotImplementedError
