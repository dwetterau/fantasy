from fantasy import Player, Position, Week


def main():
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

    # Load up the rankings for each player.
    f = open("./output/fantasy_pros.csv")
    first = True
    for line in f.readlines():
        if first:
            first = False
            continue

        cols = line.strip().split(",")
        pts = float(cols[-3])
        pos = Position.from_str(cols[-5])
        name = " ".join(cols[:-5])

        if pts < 60:
            continue
        name = rewrite_name_for_yahoo(name, name_to_id)
        try:
            i = name_to_id[name.lower()]
        except KeyError:
            # TODO: Also handle defense..
            if pos == Position.DEFENSE:
                continue

        p = id_to_player[i]
        assert p.position == pos
        p.projected_points = {Week(0, is_draft=True): pts}

    is_mock = True
    draft_pos = 2
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

    already_drafted_set = set()
    my_roster = ["" for _ in range(len(roster_spots))]

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
            my_roster = ["" for _ in range(len(roster_spots))]
            for i, num in enumerate(cmd.split(",")):
                if int(num) > 100000:
                    # TODO: I think these are defenses?!
                    continue
                rnd = i // 10
                if rnd % 2 == 1:
                    if (i + draft_pos) % num_teams == 0:
                        add_to_roster(my_roster, roster_spots, id_to_player[num])
                else:
                    if ((i + 1) - draft_pos) % num_teams == 0:
                        add_to_roster(my_roster, roster_spots, id_to_player[num])

        if cmd == "top":
            print_top_n_left(set(Position), already_drafted_set, id_to_player)
        if cmd == "next":
            # TODO: Print out a recommendation
            pass
        if cmd in ("me", "mine", "ros", "roster"):
            print(my_roster)
        if cmd in ("q", "qb"):
            print_top_n_left({Position.QUARTERBACK}, already_drafted_set, id_to_player)
        if cmd in ("w", "wr"):
            print_top_n_left({Position.WIDE_RECEIVER}, already_drafted_set, id_to_player)
        if cmd in ("r", "rb"):
            print_top_n_left({Position.RUNNING_BACK}, already_drafted_set, id_to_player)
        if cmd in ("t", "te"):
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
        if player.position not in positions:
            continue
        to_sort.append((i, player))
    s = sorted(to_sort, key=lambda p: sum(p[1].projected_points.values()), reverse=True)
    printed = 0
    for idx, (i, p) in enumerate(s):
        if i in already_drafted:
            continue
        print("{}: {}".format(idx + 1, p.name))
        printed += 1
        if printed == n:
            break


def add_to_roster(my_roster, roster_spots, player):
    for i, spot in enumerate(roster_spots):
        if len(my_roster[i]):
            continue
        if player.position in spot:
            my_roster[i] = player.name
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
    for n in name_to_id:
        if n.startswith(name.lower()):
            return n
        if name.lower().startswith(n):
            return n

    return name


if __name__ == "__main__":
    main()
