from fantasy import Player, Position, Week


def main():
    # THINGS TO TUNE
    custom_rankings_source = True
    is_mock = False
    draft_pos = 4
    num_teams = 10
    roster_spots = [
        {Position.QUARTERBACK},
        {Position.QUARTERBACK},
        {Position.WIDE_RECEIVER},
        {Position.WIDE_RECEIVER},
        {Position.WIDE_RECEIVER},
        {Position.RUNNING_BACK},
        {Position.RUNNING_BACK},
        {Position.TIGHT_END},
        {Position.WIDE_RECEIVER, Position.RUNNING_BACK, Position.TIGHT_END},
        {Position.DEFENSE},
        {Position.KICKER},
        set(Position),
        set(Position),
        set(Position),
        set(Position),
        set(Position),
        set(Position),
    ]
    if is_mock:
        roster_spots = [{Position.QUARTERBACK}] + roster_spots[3:]
    # END THINGS TO TUNE

    f = open("./output/yahoo_ids.raw")
    id_to_player = {}
    name_to_id = {}
    for line in f.readlines():
        players = line.strip().split(",")
        for p in players:
            id_str, name_and_pos = p.split("|")
            name_and_pos = name_and_pos.split(" ")
            name = " ".join(name_and_pos[:-3])
            pos = name_and_pos[-1]
            p = Player(name, Position.from_short_str(pos))
            name_to_id[name.lower()] = id_str
            id_to_player[id_str] = p
    f.close()
    for i, defense in ID_TO_DEFENSES.items():
        name_to_id[defense.lower()] = i
        p = Player(defense, Position.DEFENSE)
        id_to_player[i] = p

    # Load up the rankings for each player.
    if custom_rankings_source:
        f = open("./output/fantasy_pros_custom_overall_rankings.csv")
        for i, line in enumerate(f.readlines()):
            cols = line.strip().split(",")
            tier = (i // num_teams) + 1
            rank = i + 1
            pos_str = cols[1]
            if pos_str == "DST":
                pos_str = "DEF"
            pos = Position.from_short_str(pos_str)
            name = rewrite_name_for_yahoo(cols[0], name_to_id)
            i = name_to_id[name.lower()]

            p = id_to_player[i]
            assert p.position == pos
            p.tier = tier
            p.rank = rank
    else:
        f = open("./output/fantasy_pros_overall_rankings.csv")
        first = True
        for line in f.readlines():
            if first:
                first = False
                continue

            cols = line.strip().split(",")
            tier = int(cols[1][1:-1])
            rank = int(cols[0][1:-1])

            raw_pos = cols[5][1:-1]
            pos_str = raw_pos[:2]
            if raw_pos.startswith("DST"):
                pos_str = "DEF"
            elif raw_pos.startswith("K"):
                pos_str = "K"
            pos = Position.from_short_str(pos_str)
            name = cols[3][1:-1]

            name = rewrite_name_for_yahoo(name, name_to_id)
            i = name_to_id[name.lower()]

            p = id_to_player[i]
            assert p.position == pos
            p.tier = tier
            p.rank = rank
    f.close()

    already_drafted_set = set()
    my_roster = [None for _ in range(len(roster_spots))]

    while True:
        cmd = input("Insert command: ").lower()
        is_num = True
        try:
            int(cmd)
        except ValueError:
            is_num = False

        if "," in cmd or is_num:
            already_drafted_set = set(cmd.split(","))
            # Fill in my roster
            my_roster = [None for _ in range(len(roster_spots))]
            for i, num in enumerate(cmd.split(",")):
                rnd = i // 10
                if rnd % 2 == 1:
                    if (i + draft_pos) % num_teams == 0:
                        add_to_roster(my_roster, roster_spots, id_to_player[num])
                else:
                    if ((i + 1) - draft_pos) % num_teams == 0:
                        add_to_roster(my_roster, roster_spots, id_to_player[num])
            # Force a "print next option" on update
            cmd = "next"

        if cmd in ("t", "top"):
            print_top_n_left(set(Position), already_drafted_set, id_to_player)
        if cmd in ("n", "next"):
            # Like top, but omits non-bench roster spots that are already filled.
            looking_for = set()
            for i, x in enumerate(my_roster):
                if not x and len(roster_spots[i]) <= 3:
                    looking_for.update(roster_spots[i])
            if not looking_for:
                # Default to finding anything if we are on the bench spots
                looking_for = set(Position)

            print_top_n_left(looking_for, already_drafted_set, id_to_player)
        if cmd in ("me", "mine", "ros", "roster"):
            for i, p in enumerate(my_roster):
                options = sorted(map(lambda pos: pos.to_short_str(), roster_spots[i]))
                prefix = ",".join(options)
                if len(options) == len(Position):
                    prefix = "BENCH"
                print(prefix, p.name if p else "")
        if cmd in ("q", "qb"):
            print_top_n_left({Position.QUARTERBACK}, already_drafted_set, id_to_player)
        if cmd in ("w", "wr"):
            print_top_n_left({Position.WIDE_RECEIVER}, already_drafted_set, id_to_player)
        if cmd in ("r", "rb"):
            print_top_n_left({Position.RUNNING_BACK}, already_drafted_set, id_to_player)
        if cmd == "te":
            print_top_n_left({Position.TIGHT_END}, already_drafted_set, id_to_player)
        if cmd == "k":
            print_top_n_left({Position.KICKER}, already_drafted_set, id_to_player)
        if cmd in ("d", "def", "dst"):
            print_top_n_left({Position.DEFENSE}, already_drafted_set, id_to_player)

        # Add a newline for readability
        print()


def print_top_n_left(positions, already_drafted, id_to_player, n=10):
    to_sort = []
    for i, player in id_to_player.items():
        if player.position not in positions or player.rank == 0:
            continue
        to_sort.append((i, player))
    s = sorted(to_sort, key=lambda p: p[1].rank)
    printed = 0
    for (i, p) in s:
        if i in already_drafted:
            continue
        print("{}-{}: {} - {}".format(p.tier, p.rank, p.name, p.position.to_short_str()))
        printed += 1
        if printed == n:
            break


def add_to_roster(my_roster, roster_spots, player):
    for i, spot in enumerate(roster_spots):
        if my_roster[i]:
            continue
        if player.position in spot:
            my_roster[i] = player
            return

    print("WARNING: Could not add player to roster {}", player.name)


def rewrite_name_for_yahoo(name: str, name_to_id) -> str:
    if name.lower() in name_to_id:
        return name
    if name == "Mitch Trubisky":
        return "Mitchell Trubisky"
    if name == "D.K. Metcalf":
        return "DK Metcalf"
    if name == "Steven Hauschka":
        return "Stephen Hauschka"
    if name == "M. Valdes-scantling":
        return "Marquez Valdes-Scantling"
    for n in name_to_id:
        if n.startswith(name.lower()):
            return n
        if name.lower().startswith(n):
            return n

    return name


ID_TO_DEFENSES = {
    "100003": "Chicago",
    "100024": "LA Chargers",
    "100030": "Jacksonville",
    "100016": "Minnesota",
    "100033": "Baltimore",
    "100014": "Los Angeles",
    "100005": "Cleveland",
    "100034": "Houston",
    "100018": "New Orleans",
    "100002": "Buffalo",
    "100007": "Denver",
    "100017": "New England",
    "100011": "Indianapolis",
    "100026": "Seattle",
    "100006": "Dallas",
    "100025": "San Francisco",
    "100021": "Philadelphia",
    "100023": "Pittsburgh",
    "100012": "Kansas City",
    "100010": "Tennessee",
    "100029": "Carolina",
    "100020": "New York",
    "100001": "Atlanta",
    "100009": "Green Bay",
    "100022": "Arizona",
    "100008": "Detroit",
    "100028": "Washington",
    "100015": "Miami",
    "100004": "Cincinnati",
    "100019": "New York",
    "100027": "Tampa Bay",
    "100013": "Oakland",
}

if __name__ == "__main__":
    main()
