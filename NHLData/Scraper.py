from bs4 import BeautifulSoup as Soup
from dateutil.parser import *
import re,locale
import Data

class FileScraper(object):
    def __init__(self, file):
        self._file = file
        contents = open(self._file).read()
        self.soup = Soup(contents)

    def cleanExcessWhitespace(self, string):
        return re.sub(r'\s{2,}', ' ', string)


class GameDetailsScraper(FileScraper):

    timezones = {
    "MST": -7*3600,
    "MDT": -6*3600,
    "PST": -8*3600,
    "PDT": -7*3600,
    "CST": -6*3600,
    "CDT": -5*3600,
    "EDT": -4*3600,
    "EST": -5*3600}

    frenchTeams = ['MONTREAL CANADIENS',
                   'CANADIENS MONTREAL',
                   'OTTAWA SENATORS']


    def parseDateTime(self,date,time):
        date = self.cleanExcessWhitespac(time.strptime(date, '%A, %B %d, %Y'))
        time = self.cleanExcessWhitespace(time.strptime(time, ))

    def setAttendanceAndArena(self, text):
        attendance = self.cleanExcessWhitespace(text.encode('ascii', 'ignore'))
        if self.locale == 'fr_CA':
            (attendance, self.details.arena) = [x.strip() for x in attendance.split('@', 1)]
            attendance = attendance.replace('Ass./Att.', '').strip()
        else:
            (attendance, self.details.arena) = [x.strip() for x in attendance.split('at', 1)]
            attendance = attendance.replace('Attendance', '').strip()
        self.details.attendance = int(locale.atof(attendance))

    def setStartEndTimes(self, dateText, timesText):
        times = self.cleanExcessWhitespace(timesText.encode('ascii', 'ignore'))
        date = dateText.strip()

        if self.locale == 'fr_CA':
            (start, end) = [x.strip().
                            replace('Dbut/Start', '').
                            replace('Fin/End', '') for x in times.split(";", 1)]
        else:
            (start, end) = [x.strip().
                            replace('Start', '').
                            replace('End', '') for x in times.split(";", 1)]
        start = "%s %s" % (start, date)
        end = "%s %s" % (end, date)
        self.details.startTime = parse(start, tzinfos=self.timezones)
        self.details.endTime = parse(end, tzinfos=self.timezones)

    def setHomeGameNumbers(self, text):
        homeSummary = self.cleanExcessWhitespace(text)

        if self.locale == 'fr_CA':
            matches = re.search(r'Game\s(\d+).*Home\s(\d+)',homeSummary)
        else:
            matches = re.search(r'Game\s(\d+).*Game\s(\d+)',homeSummary)

        self.details.homeTeamGameNo = int(matches.group(1))
        self.details.homeHomeGameNo = int(matches.group(2))

    def setVisitorGameNumbers(self, text):
        visitorSummary = self.cleanExcessWhitespace(text)

        if self.locale == 'fr_CA':
            matches = re.search(r'Game\s(\d+).*Away\s(\d+)',visitorSummary)
        else:
            matches = re.search(r'Game\s(\d+).*Game\s(\d+)',visitorSummary)

        self.details.awayTeamGameNo = int(matches.group(1))
        self.details.awayAwayGameNo = int(matches.group(2))

    def scrape(self):
        locale.setlocale(locale.LC_NUMERIC, 'en_US')
        self.details = Data.GameDetails()
        self.details.awayTeam = self.soup.find('table', id='Visitor').find('img')['alt']
        self.details.awayLogo = self.soup.find('table', id='Visitor').find('img')['src']
        self.details.homeTeam = self.soup.find('table', id='Home').find_all('img')[1]['alt']
        self.details.homeLogo = self.soup.find('table', id='Home').find_all('img')[1]['src']

        #Games @ Montreal or @ Ottawa are reported in French. Grar.
        if self.details.homeTeam in self.frenchTeams:
            self.locale = 'fr_CA'
        else:
            self.locale = 'en_US'

        self.setAttendanceAndArena(self.soup.find('table', id='GameInfo').find_all('td')[4].text)


        self.setStartEndTimes(self.soup.find('table', id='GameInfo').find_all('td')[3].text,
                              self.soup.find('table', id='GameInfo').find_all('td')[5].text)


        self.details.seasonGameNo = int(self.soup.find('table', id='GameInfo')
                                        .find_all('td')[6].text.split(' ',1)[1])

        self.details.homeScore = int(self.cleanExcessWhitespace(
            self.soup.find('table', id='Home').find_all('td')[1].text)
        )
        self.details.awayScore = int(self.cleanExcessWhitespace(
            self.soup.find('table', id='Visitor').find_all('td')[1].text)
        )

        self.setHomeGameNumbers(self.soup.find('table', id='Home').find_all('td')[5].text)
        self.setVisitorGameNumbers(self.soup.find('table', id='Visitor').find_all('td')[5].text)

        return self.details

class PlayByPlayScraper(GameDetailsScraper):


    def parsePlayersOnIce(self, tableRow):
        players = []
        i = 0
        while True:
            player = Data.PlayerOnIce()
            try:
                table = tableRow.find_all('table')[i]
                player.jersey = int(self.cleanExcessWhitespace(table.td.text).strip())
                (player.position, player.name) = table.td.font['title'].split(' - ')
                players.append(player)
                i+=1
            except:
                break

        return players

    def parseEvent(self, element):
        event = Data.GamePlayEvent()
        event.eventId = int (element.contents[1].text)
        event.period = int (element.contents[3].text)

        i = element.contents[7].stripped_strings
        (event.timeElapsed,event.timeRemaining) = (i.next(), i.next())

        event.eventType = element.contents[9].text
        event.description = element.contents[11].text

        try:
            visitorOnIce = element.contents[13].contents[1].contents[1]
            homeOnIce = element.contents[15].contents[1].contents[1]

            event.visitorOnIce = self.parsePlayersOnIce(visitorOnIce)
            event.homeOnIce = self.parsePlayersOnIce(homeOnIce)
        except:
            pass



        return event

    def scrape(self):
        gameDetails = super(PlayByPlayScraper, self).scrape()
        playByPlay = Data.GamePlayByPlay()

        awayTeam = self.soup.find('tr', class_='evenColor').find_previous_sibling().find_all('td')[6].text.split(' ')[0]
        homeTeam = self.soup.find('tr', class_='evenColor').find_previous_sibling().find_all('td')[7].text.split(' ')[0]

        events = []

        eventRows = self.soup.find_all('tr', class_='evenColor')
        for i,eventRow in enumerate(eventRows):
            event = self.parseEvent(eventRow)
            event.home = homeTeam
            event.visitor = awayTeam
            events.append(event)

        playByPlay.details = gameDetails
        playByPlay.events = events

        return playByPlay



def main():
    import pprint, sys, json
    playByPlay = PlayByPlayScraper('../data/%s/%s.HTM' % (sys.argv[1], sys.argv[2]))
    print json.dumps(playByPlay.scrape(), default=Data.JsonHandler)


if __name__ == "__main__":
    main()


