from typing import List

from bs4 import BeautifulSoup

from fantasy import ProjectionSource, Week, Position, PlayerStats, Source
from fetch import fetch


class YahooProjectionSource(ProjectionSource):

    def source(self):
        return Source.YAHOO

    def _fetch_url(self, position: Position, week: Week, proj=True, page_num=0) -> str:
        # Sort - PTS is by fantasy points
        # stat1 - S_PW_X = projected points in week X
        # pos = {QB, RB, WR, TE, K, DEF}
        # count = offset (page size of 25)
        return (
            "https://football.fantasysports.yahoo.com/f1/1376662/players?"
            "&sort=PTS&status=ALL&pos={}&stat1=S_{}W_{}&jsenabled=0&sdir=1&count={}".format(
                position.to_short_str(),
                "P" if proj else "",
                week.num,
                page_num * 25,
            )
        )

    def get_players(self, position: Position, week: Week, real: bool) -> List[PlayerStats]:
        done = False
        page_num = 0
        stats_to_return = []
        while not done:
            page = fetch(self._fetch_url(position, week, proj=not real, page_num=page_num))
            html = BeautifulSoup(page, "html.parser")
            players = html.select("div.ysf-player-name")
            scores = html.select("td.Selected")
            assert len(players) == len(scores)
            orig_len = len(stats_to_return)

            for i, player in enumerate(players):
                name = player.select("a")[0].text
                points_raw = scores[i].text
                try:
                    points = float(points_raw)
                except ValueError:
                    points = 0.0

                if points == 0:
                    done = True
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
            page_num += 1
            if len(stats_to_return) == orig_len:
                break

        return stats_to_return
