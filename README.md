Simple fantasy football scraper
=====

## Setup
```
$ python3 -m virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

## Usage

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
2. Be sure the `is_mock=False` for the real draft, and tweak roster positions as necessary
3. Start running the drafted player exporting code from `draft_scrape.js` on the Yahoo! website's console.
4. Start up `draft.py` and periodically update the state of the draft by pasting in new status.