# nhl2json

Scraping the NHL.com's game stats and regurgitating them in a much more useful json.

## Dependencies

* Python >= 2.5?
* Flask
* dateutil

## Usage

The easiest way to use this code is to run it as a Flask app

    $ python run.py

## Available Routes

### Play By Play

Parses the NHL's play by play pages in the format of [http://www.nhl.com/scores/htmlreports/20122013/PL020001.HTM][]
via the url: http://localhost:5000/pbp/[season]/[id]

* [season]: one of ['20102011', '20112012', '20102013']. Earlier seasons might be supported, they might not.
* [id]: nhl game number. For non-shorted complete seasons, valid values are in the range [1-1230].

[http://www.nhl.com/scores/htmlreports/20122013/PL020001.HTM]: http://www.nhl.com/scores/htmlreports/20122013/PL020001.HTM


## Todo

* parse the other stats pages
* gzip the stored html
* cache the response
