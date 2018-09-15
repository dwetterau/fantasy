from typing import List

from fantasy import ProjectionSource, Player, Week, Position
from fetch import fetch


class YahooProjectionSource(ProjectionSource):

    def _position_to_str(self, position: Position) -> str:
        if position == Position.QUARTERBACK:
            return "QB"
        elif position == Position.RUNNING_BACK:
            return "RB"
        elif position == Position.WIDE_RECEIVER:
            return "WR"
        elif position == Position.TIGHT_END:
            return "TE"
        elif position == Position.KICKER:
            return "K"
        elif position == Position.DEFENSE:
            return "DEF"

    def _fetch_url(self, position: Position, week: Week, page_num=0) -> str:
        # Sort - PTS is by fantasy points
        # stat1 - S_PW_X = projected points in week X
        # pos = {QB, RB, WR, TE, K, DEF}
        # count = offset (page size of 25)
        return (
            "https://football.fantasysports.yahoo.com/f1/1338663/players?"
            "&sort=PTS&status=ALL&pos={}&stat1=S_PW_{}&jsenabled=0&sdir=1&count={}".format(
                self._position_to_str(position),
                week.num,
                page_num * 25,
            )
        )

    def get_players(self, position: Position, week: Week) -> List[Player]:
        page = fetch(self._fetch_url(position, week))
        print(page)
        pass
