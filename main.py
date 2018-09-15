from fantasy import Position, Week
from yahoo import YahooProjectionSource


def main():
    y = YahooProjectionSource()
    players = y.get_players(Position.QUARTERBACK, Week(1))
    players2 = y.get_players(Position.QUARTERBACK, Week(2))

    players_by_name = {player.name: player for player in players}
    for player in players2:
        last_week = players_by_name.get(player.name)
        if not last_week:
            continue
        last_week.merge(player)

    print(players_by_name)


if __name__ == "__main__":
    main()
