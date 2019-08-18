from fantasy import Week, Position
from fantasy_pros import FantasyProsProjectionSource


# Downloads the latest rankings of all players.
def main():
    source = FantasyProsProjectionSource()
    week = Week(0, is_draft=True)
    stats = []
    for position in Position:
        stats.extend(source.get_players(
            position,
            week,
            False,
        ))

    print(",".join((
        "name",
        "position",
        "week",
        "points",
        "type",
        "source"
    )))

    for stat in stats:
        print(stat.to_csv())


if __name__ == "__main__":
    main()
