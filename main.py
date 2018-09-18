import asyncio

from espn import ESPNProjectionSource


async def main():
    sources = [
        # YahooProjectionSource(),
        ESPNProjectionSource(),
    ]
    stats = []
    for source in sources:
        stats.extend(await source.players_all_weeks())

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
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
