from enum import Enum
from typing import Dict, List


class Week(object):
    num: int

    def __init__(self, num: int):
        self.num = num

    def __str__(self) -> str:
        return "Week-{}".format(self.num)

    def __repr__(self) -> str:
        return self.__str__()


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
        self.projected_points = {}
        self.actual_points = {}

    def __str__(self) -> str:
        return "<Player {}-{} proj:{} actual:{}>".format(
            self.name,
            self.position,
            self.projected_points,
            self.actual_points,
        )

    def __repr__(self) -> str:
        return self.__str__()

    def merge(self, other: "Player"):
        assert other.name == self.name and other.position == self.position
        self.projected_points.update(other.projected_points)
        self.actual_points.update(other.actual_points)


class ProjectionSource(object):

    def get_players(self, position: Position, week: Week) -> List[Player]:
        raise NotImplemented

    def players_all_weeks(self) -> List[Player]:
        players_by_name = {}
        for week in [Week(1), Week(2)]:
            for position in Position:
                players = self.get_players(position, week)
                for p in players:
                    if p.name in players_by_name:
                        players_by_name[p.name].merge(p)
                    else:
                        players_by_name[p.name] = p

        return list(players_by_name.values())
