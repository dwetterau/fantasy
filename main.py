
def main():
    y = YahooProjectionSource()
    y.get_players(Position.QUARTERBACK, Week(1))


if __name__ == "__main__":
    main()