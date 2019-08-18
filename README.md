Fantasy football tools
=====

## Setup
```
$ python3 -m virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

## Scraper usage

```
$ source env/bin/activate
$ python main.py > ~/full.csv
```

Note: Yahoo is pretty slow so it's commented out in `main.py`, You can also fetch each source one at
a time by commenting out parts of `main.py`. Maybe someday I'll make it have more flags and
parse args or whatever.


## Draft assistance
Steps:
1. Download the latest CSV of draft rankings from https://www.fantasypros.com/nfl/rankings/consensus-cheatsheets.php
2. Put that in `./output/fantasy_pros_overall_rankings.csv`
3. Be sure the `is_mock=False` for the real draft, and tweak roster and starting positions as necessary
4. Start running the drafted player exporting code from `draft_scrape.js` on the Yahoo! website's console.
5. Start up `draft.py` and periodically update the state of the draft by pasting in new status.

Debugging:
- If it errors when starting up, try truncating the overall rankings to avoid players that you're
  not going to be drafting anyway.