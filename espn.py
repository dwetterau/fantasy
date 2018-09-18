from typing import List

from bs4 import BeautifulSoup

from fantasy import ProjectionSource, Week, Position, PlayerStats, Source
from fetch import fetch


class ESPNProjectionSource(ProjectionSource):

    def source(self):
        return Source.ESPN

    def _fetch_url(self, week: Week, page_num=0) -> str:
        return (
            "http://games.espn.com/ffl/tools/projections?"
            "scoringPeriodId={}&seasonId=2018&startIndex={}".format(
                week.num,
                page_num * 40,
            )
        )

    def get_players(self, fake_position: Position, week: Week, real: bool) -> List[PlayerStats]:
        if fake_position != Position.QUARTERBACK or real:
            return []

        done = False
        page_num = 0
        stats_to_return = []
        while not done:
            page = fetch(self._fetch_url(week, page_num=page_num))
            html = BeautifulSoup(page, "html.parser")
            players = html.select("tr.pncPlayerRow")

            orig_len = len(stats_to_return)
            for player in players:
                name = player.select("td.playertablePlayerName a")[0].text
                position_raw = player.select("td.playertablePlayerName")[0].text

                points_raw = player.select("td.playertableStat.sortedCell")[0].text
                try:
                    points = float(points_raw)
                except ValueError:
                    points = 0.0

                position = None
                for part in position_raw.strip().split()[::-1]:
                    try:
                        position = Position.from_short_str(part)
                        break
                    except ValueError:
                        continue
                if not position:
                    continue

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
