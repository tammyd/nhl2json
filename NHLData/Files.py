import os, errno
import urllib2

class PlayByPlayFile(object):

    HOST = "http://www.nhl.com/scores/htmlreports/"
    PREFIX = 'PL02'

    def __init__(self, dir, season, gameId):
        self.directory = dir
        self.season = season
        self.gameId = gameId

    def getFileName(self):
        return "%s/%s/%s%04d.HTM" % (self.directory, self.season, self.PREFIX, self.gameId)

    def getUrl(self):
        return "%s/%s/%s%04d.HTM" % (self.HOST, self.season, self.PREFIX, self.gameId)

    def ensureData(self):
        filename = self.getFileName()
        try:
            with open(filename) as f: return filename
        except IOError as e:
            return self.downloadData()

    def downloadData(self):
        filename = self.getFileName()
        url = self.getUrl()

        path = os.path.dirname(filename)
        if not os.path.exists(path):
            # try and create the directory - python equiv of mkdir -p
            try:
                os.makedirs(path)
            except OSError as exc:
                if exc.errno == errno.EEXIST and os.path.isdir(path):
                    pass
                else: raise

        # download and save url contents
        f = urllib2.urlopen(url)
        with open(filename, "wb") as html:
            html.write(f.read())

        #TODO: These files are huge - we should gzip them or something

        return filename





