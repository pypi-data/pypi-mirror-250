# Copyright DST Group. Licensed under the MIT license.

from csle_cyborg.shared.actions.game_actions.game_action import GameAction


class GameEcho(GameAction):

    def __init__(self, echo_cmd: str):
        super().__init__()
        self.cmd = echo_cmd
