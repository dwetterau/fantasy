from typing import List

from bs4 import BeautifulSoup

from fantasy import ProjectionSource, Week, Position, PlayerStats, Source
from fetch import fetch


class FantasyProsProjectionSource(ProjectionSource):

    def source(self):
        return Source.FANTASY_PROS

    def _fetch_url(self, position: Position, week: Week) -> str:
        position = position.to_short_str().lower()
        if position == "def":
            position = "dst"

        return (
            "https://www.fantasypros.com/nfl/projections/{}.php?week={}".format(
                position,
                week.num,
            )
        )

    def get_players(self, position: Position, week: Week, real: bool) -> List[PlayerStats]:
        if real:
            return []

        stats_to_return = []
        page = fetch(self._fetch_url(position, week))
        html = BeautifulSoup(page, "html.parser")
        players = html.select("table#data tr")

        for player in players:
            name_cell = player.select("td.player-label")
            if not name_cell:
                # Probably a header
                continue
            name = name_cell[0].select("a.player-name")[0].text
            points_raw = player.select("td")[-1].text
            try:
                points = float(points_raw)
            except ValueError:
                points = 0.0

            if points == 0:
                break

            p = PlayerStats(
                name=name,
                position=position,
                week=week,
                points=points,
                real=real,
                source=self.source(),
            )
            stats_to_return.append(p)

        return stats_to_return
