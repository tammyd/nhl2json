
def JsonHandler(Obj):
    if hasattr(Obj, 'jsonable'):
        return Obj.jsonable()
    else:
        raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(Obj), repr(Obj))


class TeamInfo(object):
    def __init__(self):
        self.name = None
        self.logo = None

    def jsonable(self):
        return {'name': self.name, 'logo':self.logo}

class TeamGame(object):
    def __init__(self):
        self.name = None
        self.logo = None
        self.gameNo = None
        self._isHome = None
        self.homeGameNo = None
        self.awayGameNo = None

    def jsonable(self):
        data = {
            'name': self.name,
            'logo':self.logo,
            'gameNo': self.gameNo
        }
        if self.homeGameNo is not None:
            data['homeGameNo'] = self.homeGameNo
        if self.awayGameNo is not None:
            data['awayGameNo'] = self.awayGameNo

        return data
    @property
    def isHome(self):
        return self._isHome

    @property
    def isAway(self):
        return not self.isHome

    @isHome.setter
    def isHome(self, value):
        self._isHome = True if value else False

    @isAway.setter
    def isAway(self, value):
        self._isHome = False if value else True

class GameDetails(object):

    def __init__(self):
        self._homeTeam = TeamGame()
        self._awayTeam = TeamGame()
        self._homeTeam.isHome = True
        self._awayTeam.isHome = False

        #Straight up properties
        self.attendance = None
        self.seasonGameNo = None
        self.arena = None
        self.startTime = None
        self.endTime = None
        self.homeScore = None
        self.awayScore = None

    def jsonable(self):
        return {
            'homeTeam': self._homeTeam.jsonable(),
            'awayTeam': self._awayTeam.jsonable(),
            'attendance': self.attendance,
            'seasonGameNo': self.seasonGameNo,
            'arena': self.arena,
            'startTime': self.startTime.isoformat(),
            'endTime': self.endTime.isoformat(),
            'homeScore': self.homeScore,
            'awayScore': self.awayScore
        }
        
    @property
    def homeTeamGameNo(self):
        return self._homeTeam.gameNo
    
    @homeTeamGameNo.setter
    def homeTeamGameNo(self, value):
        self._homeTeam.gameNo = value
        
    @property
    def awayTeamGameNo(self):
        return self._awayTeam.gameNo
    
    @awayTeamGameNo.setter
    def awayTeamGameNo(self, value):
        self._awayTeam.gameNo = value
        
    @property 
    def homeHomeGameNo(self):
        return self._homeTeam.homeGameNo
    
    @homeHomeGameNo.setter
    def homeHomeGameNo(self, value):
        self._homeTeam.homeGameNo = value

    @property
    def awayAwayGameNo(self):
        return self._awayTeam.awayGameNo

    @awayAwayGameNo.setter
    def awayAwayGameNo(self, value):
        self._awayTeam.awayGameNo = value


    @property
    def homeTeam(self):
        return self._homeTeam.name

    @homeTeam.setter
    def homeTeam(self, value):
        self._homeTeam.name = value

    @property
    def awayTeam(self):
        return self._awayTeam.name

    @awayTeam.setter
    def awayTeam(self, value):
        self._awayTeam.name = value

    @property
    def homeLogo(self):
        return self._homeTeam.logo

    @homeLogo.setter
    def homeLogo(self, value):
        self._homeTeam.logo = value

    @property
    def awayLogo(self):
        return self._awayTeam.logo

    @awayLogo.setter
    def awayLogo(self, value):
        self._awayTeam.logo = value

class PlayerOnIce(object):
    def __init__(self):
        self.name = None
        self.position = None
        self.jersey = None

    def jsonable(self):
        return {
            'name': self.name,
            'position': self.position,
            'jersey': self.jersey
        }

class GamePlayEvent(object):
    def __init__(self):
        self.home = None
        self.visitor = None
        self.period = None
        self.eventId = None
        self.timeElapsed = None
        self.timeRemaining = None
        self.eventType = None
        self.description = None
        self.homeOnIce = []
        self.visitorOnIce = []

    def jsonable(self):
        data = {
            'home': self.home,
            'visitor': self.visitor,
            'period': self.period,
            'eventId': self.eventId,
            'timeElapsed': self.timeElapsed,
            'timeRemaining': self.timeRemaining,
            'eventType': self.eventType,
            'description': self.description,
            'homeOnIce': [x.jsonable() for x in self.homeOnIce],
            'visitorOnIce': [x.jsonable() for x in self.visitorOnIce]
        }

        return data


class GamePlayByPlay(object):
    def __init__(self):
        self.details = None
        self.events = []

    def jsonable(self):
        return {
            'gameDetails': self.details.jsonable(),
            'events': [x.jsonable() for x in self.events]
        }



        



