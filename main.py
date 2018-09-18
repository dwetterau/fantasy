import asyncio

from yahoo import YahooProjectionSource


async def main():
    y = YahooProjectionSource()
    stats = await y.players_all_weeks()
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
