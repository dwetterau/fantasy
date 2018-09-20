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
