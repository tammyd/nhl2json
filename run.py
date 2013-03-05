from flask import Flask
from flask import json, abort
from flask import Response
from urllib2 import HTTPError
from NHLData.Scraper import PlayByPlayScraper
from NHLData.Data import JsonHandler
from NHLData.Files import PlayByPlayFile

app = Flask(__name__)

@app.route("/pbp/<int:season>/<int:gameid>")
def pbp(season,gameid):
    try:
        dataFile = PlayByPlayFile('data', season, gameid).ensureData()
        playByPlay = PlayByPlayScraper(dataFile)
        js = json.dumps(playByPlay.scrape(), default=JsonHandler)
    except HTTPError as e:
        abort(e.code)

    #TODO
    #The response never changes
    #Cache this, or at least set some cache-control headers!!
    resp = Response(js, status=200, mimetype='application/json')

    return resp

if __name__ == "__main__":
    app.run(debug=True)