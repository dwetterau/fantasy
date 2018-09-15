from enum import Enum
from typing import Dict, List


class Week(object):
    num: int

    def __init__(self, num: int):
        self.num = num


class Position(Enum):
    QUARTERBACK = 1
    RUNNING_BACK = 2
    WIDE_RECEIVER = 3
    TIGHT_END = 4
    KICKER = 5
    DEFENSE = 6


class Player(object):
    name: str
    position: Position
    projected_points: Dict[Week, float]
    actual_points: Dict[Week, float]

    def __init__(self, name: str, position: Position):
        self.name = name
        self.position = position

class ProjectionSource(object):

    def get_players(self, position: Position, week: Week) -> List[Player]:
        raise NotImplemented
