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


class Source(Enum):
    YAHOO = 1


class PlayerStats(object):
    name: str
    position: Position
    week: Week
    points: float
    real: bool
    source: Source

    def __init__(
        self,
        name: str,
        position: Position,
        week: Week,
        points: float,
        real: bool,
        source: Source
    ):
        self.name = name
        self.position = position
        self.week = week
        self.points = points
        self.real = real
        self.source = source


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

    def source(self) -> Source:
        raise NotImplemented

    def get_players(self, position: Position, week: Week, real: bool) -> List[PlayerStats]:
        raise NotImplemented

    def players_all_weeks(self) -> List[PlayerStats]:
        stats = []
        real_weeks = [Week(x) for x in range(1, 4)]
        proj_weeks = [Week(x) for x in range(1, 13)]

        for position in Position:
            for week in real_weeks:
                stats.extend(self.get_players(position, week, real=True))
            for week in proj_weeks:
                stats.extend(self.get_players(position, week, real=False))

        return stats
