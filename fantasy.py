import asyncio
import concurrent.futures

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

    def to_short_str(self) -> str:
        if self == Position.QUARTERBACK:
            return "QB"
        elif self == Position.RUNNING_BACK:
            return "RB"
        elif self == Position.WIDE_RECEIVER:
            return "WR"
        elif self == Position.TIGHT_END:
            return "TE"
        elif self == Position.KICKER:
            return "K"
        elif self == Position.DEFENSE:
            return "DEF"
        raise ValueError

    @classmethod
    def from_short_str(cls, short_str: str) -> 'Position':
        upper = short_str.upper()
        for position in Position:
            if position.to_short_str() == upper:
                return position

        raise ValueError


class Source(Enum):
    YAHOO = 1
    ESPN = 2


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

    def to_csv(self) -> str:
        return ",".join((
            self.name,
            self.position.name,
            str(self.week.num),
            str(self.points),
            "real" if self.real else "proj",
            self.source.name,
        ))


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

    async def players_all_weeks(self) -> List[PlayerStats]:
        stats = []
        real_weeks = [Week(x) for x in range(1, 3)]
        proj_weeks = [Week(x) for x in range(1, 5)]

        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            loop = asyncio.get_event_loop()
            futures = []
            for position in Position:
                for week in real_weeks:
                    futures.append(loop.run_in_executor(
                        executor,
                        self.get_players,
                        position,
                        week,
                        True,
                    ))
                for week in proj_weeks:
                    futures.append(loop.run_in_executor(
                        executor,
                        self.get_players,
                        position,
                        week,
                        False,
                    ))
            for response in await asyncio.gather(*futures):
                stats.extend(response)

        return stats
