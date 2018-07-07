from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

engine = create_engine('sqlite:///data.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()


class Summoner(Base):
    """Just the normal Leauge of Legend Summoner with his profile """

    __tablename__ = 'summoners'

    summoner_id = Column(Integer, ForeignKey("Leauge_RANKED_SOLO_5x5.player_or_team_id"),ForeignKey("Leauge_RANKED_FLEX_SR.player_or_team_id"),ForeignKey("Leauge_RANKED_FLEX_TT.player_or_team_id"),ForeignKey("ChampionMastery.player_id"),unique=True,nullable=False)
    account_id = Column(Integer,ForeignKey("Matches.player_id"), unique=True, primary_key=True)
    name = Column(String(80), unique=True)
    profile_icon_id = Column(Integer)
    revision_date = Column(Integer)
    summoner_level = Column(Integer)
    solo_5v5_leauge = relationship('LeaugeRankedSolo5x5', viewonly=True)
    flex_5v5_leauge = relationship('LeaugeRankedFlexSR',viewonly=True)
    tt_3v3_leauge = relationship('LeaugeRankedFlexTT',viewonly=True)
    champion_masteries = relationship('ChampionMastery',viewonly=True)
    matches = relationship('Matches',viewonly=True)

    def __init__(self, id, accountId, name, profileIconId, revisionDate, summonerLevel):
        self.summoner_id = id
        self.account_id = accountId
        self.name = name
        self.profile_icon_id = profileIconId
        self.revision_date = revisionDate
        self.summoner_level = summonerLevel

    def __repr__(self):
        return "<Summoner(name='%s', accountId='%s', summonerId='%s', summonerLevel='%s', revisionDate='%s', profileIconId='%s', [SOLO_5v5_leauge'%s', FLEX_5v5_leauge'%s', TT_3v3_leauge'%s']>" % (
            self.name, self.account_id, self.summoner_id, self.summoner_level, self.revision_date, self.profile_icon_id, self.solo_5v5_leauge, self.flex_5v5_leauge, self.tt_3v3_leauge)

    def get_all_matches(self):
        return self.matches.find_all_by_id(self.account_id)

    @classmethod
    def find_by_name(cls, name):
        return session.query(cls).filter_by(name=name).first()
    
    @classmethod
    def find_by_summoner_id(cls, summoner_id):
        return session.query(cls).filter_by(summoner_id=summoner_id).first()

    @classmethod
    def find_by_account_id(cls, account_id):
        return session.query(cls).filter_by(account_id=account_id).first()

    @classmethod
    def get_all_summoners(cls):
        """return a list of summoner objects from all your summoner in the Database"""
        return session.query(cls).all()

    def to_dict(self):
        return {
            "name": self.name,
            "accountId": self.account_id,
            "summonerId": self.summoner_id,
            "summonerLevel": self.summoner_level,
            "revisionDate":  self.revision_date,
            "profileIconId": self.profile_icon_id
            }

    def insert_to_db(self):
        session.add(self)
        session.commit()

    def add(self):
        session.add(self)

    @classmethod
    def commit(cls):
        session.commit()


class LeaugeRankedSolo5x5(Base):
    
    __tablename__ = 'Leauge_RANKED_SOLO_5x5'

    leauge_id = Column(String(100))
    leauge_name = Column(String(80))
    tier = Column(String(15))
    queue_type = Column(String(20))
    rank = Column(String(3))
    player_or_team_id = Column(Integer, primary_key=True)
    player_or_team_name = Column(String(80))
    leauge_points = Column(Integer)
    wins = Column(Integer)
    losses = Column(Integer)
    veteran = Column(String)
    inactive = Column(String)
    fresh_blood = Column(String)
    hot_streak = Column(String)

    def __init__(self, leagueId, leagueName, tier, queueType, rank, playerOrTeamId, playerOrTeamName, leaguePoints, wins, losses, veteran, inactive, freshBlood, hotStreak):
        self.leauge_id = leagueId
        self.leauge_name = leagueName
        self.tier = tier
        self.queue_type = queueType
        self.rank = rank
        self.player_or_team_id = playerOrTeamId
        self.player_or_team_name = playerOrTeamName
        self.leauge_points = leaguePoints
        self.wins = wins
        self.losses = losses
        self.veteran = str(veteran)
        self.inactive = str(inactive)
        self.fresh_blood = str(freshBlood)
        self.hot_streak = str(hotStreak)
        #self.mini_series = miniSeries -> promo für nächste division
        
    def __repr__(self):
        return "<LeaugeRANKED_SOLO_5x5(name='%s', leaugeId='%s', queueType='%s' playerOrTeamName='%s', tier='%s', rank='%s', leaugePoints='%s'>" % (
            self.leauge_name, self.leauge_id, self.queue_type, self.player_or_team_name, self.tier, self.rank, self.leauge_points)

    def insert_to_db(self):
        session.add(self)
        session.commit()

    def to_dict(self):
        """return the object as a dict"""
        return {'leagueId': self.leauge_id,
                'leagueName': self.leauge_name,
                'tier': self.tier,
                'queueType': self.queue_type,
                'rank': self.rank,
                'playerOrTeamId': self.player_or_team_id,
                'playerOrTeamName': self.player_or_team_name,
                'leaguePoints': self.leauge_points,
                'wins': self.wins,
                'losses': self.losses,
                'veteran': self.veteran,
                'inactive': self.inactive,
                'freshBlood': self.fresh_blood,
                'hotStreak': self.hot_streak}

    @classmethod
    def find_by_leauge_id(cls, leauge_id):
        return session.query(cls).filter_by(leauge_id=leauge_id).first()

    @classmethod
    def find_by_summoner_id(cls, summoner_id):
        """player_or_team_id = summoner_id"""
        return session.query(cls).filter_by(player_or_team_id=summoner_id).first()

    @classmethod
    def get_all(cls):
        """return a list of Leauge_RANKED_SOLO_5x5 objects from all your Leauge_RANKED_SOLO_5x5 in the Database"""
        return session.query(cls).all()

    def add(self):
        session.add(self)

    @classmethod
    def commit(cls):
        session.commit()


class LeaugeRankedFlexSR(Base):
    
    __tablename__ = 'Leauge_RANKED_FLEX_SR'

    leauge_id = Column(String(100))
    leauge_name = Column(String(80))
    tier = Column(String(15))
    queue_type = Column(String(20))
    rank = Column(String(3))
    player_or_team_id = Column(Integer, primary_key=True)
    player_or_team_name = Column(String(80))
    leauge_points = Column(Integer)
    wins = Column(Integer)
    losses = Column(Integer)
    veteran = Column(String)
    inactive = Column(String)
    fresh_blood = Column(String)
    hot_streak = Column(String)

    def __init__(self, leagueId, leagueName, tier, queueType, rank, playerOrTeamId, playerOrTeamName, leaguePoints, wins, losses, veteran, inactive, freshBlood, hotStreak):
        self.leauge_id = leagueId
        self.leauge_name = leagueName
        self.tier = tier
        self.queue_type = queueType
        self.rank = rank
        self.player_or_team_id = playerOrTeamId
        self.player_or_team_name = playerOrTeamName
        self.leauge_points = leaguePoints
        self.wins = wins
        self.losses = losses
        self.veteran = str(veteran)
        self.inactive = str(inactive)
        self.fresh_blood = str(freshBlood)
        self.hot_streak = str(hotStreak)
        #self.mini_series = miniSeries
        
    def __repr__(self):
        return "<LeaugeRANKED_FLEX_SR(name='%s', leaugeId='%s', queueType='%s' playerOrTeamName='%s', tier='%s', rank='%s', leaugePoints='%s'>" % (
            self.leauge_name, self.leauge_id, self.queue_type, self.player_or_team_name, self.tier, self.rank, self.leauge_points)

    def insert_to_db(self):
        session.add(self)
        session.commit()

    def add(self):
        session.add(self)

    @classmethod
    def commit(cls):
        session.commit()

    def to_dict(self):
        """return the object as a dict"""
        return {'leagueId': self.leauge_id,
                'leagueName': self.leauge_name,
                'tier': self.tier,
                'queueType': self.queue_type,
                'rank': self.rank,
                'playerOrTeamId': self.player_or_team_id,
                'playerOrTeamName': self.player_or_team_name,
                'leaguePoints': self.leauge_points,
                'wins': self.wins,
                'losses': self.losses,
                'veteran': self.veteran,
                'inactive': self.inactive,
                'freshBlood': self.fresh_blood,
                'hotStreak': self.hot_streak}

    @classmethod
    def find_by_leauge_id(cls, leauge_id):
        return session.query(cls).filter_by(leauge_id=leauge_id).first()

    @classmethod
    def find_by_summoner_id(cls, summoner_id):
        """player_or_team_id = summoner_id"""
        return session.query(cls).filter_by(player_or_team_id=summoner_id).first()

    @classmethod
    def get_all(cls):
        """return a list of Leauge_RANKED_FLEX_SR objects from all your Leauge_RANKED_FLEX_SR in the Database"""
        return session.query(cls).all()


class LeaugeRankedFlexTT(Base):
    
    __tablename__ = 'Leauge_RANKED_FLEX_TT'

    leauge_id = Column(String(100))
    leauge_name = Column(String(80))
    tier = Column(String(15))
    queue_type = Column(String(20))
    rank = Column(String(3))
    player_or_team_id = Column(Integer, primary_key=True)
    player_or_team_name = Column(String(80))
    leauge_points = Column(Integer)
    wins = Column(Integer)
    losses = Column(Integer)
    veteran = Column(String)
    inactive = Column(String)
    fresh_blood = Column(String)
    hot_streak = Column(String)

    def __init__(self, leagueId, leagueName, tier, queueType, rank, playerOrTeamId, playerOrTeamName, leaguePoints, wins, losses, veteran, inactive, freshBlood, hotStreak):
        self.leauge_id = leagueId
        self.leauge_name = leagueName
        self.tier = tier
        self.queue_type = queueType
        self.rank = rank
        self.player_or_team_id = playerOrTeamId
        self.player_or_team_name = playerOrTeamName
        self.leauge_points = leaguePoints
        self.wins = wins
        self.losses = losses
        self.veteran = str(veteran)
        self.inactive = str(inactive)
        self.fresh_blood = str(freshBlood)
        self.hot_streak = str(hotStreak)
        #self.mini_series = miniSeries
        
    def __repr__(self):
        return "<LeaugeRANKED_FLEX_TT(name='%s', leaugeId='%s', queueType='%s' playerOrTeamName='%s', tier='%s', rank='%s', leaugePoints='%s'>" % (
            self.leauge_name, self.leauge_id, self.queue_type, self.player_or_team_name, self.tier, self.rank, self.leauge_points)

    def insert_to_db(self):
        session.add(self)
        session.commit()

    def add(self):
        session.add(self)

    @classmethod
    def commit(cls):
        session.commit()

    def to_dict(self):
        """return the object as a dict"""
        return {'leagueId': self.leauge_id,
                'leagueName': self.leauge_name,
                'tier': self.tier,
                'queueType': self.queue_type,
                'rank': self.rank,
                'playerOrTeamId': self.player_or_team_id,
                'playerOrTeamName': self.player_or_team_name,
                'leaguePoints': self.leauge_points,
                'wins': self.wins,
                'losses': self.losses,
                'veteran': self.veteran,
                'inactive': self.inactive,
                'freshBlood': self.fresh_blood,
                'hotStreak': self.hot_streak}

    @classmethod
    def find_by_leauge_id(cls, leauge_id):
        return session.query(cls).filter_by(leauge_id=leauge_id).first()

    @classmethod
    def find_by_summoner_id(cls, summoner_id):
        """player_or_team_id = summoner_id"""
        return session.query(cls).filter_by(player_or_team_id=summoner_id).first()

    @classmethod
    def get_all(cls):
        """return a list of Leauge_RANKED_FLEX_TT objects from all your Leauge_RANKED_FLEX_TT in the Database"""
        return session.query(cls).all()


class ChampionMastery(Base):

    __tablename__ = 'ChampionMastery'
    id = Column(Integer, primary_key=True)
    chest_granted = Column(String)
    champion_level = Column(Integer)
    champion_points = Column(Integer)
    champion_id = Column(Integer)
    player_id = Column(Integer)
    champion_points_until_next_level = Column(Integer)
    tokens_earned = Column(Integer)
    champion_points_since_last_level = Column(Integer)
    last_play_time = Column(Integer)

    def __init__(self, chestGranted, championLevel, championPoints, championId, playerId, championPointsUntilNextLevel, tokensEarned, championPointsSinceLastLevel, lastPlayTime):
        self.chest_granted = chestGranted
        self.champion_level = championLevel
        self.champion_points = championPoints
        self.champion_id = championId
        self.player_id = playerId
        self.champion_points_until_next_level = championPointsUntilNextLevel
        self.tokens_earned = tokensEarned
        self.champion_points_since_last_level = championPointsSinceLastLevel
        self.last_play_time = lastPlayTime
        self.id = int(str(playerId)+str(championId))

    def __repr__(self):
        return "<ChampionsMastery(playerId='%s', championId='%s', championPoints='%s', championLevel='%s', chestGranted='%s', championPointsUntilNextLevel='%s', tokensEarned'%s', championPointsSinceLastLevel'%s', lastPlayTime'%s'>" % (
            self.player_id, self.champion_id, self.champion_points, self.champion_level, self.chest_granted, self.champion_pionts_until_next_level, self.tokens_earned, self.champion_points_since_last_level, self.last_play_time)

    def to_dict(self):
        """returns the object as dict :returns dict"""
        return {'id': self.id,
                'lastPlayTime': self.last_play_time,
                'championPointsSinceLastLevel': self.champion_points_since_last_level,
                'championPointsUntilNextLevel': self.champion_points_until_next_level,
                'tokensEarned': self.tokens_earned,
                'playerId': self.player_id,
                'championId': self.champion_id,
                'championPoints': self.champion_points,
                'championLevel': self.champion_level,
                'chestGranted': self.chest_granted}

    @classmethod
    def find_by_player_id(cls, summoner_id):
        return session.query(cls).filter_by(player_id=summoner_id).all()
    
    @classmethod
    def find_by_champion_id(cls, champion_id):
        return session.query(cls).filter_by(champion_id=champion_id).all()
    
    @classmethod
    def find_by_summoner_and_champion_id(cls, summoner_id, champion_id):
        return session.query(cls).filter_by(player_id=summoner_id).filter_by(champion_id=champion_id).first()
    
    @classmethod
    def get_all(cls):
        """return a list of ChampionMastery objects from all your ChampionMastery in the Database"""
        return session.query(cls).all()

    def add(self):
        session.add(self)

    @classmethod
    def commit(cls):
        session.commit()

    def insert_to_db(self):
        session.add(self)
        session.commit()


class Matches(Base):
    """playerId or player_id = Summoner.account_id """
    __tablename__ = 'Matches'
    id = Column(Integer, primary_key=True)
    platform_id = Column(String)
    game_id = Column(Integer)
    champion = Column(Integer)
    queue = Column(Integer)
    season = Column(Integer)
    timestamp = Column(Integer)
    role = Column(String)
    lane = Column(String)
    player_id = Column(Integer)

    def __init__(self, platformId, gameId, champion, queue, season, timestamp, role, lane, playerId):
        self.platform_id = platformId
        self.game_id = gameId
        self.champion = champion
        self.queue = queue
        self.season = season
        self.timestamp = timestamp
        self.role = role
        self.lane = lane
        self.player_id = playerId
        self.id = int(str(playerId) + str(gameId))

    def __repr__(self):
        return "<Match(platformId='%s', gameId='%s', Champion='%s', queue='%s', season='%s', timestamp='%s', role'%s', lane'%s', playerId'%s'>" % (
            self.platform_id, self.game_id, self.champion, self.queue, self.season, self.timestamp, self.role, self.lane, self.player_id)
    
    def to_dict(self):
        """returns the object as a dict"""
        dicts = {
            "platformId": self.platform_id,
            "gameId": self.game_id,
            "champion": self.champion,
            "queue": self.queue,
            "season": self.season,
            "timeStamp": self.timestamp,
            "role": self.role,
            "lane": self.lane,
            "playerId": self.player_id
            }
        return dicts

    @classmethod
    def find_by_id(cls, player_id_gameId):
        return session.query(cls).filter_by(id=player_id_gameId).first()

    @classmethod
    def find_all_by_id(cls, player_id):
        return session.query(cls).filter_by(player_id=player_id).all()
    
    @classmethod
    def get_all_matches(cls):
        """return a list of matches objects from all your matches in the Database """
        return session.query(cls).all()

    def insert_to_db(self):
        session.add(self)
        session.commit()

    def add(self):
        session.add(self)

    @classmethod
    def commit(cls):
        session.commit()


class Champions(Base):
    __tablename__ = 'Champions'

    id = Column(Integer, primary_key=True)
    key = Column(String)
    name = Column(String)
    title = Column(String)

    def __init__(self, id, key, name, title):
        self.id = id 
        self.key = key
        self.name = name
        self.title = title


    def to_dict(self):
        """returns the object as a dict"""
        dicts = {
            "id": self.id,
            "key": self.key,
            "name": self.name,
            "title": self.title
            }
        return dicts

    @classmethod
    def get_all_champions(cls):
        """return a list of champions objects from all your champions in the Database """
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, id):
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return session.query(cls).filter_by(name=name).first()

    def insert_to_db(self):
        session.add(self)
        session.commit()

    def add(self):
        session.add(self)

    @classmethod
    def commit(cls):
        session.commit()


class CsDiffPerMinDeltas(Base):

    __tablename__ = "CsDiffPerMinDeltas"

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer)
    participant_id = Column(Integer)
    null_zehn = Column(Float)
    zehn_zwanzig = Column(Float)
    zwanzig_dreisig = Column(Float)
    dreisig_vierzig = Column(Float)
    vierzig_fünfzig = Column(Float)
    fünfzig_sechzig = Column(Float)
    sechzig_siebzig = Column(Float)
    siebzig_achzieg = Column(Float)
    achzig_neunzig = Column(Float)
    neunzig_hunndert = Column(Float)

    def __init__(self, gameId, participantId, eins, zwei, drei, vier, fünf, sechs, sieben, acht, neun, zehn):
        self.id = int(str(gameId)+str(participantId))
        self.game_id = gameId
        self.participant_id = participantId
        self.null_zehn = eins
        self.zehn_zwanzig = zwei
        self.zwanzig_dreisig = drei
        self.dreisig_vierzig = vier
        self.vierzig_fünfzig = fünf
        self.fünfzig_sechzig = sechs
        self.sechzig_siebzig = sieben
        self.siebzig_achzieg = acht
        self.achzig_neunzig = neun
        self.neunzig_hunndert = zehn

    def to_dict(self):
        """"returns the object as a dict"""
        dicts = {
            "id": self.id,
            "gameId": self.game_id,
            "participantId": self.participant_id,
            "0-10": self.null_zehn,
            "10-20": self.zehn_zwanzig,
            "20-30": self.zwanzig_dreisig,
            "30-40": self.dreisig_vierzig,
            "40-50": self.vierzig_fünfzig,
            "50-60": self.fünfzig_sechzig,
            "60-70": self.sechzig_siebzig,
            "70-80": self.siebzig_achzieg,
            "80-90": self.achzig_neunzig,
            "90-100": self.neunzig_hunndert
            }
        return dicts

    @classmethod
    def find_by_id(cls,id):
        """ id = gameId and participantId """
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def get_all_CsDiffPerMinDeltas(cls):
        """return a list of CsDiffPerMinDeltas objects from all your CsDiffPerMinDeltas in the Database """
        return session.query(cls).all()

    def insert_to_db(self):
        session.add(self)
        session.commit()

    def add(self):
        session.add(self)

    @classmethod
    def commit(cls):
        session.commit()


class GoldPerMinDeltas(Base):

    __tablename__ = "GoldPerMinDeltas"

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer)
    participant_id = Column(Integer)
    null_zehn = Column(Float)
    zehn_zwanzig = Column(Float)
    zwanzig_dreisig = Column(Float)
    dreisig_vierzig = Column(Float)
    vierzig_fünfzig = Column(Float)
    fünfzig_sechzig = Column(Float)
    sechzig_siebzig = Column(Float)
    siebzig_achzieg = Column(Float)
    achzig_neunzig = Column(Float)
    neunzig_hunndert = Column(Float)

    def __init__(self, gameId, participantId, eins, zwei, drei, vier, fünf, sechs, sieben, acht, neun, zehn):
        self.id = int(str(gameId)+str(participantId))
        self.game_id = gameId
        self.participant_id = participantId
        self.null_zehn = eins
        self.zehn_zwanzig = zwei
        self.zwanzig_dreisig = drei
        self.dreisig_vierzig = vier
        self.vierzig_fünfzig = fünf
        self.fünfzig_sechzig = sechs
        self.sechzig_siebzig = sieben
        self.siebzig_achzieg = acht
        self.achzig_neunzig = neun
        self.neunzig_hunndert = zehn

    def to_dict(self):
        """returns the object as a dict"""
        dicts = {
            "id": self.id,
            "gameId": self.game_id,
            "participantId": self.participant_id,
            "0-10": self.null_zehn,
            "10-20": self.zehn_zwanzig,
            "20-30": self.zwanzig_dreisig,
            "30-40": self.dreisig_vierzig,
            "40-50": self.vierzig_fünfzig,
            "50-60": self.fünfzig_sechzig,
            "60-70": self.sechzig_siebzig,
            "70-80": self.siebzig_achzieg,
            "80-90": self.achzig_neunzig,
            "90-100": self.neunzig_hunndert
            }
        return dicts

    @classmethod
    def find_by_id(cls, id):
        """ id = gameId and participantId """
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def get_all_GoldPerMinDeltas(cls):
        """return a list of GoldPerMinDeltas objects from all your GoldPerMinDeltas in the Database """
        return session.query(cls).all()

    def insert_to_db(self):
        session.add(self)
        session.commit()

    def add(self):
        session.add(self)

    @classmethod
    def commit(cls):
        session.commit()


class XpDiffPerMinDeltas(Base):

    __tablename__ = "XpDiffPerMinDeltas"

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer)
    participant_id = Column(Integer)
    null_zehn = Column(Float)
    zehn_zwanzig = Column(Float)
    zwanzig_dreisig = Column(Float)
    dreisig_vierzig = Column(Float)
    vierzig_fünfzig = Column(Float)
    fünfzig_sechzig = Column(Float)
    sechzig_siebzig = Column(Float)
    siebzig_achzieg = Column(Float)
    achzig_neunzig = Column(Float)
    neunzig_hunndert = Column(Float)

    def __init__(self, gameId, participantId, eins, zwei, drei, vier, fünf, sechs, sieben, acht, neun, zehn):
        self.id = int(str(gameId)+str(participantId))
        self.game_id = gameId
        self.participant_id = participantId
        self.null_zehn = eins
        self.zehn_zwanzig = zwei
        self.zwanzig_dreisig = drei
        self.dreisig_vierzig = vier
        self.vierzig_fünfzig = fünf
        self.fünfzig_sechzig = sechs
        self.sechzig_siebzig = sieben
        self.siebzig_achzieg = acht
        self.achzig_neunzig = neun
        self.neunzig_hunndert = zehn


    def to_dict(self):
        """returns the object as dict"""
        dicts = {
            "id": self.id,
            "gameId": self.game_id,
            "participantId": self.participant_id,
            "0-10": self.null_zehn,
            "10-20": self.zehn_zwanzig,
            "20-30": self.zwanzig_dreisig,
            "30-40": self.dreisig_vierzig,
            "40-50": self.vierzig_fünfzig,
            "50-60": self.fünfzig_sechzig,
            "60-70": self.sechzig_siebzig,
            "70-80": self.siebzig_achzieg,
            "80-90": self.achzig_neunzig,
            "90-100": self.neunzig_hunndert
            }
        return dicts

    @classmethod
    def find_by_id(cls,id):
        """ id = gameId and participantId """
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def get_all_XpDiffPerMinDeltas(cls):
        """return a list of XpDiffPerMinDeltas objects from all your XpDiffPerMinDeltas in the Database """
        return session.query(cls).all()

    def insert_to_db(self):
        session.add(self)
        session.commit()

    def add(self):
        session.add(self)

    @classmethod
    def commit(cls):
        session.commit()


class CreepsPerMinDeltas(Base):

    __tablename__ = "CreepsPerMinDeltas"

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer)
    participant_id = Column(Integer)
    null_zehn = Column(Float)
    zehn_zwanzig = Column(Float)
    zwanzig_dreisig = Column(Float)
    dreisig_vierzig = Column(Float)
    vierzig_fünfzig = Column(Float)
    fünfzig_sechzig = Column(Float)
    sechzig_siebzig = Column(Float)
    siebzig_achzieg = Column(Float)
    achzig_neunzig = Column(Float)
    neunzig_hunndert = Column(Float)

    def __init__(self, gameId, participantId, eins, zwei, drei, vier, fünf, sechs, sieben, acht, neun, zehn):
        self.id = int(str(gameId)+str(participantId))
        self.game_id = gameId
        self.participant_id = participantId
        self.null_zehn = eins
        self.zehn_zwanzig = zwei
        self.zwanzig_dreisig = drei
        self.dreisig_vierzig = vier
        self.vierzig_fünfzig = fünf
        self.fünfzig_sechzig = sechs
        self.sechzig_siebzig = sieben
        self.siebzig_achzieg = acht
        self.achzig_neunzig = neun
        self.neunzig_hunndert = zehn

    def to_dict(self):
        """returns the object as dict"""
        dicts = {
            "id": self.id,
            "gameId": self.game_id,
            "participantId": self.participant_id,
            "0-10": self.null_zehn,
            "10-20": self.zehn_zwanzig,
            "20-30": self.zwanzig_dreisig,
            "30-40": self.dreisig_vierzig,
            "40-50": self.vierzig_fünfzig,
            "50-60": self.fünfzig_sechzig,
            "60-70": self.sechzig_siebzig,
            "70-80": self.siebzig_achzieg,
            "80-90": self.achzig_neunzig,
            "90-100": self.neunzig_hunndert
            }
        return dicts

    @classmethod
    def find_by_id(cls, id):
        """ id = gameId and participantId """
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def get_all_CreepsPerMinDeltas(cls):
        """return a list of CreepsPerMinDeltas objects from all your CreepsPerMinDeltas in the Database """
        return session.query(cls).all()

    def insert_to_db(self):
        session.add(self)
        session.commit()

    def add(self):
        session.add(self)

    @classmethod
    def commit(cls):
        session.commit()


class XpPerMinDeltas(Base):

    __tablename__ = "XpPerMinDeltas"

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer)
    participant_id = Column(Integer)
    null_zehn = Column(Float)
    zehn_zwanzig = Column(Float)
    zwanzig_dreisig = Column(Float)
    dreisig_vierzig = Column(Float)
    vierzig_fünfzig = Column(Float)
    fünfzig_sechzig = Column(Float)
    sechzig_siebzig = Column(Float)
    siebzig_achzieg = Column(Float)
    achzig_neunzig = Column(Float)
    neunzig_hunndert = Column(Float)

    def __init__(self, gameId, participantId, eins, zwei, drei, vier, fünf, sechs, sieben, acht, neun, zehn):
        self.id = int(str(gameId)+str(participantId))
        self.game_id = gameId
        self.participant_id = participantId
        self.null_zehn = eins
        self.zehn_zwanzig = zwei
        self.zwanzig_dreisig = drei
        self.dreisig_vierzig = vier
        self.vierzig_fünfzig = fünf
        self.fünfzig_sechzig = sechs
        self.sechzig_siebzig = sieben
        self.siebzig_achzieg = acht
        self.achzig_neunzig = neun
        self.neunzig_hunndert = zehn

    def to_dict(self):
        """returns the object as dict"""
        dicts = {
            "id": self.id,
            "gameId": self.game_id,
            "participantId": self.participant_id,
            "0-10": self.null_zehn,
            "10-20": self.zehn_zwanzig,
            "20-30": self.zwanzig_dreisig,
            "30-40": self.dreisig_vierzig,
            "40-50": self.vierzig_fünfzig,
            "50-60": self.fünfzig_sechzig,
            "60-70": self.sechzig_siebzig,
            "70-80": self.siebzig_achzieg,
            "80-90": self.achzig_neunzig,
            "90-100": self.neunzig_hunndert
            }
        return dicts

    @classmethod
    def find_by_id(cls, id):
        """ id = gameId and participantId """
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def get_all_XpPerMinDeltas(cls):
        """return a list of XpPerMinDeltas objects from all your XpPerMinDeltas in the Database """
        return session.query(cls).all()

    def insert_to_db(self):
        session.add(self)
        session.commit()

    def add(self):
        session.add(self)

    @classmethod
    def commit(cls):
        session.commit()


class DamageTakenDiffPerMinDeltas(Base):

    __tablename__ = "DamageTakenDiffPerMinDeltas"

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer)
    participant_id = Column(Integer)
    null_zehn = Column(Float)
    zehn_zwanzig = Column(Float)
    zwanzig_dreisig = Column(Float)
    dreisig_vierzig = Column(Float)
    vierzig_fünfzig = Column(Float)
    fünfzig_sechzig = Column(Float)
    sechzig_siebzig = Column(Float)
    siebzig_achzieg = Column(Float)
    achzig_neunzig = Column(Float)
    neunzig_hunndert = Column(Float)

    def __init__(self, gameId, participantId, eins, zwei, drei, vier, fünf, sechs, sieben, acht, neun, zehn):
        self.id = int(str(gameId)+str(participantId))
        self.game_id = gameId
        self.participant_id = participantId
        self.null_zehn = eins
        self.zehn_zwanzig = zwei
        self.zwanzig_dreisig = drei
        self.dreisig_vierzig = vier
        self.vierzig_fünfzig = fünf
        self.fünfzig_sechzig = sechs
        self.sechzig_siebzig = sieben
        self.siebzig_achzieg = acht
        self.achzig_neunzig = neun
        self.neunzig_hunndert = zehn

    def to_dict(self):
        """returns the objects as dict"""
        dicts = {
            "id": self.id,
            "gameId": self.game_id,
            "participantId": self.participant_id,
            "0-10": self.null_zehn,
            "10-20": self.zehn_zwanzig,
            "20-30": self.zwanzig_dreisig,
            "30-40": self.dreisig_vierzig,
            "40-50": self.vierzig_fünfzig,
            "50-60": self.fünfzig_sechzig,
            "60-70": self.sechzig_siebzig,
            "70-80": self.siebzig_achzieg,
            "80-90": self.achzig_neunzig,
            "90-100": self.neunzig_hunndert
            }
        return dicts

    @classmethod
    def find_by_id(cls,id):
        """ id = gameId and participantId """
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def get_all_DamageTakenDiffPerMinDeltas(cls):
        """return a list of DamageTakenDiffPerMinDeltas objects from all your DamageTakenDiffPerMinDeltas in the Database """
        return session.query(cls).all()

    def insert_to_db(self):
        session.add(self)
        session.commit()

    def add(self):
        session.add(self)

    @classmethod
    def commit(cls):
        session.commit()


class DamageTakenPerMinDeltas(Base):

    __tablename__ = "DamageTakenPerMinDeltas"

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer)
    participant_id = Column(Integer)
    null_zehn = Column(Float)
    zehn_zwanzig = Column(Float)
    zwanzig_dreisig = Column(Float)
    dreisig_vierzig = Column(Float)
    vierzig_fünfzig = Column(Float)
    fünfzig_sechzig = Column(Float)
    sechzig_siebzig = Column(Float)
    siebzig_achzieg = Column(Float)
    achzig_neunzig = Column(Float)
    neunzig_hunndert = Column(Float)

    def __init__(self, gameId, participantId, eins, zwei, drei, vier, fünf, sechs, sieben, acht, neun, zehn):
        self.id = int(str(gameId)+str(participantId))
        self.game_id = gameId
        self.participant_id = participantId
        self.null_zehn = eins
        self.zehn_zwanzig = zwei
        self.zwanzig_dreisig = drei
        self.dreisig_vierzig = vier
        self.vierzig_fünfzig = fünf
        self.fünfzig_sechzig = sechs
        self.sechzig_siebzig = sieben
        self.siebzig_achzieg = acht
        self.achzig_neunzig = neun
        self.neunzig_hunndert = zehn

    def to_dict(self):
        """returns the object as a dict"""
        return {
            "id": self.id,
            "gameId": self.game_id,
            "participantId": self.participant_id,
            "0-10": self.null_zehn,
            "10-20": self.zehn_zwanzig,
            "20-30": self.zwanzig_dreisig,
            "30-40": self.dreisig_vierzig,
            "40-50": self.vierzig_fünfzig,
            "50-60": self.fünfzig_sechzig,
            "60-70": self.sechzig_siebzig,
            "70-80": self.siebzig_achzieg,
            "80-90": self.achzig_neunzig,
            "90-100": self.neunzig_hunndert
            }

    @classmethod
    def find_by_id(cls, id):
        """ id = gameId and participantId """
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def get_all_DamageTakenPerMinDeltas(cls):
        """return a list of DamageTakenPerMinDeltas objects from all your DamageTakenPerMinDeltas in the Database """
        return session.query(cls).all()

    def insert_to_db(self):
        session.add(self)
        session.commit()

    def add(self):
        session.add(self)

    @classmethod
    def commit(cls):
        session.commit()


class Timeline(Base):

    __tablename__ = "Timeline"

    id = Column(Integer,ForeignKey('CsDiffPerMinDeltas.id'),ForeignKey('GoldPerMinDeltas.id'),ForeignKey('XpDiffPerMinDeltas.id'),ForeignKey('CreepsPerMinDeltas.id'),ForeignKey('XpPerMinDeltas.id'),ForeignKey('DamageTakenDiffPerMinDeltas.id'),ForeignKey('DamageTakenPerMinDeltas.id'), primary_key=True)
    game_id = Column(Integer)
    lane = Column(String)
    participant_id = Column(Integer)
    role = Column(String)
    cs_diff_per_min_deltas = relationship('CsDiffPerMinDeltas', viewonly=True)
    gold_per_min_deltas = relationship('GoldPerMinDeltas', viewonly=True)
    xp_diff_per_min_deltas = relationship('XpDiffPerMinDeltas', viewonly=True)
    creeps_per_min_deltas = relationship('CreepsPerMinDeltas', viewonly=True)
    xp_per_min_deltas = relationship('XpPerMinDeltas', viewonly=True)
    damage_taken_diff_per_min_deltas = relationship('DamageTakenDiffPerMinDeltas',viewonly=True)
    damage_taken_per_min_deltas = relationship('DamageTakenPerMinDeltas', viewonly=True)

    def __init__(self, gameId, lane, participantId, role):
        self.id = int(str(gameId)+str(participantId))
        self.game_id = gameId
        self.lane = lane
        self.participant_id = participantId
        self.role = role

    def to_dict(self):
        """returns the object as a dict"""
        return {
            "id": self.id,
            "gameId": self.game_id,
            "lane": self.lane,
            "participantId": self.participant_id,
            "role": self.role
            }

    @classmethod
    def find_by_id(cls,id):
        """ id = gameId and participantId """
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def get_all_timeline(cls):
        """return all Timelines from the Database """
        return session.query(cls).all()

    def insert_to_db(self):
        session.add(self)
        session.commit()

    def add(self):
        session.add(self)

    @classmethod
    def commit(cls):
        session.commit()


class ParticipantIdentities(Base):
    
    __tablename__ = "ParticipantIdentities"

    current_platform_id = Column(String(10))
    summoner_name = Column(String(20))
    match_history_uri = Column(String)
    platform_id = Column(String)
    current_account_id = Column(Integer)
    profile_icon_id = Column(Integer)
    summoner_id = Column(Integer)
    account_id = Column(Integer)
    participant_id = Column(Integer)
    game_id = Column(Integer)
    id = Column(Integer, primary_key=True, unique=True)
    key_for_stats = Column(Integer, ForeignKey("Stats.id"), ForeignKey("Timeline.id"), ForeignKey("Participants.id"))
    stats = relationship("Stats", viewonly=True)
    timeline = relationship("Timeline", viewonly=True)
    participants = relationship("Participants", viewonly=True)

    def __init__(self, currentPlatformId, summonerName, matchHistoryUri, platformId, currentAccountId, profileIcon, summonerId, accountId, participantId, gameId):
        self.current_platform_id = currentPlatformId
        self.summoner_name = summonerName
        self.match_history_uri = matchHistoryUri
        self.platform_id = platformId
        self.current_account_id = currentAccountId
        self.profile_icon_id = profileIcon
        self.summoner_id = summonerId
        self.account_id = accountId
        self.participant_id = participantId
        self.game_id = gameId
        self.id = int(str(gameId)+str(summonerId))
        self.key_for_stats = int(str(gameId)+str(participantId))

    def to_dict(self):
        """returns the object as a dict"""
        return {
            "currentPlatformId": self.current_platform_id,
            "summonerName": self.summoner_name,
            "matchHistoryUri": self.match_history_uri,
            "platformId": self.platform_id,
            "currentAccountId": self.current_account_id,
            "profileIconId": self.profile_icon_id,
            "summonerId": self.summoner_id,
            "accountId": self.account_id,
            "participantId": self.participant_id,
            "gameId": self.game_id,
            "id": self.id,
            "keyForStats": self.key_for_stats
            }

    @classmethod
    def find_by_id(cls, id):
        """ id = gameId and summonerId"""
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def get_all(cls):
        """return all Participantidentities from the Database"""
        return session.query(cls).all()

    def insert_to_db(self):
        session.add(self)
        session.commit()

    def add(self):
        session.add(self)

    @classmethod
    def commit(cls):
        session.commit()


class BigMatch(Base):
    __tablename__ = "BigMatch"
    season_id = Column(String)
    queue_id = Column(Integer)
    game_id = Column(Integer, ForeignKey("ParticipantIdentities.game_id"),ForeignKey("Team.game_id"), primary_key=True, unique=True)
    game_version = Column(String)
    platform_id = Column(String)
    game_mode = Column(String)
    map_id = Column(Integer)
    game_type = Column(String)
    game_duration = Column(Integer)
    game_creation = Column(Integer)
    player = relationship('ParticipantIdentities', viewonly=True)
    teams = relationship('Team', viewonly=True)

    def __init__(self, seasonId, queueId, gameId, gameVersion, platformId, gameMode, mapId, gameType, gameDuration, gameCreation):
        self.season_id = seasonId
        self.queue_id = queueId
        self.game_id = gameId
        self.game_version = gameVersion
        self.platform_id = platformId
        self.game_mode = gameMode
        self.map_id = mapId
        self.game_type = gameType
        self.game_duration = gameDuration
        self.game_creation = gameCreation

    def to_dict(self):
        """returns the object as a dict"""
        return {
            "seasonId": self.season_id,
            "queueId": self.queue_id,
            "gameId": self.game_id,
            "gameVersion": self.game_version,
            "platformId": self.platform_id,
            "gameMode": self.game_mode,
            "mapId": self.map_id,
            "gameType": self.game_type,
            "gameDuration": self.game_duration,
            "gameCreation": self.game_creation
            }

    @classmethod
    def find_by_id(cls, game_id):
        """ id = gameId """
        return session.query(cls).filter_by(game_id=game_id).first()

    def get_participant_identities(self, summoner_id):
        return self.player.find_by_id(int(str(self.game_id)+str(summoner_id)))

    def get_team_by_id(self, team_id):
        return self.teams.find_by_id(int(str(self.game_id)+str(team_id)))

    @classmethod
    def get_all(cls):
        """return all BigMatches from the Database"""
        return session.query(cls).all()
    
    def insert_to_db(self):
        session.add(self)
        session.commit()

    def add(self):
        session.add(self)

    @classmethod
    def commit(cls):
        session.commit()


class Team(Base):
    __tablename__ = "Team"

    first_dragon = Column(String)
    first_inhibitor = Column(String)
    win = Column(String)
    first_rift_herald = Column(String)
    first_baron = Column(String)
    baron_kils = Column(Integer)
    rift_herald_kills = Column(Integer)
    first_blood = Column(String)
    team_id = Column(Integer)
    first_tower = Column(String)
    vilemaw_kills = Column(Integer)
    inhibitor_kills = Column(Integer)
    tower_kills = Column(Integer)
    dominion_victory_score = Column(Integer)
    dragon_kills = Column(Integer)
    id = Column(Integer, ForeignKey("Bans.id"), primary_key=True, unique=True)
    game_id = Column(Integer)
    bans = relationship('Bans', viewonly=True)

    def __init__(self, firstDragon, firstInhibitor, win, firstRiftHerald, firstBaron, baronKills, riftHeraldKills, firstBlood, teamId, firstTower, vilemawKills, inhibitorKills, towerKills, dominionVictoryScore, dragonKills, gameId):
        self.first_dragon = firstDragon
        self.first_inhibitor = firstInhibitor
        self.win = win
        self.first_rift_herald = firstRiftHerald
        self.first_baron = firstBaron
        self.baron_kils = baronKills
        self.rift_herald_kills = riftHeraldKills
        self.first_blood = firstBlood
        self.team_id = teamId
        self.first_tower = firstTower
        self.vilemaw_kills = vilemawKills
        self.inhibitor_kills = inhibitorKills
        self.tower_kills = towerKills
        self.dominion_victory_score = dominionVictoryScore
        self.dragon_kills = dragonKills
        self.id = int(str(gameId)+str(teamId))
        self.game_id = gameId

    def to_dict(self):
        """returns the object as a dict"""
        return {
            "firstDragon": self.first_dragon,
            "firstInhibitor": self.first_inhibitor,
            "win": self.win,
            "firstRiftHerald": self.first_rift_herald,
            "firstBaron": self.first_baron,
            "baronKills": self.baron_kils,
            "riftHeraldKills": self.rift_herald_kills,
            "firstBlood": self.first_blood,
            "teamId": self.team_id,
            "firstTower": self.first_tower,
            "vilemawKills": self.vilemaw_kills,
            "inhibitorKills": self.inhibitor_kills,
            "towerKills": self.tower_kills,
            "dominionVictoryScore": self.dominion_victory_score,
            "dragonKills": self.dragon_kills,
            "id": self.id,
            "gameId": self.game_id
            }

    @classmethod
    def find_by_ids(cls, game_id, team_id):
        """ game_id team_id """
        return session.query(cls).filter_by(id = int(str(game_id)+str(team_id))).first()

    @classmethod
    def get_all(cls):
        """return an generator of all Teams"""
        return session.query(cls).all()

    def insert_to_db(self):
        session.add(self)
        session.commit()

    def add(self):
        session.add(self)

    @classmethod
    def commit(cls):
        session.commit()


class Bans(Base):

    __tablename__  = "Bans"

    game_id = Column(Integer)
    team_id = Column(Integer)
    id = Column(Integer, primary_key=True)
    champion_id1 = Column(Integer)
    champion_id2 = Column(Integer)
    champion_id3 = Column(Integer)
    champion_id4 = Column(Integer)
    champion_id5 = Column(Integer)

    def __init__(self, gameId, teamId, championId1, championId2, championId3, championId4, championId5):
        self.game_id = gameId
        self.team_id = teamId
        self.id = int(str(gameId)+str(teamId))
        self.champion_id1 = championId1
        self.champion_id2 = championId2
        self.champion_id3 = championId3
        self.champion_id4 = championId4
        self.champion_id5 = championId5

    def to_dict(self):
        """returns the object as a dict"""
        return {
            "gameId": self.game_id,
            "teamId": self.team_id,
            "id": self.id,
            "championId1": self.champion_id1,
            "championId2": self.champion_id2,
            "championId3": self.champion_id3,
            "championId4": self.champion_id4,
            "championId5": self.champion_id5
            }

    @classmethod
    def find_by_ids(cls, game_id, team_id):
        return session.query(cls).filter_by(id = int(str(game_id)+str(team_id))).first()

    @classmethod
    def get_all(cls):
        """return all Bans from the Database"""
        return session.query(cls).all()

    def insert_to_db(self):
        session.add(self)
        session.commit()

    def add(self):
        session.add(self)

    @classmethod
    def commit(cls):
        session.commit()


class Stats(Base):
    
    __tablename__ = "Stats"
    
    id = Column(Integer, primary_key=True)
    player_score0 = Column(Integer)
    player_score1 = Column(Integer)
    player_score2 = Column(Integer)
    player_score3 = Column(Integer)
    player_score4 = Column(Integer)
    player_score5 = Column(Integer)
    player_score6 = Column(Integer)
    player_score7 = Column(Integer)
    player_score8 = Column(Integer)
    player_score9 = Column(Integer)
    magic_damage_dealt = Column(Integer)
    magic_damage_dealt_to_champions = Column(Integer)
    magic_damage_taken = Column(Integer)
    total_damage_dealt = Column(Integer)
    total_damage_dealt_to_champions = Column(Integer)
    total_damage_taken = Column(Integer)
    physical_damage_dealt = Column(Integer)
    physical_damage_dealt_to_champions = Column(Integer)
    physical_damage_taken = Column(Integer)
    true_damage_dealt = Column(Integer)
    true_damage_dealt_to_champions = Column(Integer)
    true_damage_taken = Column(Integer)
    vision_score = Column(Integer)
    wards_placed = Column(Integer)
    sight_wards_bought_in_game = Column(Integer)
    vision_wards_bought_in_game = Column(Integer)
    total_time_crowd_control_dealt = Column(Integer)
    longest_time_spent_living = Column(Integer)
    totale_score_rank = Column(Integer)
    total_units_healed = Column(Integer)
    lagest_critical_strike = Column(Integer)
    first_blood_assist = Column(String)
    gold_spent = Column(Integer)
    gold_earned = Column(Integer)
    participant_id = Column(Integer)
    objective_player_score = Column(Integer)
    combat_player_score = Column(Integer)
    total_player_score = Column(Integer)
    win = Column(String)
    total_heal = Column(Integer)
    time_ccing_others = Column(Integer)
    champion_level = Column(Integer)
    neutral_minions_killed = Column(Integer)
    total_minions_killed = Column(Integer)
    neutral_minions_killed_team_jungle = Column(Integer)
    neutral_minions_killed_enemy_jungle = Column(Integer)
    largest_multi_kill = Column(Integer)
    largest_killing_spree = Column(Integer)
    killing_sprees = Column(Integer)
    unreal_kills = Column(Integer)
    double_kills = Column(Integer)
    triple_kills = Column(Integer)
    quadra_kills = Column(Integer)
    penta_kills = Column(Integer)
    kills = Column(Integer)
    deaths = Column(Integer)
    assists = Column(Integer)
    first_blood_kill = Column(String)
    wards_killed = Column(Integer)
    first_inhibitor_kill = Column(String)
    first_inhibitor_assist = Column(String)
    first_tower_kill = Column(String)
    first_tower_assist = Column(String)
    turret_kills = Column(Integer)
    inhibitor_kills = Column(Integer)
    item0 = Column(Integer)
    item1 = Column(Integer)
    item2 = Column(Integer)
    item3 = Column(Integer)
    item4 = Column(Integer)
    item5 = Column(Integer)
    item6 = Column(Integer)
    perk_primary_style = Column(Integer)
    perk_sub_style = Column(Integer)
    perk0 = Column(Integer)
    perk1 = Column(Integer)
    perk2 = Column(Integer)
    perk3 = Column(Integer)
    perk4 = Column(Integer)
    perk5 = Column(Integer)
    perk0_var1 = Column(Integer)
    perk0_var2 = Column(Integer)
    perk0_var3 = Column(Integer)
    perk1_var1 = Column(Integer)
    perk1_var2 = Column(Integer)
    perk1_var3 = Column(Integer)
    perk2_var1 = Column(Integer)
    perk2_var2 = Column(Integer)
    perk2_var3 = Column(Integer)
    perk3_var1 = Column(Integer)
    perk3_var2 = Column(Integer)
    perk3_var3 = Column(Integer)
    perk4_var1 = Column(Integer)
    perk4_var2 = Column(Integer)
    perk4_var3 = Column(Integer)
    perk5_var1 = Column(Integer)
    perk5_var2 = Column(Integer)
    perk5_var3 = Column(Integer)

    def __init__(self, gameId,  neutralMinionsKilledTeamJungle, visionScore, magicDamageDealtToChampions, largestMultiKill, totalTimeCrowdControlDealt, longestTimeSpentLiving, perk1Var1, perk1Var3, perk1Var2,
                tripleKills, perk5, perk4, playerScore9, playerScore8, kills, playerScore1, playerScore0, playerScore3, playerScore2, playerScore5, playerScore4, playerScore7, playerScore6, perk5Var1,
                perk5Var3, perk5Var2, totalScoreRank, neutralMinionsKilled, damageDealtToTurrets, physicalDamageDealtToChampions, damageDealtToObjectives, perk2Var2, perk2Var3, totalUnitsHealed, perk2Var1,
                perk4Var1, totalDamageTaken, perk4Var3, wardsKilled, largestCriticalStrike, largestKillingSpree, quadraKills, magicDamageDealt, firstBloodAssist, item2, item3, item0, item1, item6, item4, item5,
                perk1, perk0, perk3, perk2, perk3Var3, perk3Var2, perk3Var1, damageSelfMitigated, magicalDamageTaken, perk0Var2, firstInhibitorKill, trueDamageTaken, assists, perk4Var2, goldSpent, trueDamageDealt,
                participantId, physicalDamageDealt, sightWardsBoughtInGame, totalDamageDealtToChampions, physicalDamageTaken, totalPlayerScore, win, objectivePlayerScore, totalDamageDealt, neutralMinionsKilledEnemyJungle,
                deaths, wardsPlaced, perkPrimaryStyle, perkSubStyle, turretKills, firstBloodKill, trueDamageDealtToChampions, goldEarned, killingSprees, unrealKills, firstTowerAssist, firstTowerKill, champLevel,
                doubleKills, inhibitorKills, firstInhibitorAssist, perk0Var1, combatPlayerScore, perk0Var3, visionWardsBoughtInGame, pentaKills, totalHeal, totalMinionsKilled, timeCCingOthers):

        self.id = int(str(gameId)+str(participantId))
        self.player_score0 = playerScore0
        self.player_score1 = playerScore1
        self.player_score2 = playerScore2
        self.player_score3 = playerScore3
        self.player_score4 = playerScore4
        self.player_score5 = playerScore5
        self.player_score6 = playerScore6
        self.player_score7 = playerScore7
        self.player_score8 = playerScore8
        self.player_score9 = playerScore9
        self.magic_damage_dealt_to_champions = magicDamageDealtToChampions
        self.magic_damage_dealt = magicDamageDealt
        self.magic_damage_taken = magicalDamageTaken
        self.total_damage_taken = totalDamageTaken
        self.total_damage_dealt_to_champions = totalDamageDealtToChampions
        self.total_damage_dealt = totalDamageDealt
        self.physical_damage_taken = physicalDamageTaken
        self.physical_damage_dealt_to_champions = physicalDamageDealtToChampions
        self.physical_damage_dealt = physicalDamageDealt
        self.true_damage_taken = trueDamageTaken
        self.true_damage_dealt_to_champions = trueDamageDealtToChampions
        self.true_damage_dealt = trueDamageDealt
        self.damage_dealt_to_turrets = damageDealtToTurrets
        self.damage_gealt_to_objectives = damageDealtToObjectives
        self.damage_self_mitigated = damageSelfMitigated
        self.vision_score = visionScore
        self.wards_placed = wardsPlaced
        self.sight_wards_bought_in_game = sightWardsBoughtInGame
        self.vision_wards_bought_in_game = visionWardsBoughtInGame
        self.total_time_crowd_control_dealt = totalTimeCrowdControlDealt
        self.longest_time_spent_living = longestTimeSpentLiving
        self.totale_score_rank = totalScoreRank
        self.total_units_healed = totalUnitsHealed
        self.lagest_critical_strike = largestCriticalStrike
        self.first_blood_assist = firstBloodAssist
        self.gold_spent = goldSpent
        self.gold_earned = goldEarned
        self.participant_id = participantId
        self.objective_player_score = objectivePlayerScore
        self.combat_player_score = combatPlayerScore
        self.total_player_score = totalPlayerScore
        self.win = win
        self.total_heal = totalHeal
        self.time_ccing_others = timeCCingOthers
        self.champion_level = champLevel
        self.neutral_minions_killed = neutralMinionsKilled
        self.total_minions_killed = totalMinionsKilled
        self.neutral_minions_killed_team_jungle = neutralMinionsKilledTeamJungle
        self.neutral_minions_killed_enemy_jungle = neutralMinionsKilledEnemyJungle
        self.largest_multi_kill = largestMultiKill
        self.largest_killing_spree = largestKillingSpree
        self.killing_sprees = killingSprees
        self.unreal_kills = unrealKills
        self.double_kills = doubleKills
        self.triple_kills = tripleKills
        self.quadra_kills = quadraKills
        self.penta_kills = pentaKills
        self.kills = kills
        self.deaths = deaths
        self.assists = assists
        self.first_blood_kill = firstBloodKill
        self.wards_killed = wardsKilled
        self.first_inhibitor_kill = firstInhibitorKill
        self.first_inhibitor_assist = firstInhibitorAssist
        self.first_tower_kill = firstTowerKill
        self.first_tower_assist = firstTowerAssist
        self.turret_kills = turretKills
        self.inhibitor_kills = inhibitorKills
        self.item0 = item0
        self.item1 = item1
        self.item2 = item2
        self.item3 = item3
        self.item4 = item4
        self.item5 = item5
        self.item6 = item6
        self.perk_primary_style = perkPrimaryStyle
        self.perk_sub_style = perkSubStyle
        self.perk0 = perk0
        self.perk1 = perk1
        self.perk2 = perk2
        self.perk3 = perk3
        self.perk4 = perk4
        self.perk5 = perk5
        self.perk0_var1 = perk0Var1
        self.perk0_var2 = perk0Var2
        self.perk0_var3 = perk0Var3
        self.perk1_var1 = perk1Var1
        self.perk1_var2 = perk1Var2
        self.perk1_var3 = perk1Var3
        self.perk2_var1 = perk2Var1
        self.perk2_var2 = perk2Var2
        self.perk2_var3 = perk2Var3
        self.perk3_var1 = perk3Var1
        self.perk3_var2 = perk3Var2
        self.perk3_var3 = perk3Var3
        self.perk4_var1 = perk4Var1
        self.perk4_var2 = perk4Var2
        self.perk4_var3 = perk4Var3
        self.perk5_var1 = perk5Var1
        self.perk5_var2 = perk5Var2
        self.perk5_var3 = perk5Var3

    def to_dict(self):
        """returns the object as a dict"""
        return {
            "id": self.id,
            "playerScore0": self.player_score0,
            "playerScore1": self.player_score1,
            "playerScore2": self.player_score2,
            "playerScore3": self.player_score3,
            "playerScore4": self.player_score4,
            "playerScore5": self.player_score5,
            "playerScore6": self.player_score6,
            "playerScore7": self.player_score7,
            "playerScore8": self.player_score8,
            "playerScore9": self.player_score9,
            "magicDamageDealtToChampions":self.magic_damage_dealt_to_champions,
            "magicDamageDealt": self.magic_damage_dealt,
            "magicalDamageTaken": self.magic_damage_taken,
            "totalDamageTaken": self.total_damage_taken,
            "totalDamageDealtToChampions": self.total_damage_dealt_to_champions,
            "totalDamageDealt": self.total_damage_dealt,
            "physicalDamageTaken": self.physical_damage_taken,
            "physicalDamageDealtToChampions": self.physical_damage_dealt_to_champions,
            "physicalDamageDealt": self.physical_damage_dealt,
            "trueDamageTaken": self.true_damage_taken,
            "trueDamageDealtToChampions": self.true_damage_dealt_to_champions,
            "trueDamageDealt": self.true_damage_dealt,
            "damageDealtToTurrets": self.damage_dealt_to_turrets,
            "damageDealtToObjectives": self.damage_gealt_to_objectives,
            "damageSelfMitigated": self.damage_self_mitigated,
            "visionScore": self.vision_score,
            "wardsPlaced": self.wards_placed,
            "sightWardsBoughtInGame": self.sight_wards_bought_in_game,
            "visionWardsBoughtInGame": self.vision_wards_bought_in_game,
            "totalTimeCrowdControlDealt": self.total_time_crowd_control_dealt,
            "longestTimeSpentLiving": self.longest_time_spent_living,
            "totalScoreRank": self.totale_score_rank,
            "totalUnitsHealed": self.total_units_healed,
            "largestCriticalStrike": self.lagest_critical_strike,
            "firstBloodAssist": self.first_blood_assist,
            "goldSpent": self.gold_spent,
            "goldEarned": self.gold_earned,
            "participantId": self.participant_id,
            "objectivePlayerScore": self.objective_player_score,
            "combatPlayerScore": self.combat_player_score,
            "totalPlayerScore": self.total_player_score,
            "win": self.win,
            "totalHeal": self.total_heal,
            "timeCCingOthers": self.time_ccing_others,
            "champLevel": self.champion_level,
            "neutralMinionsKilled": self.neutral_minions_killed,
            "totalMinionsKilled": self.total_minions_killed,
            "neutralMinionsKilledTeamJungle": self.neutral_minions_killed_team_jungle,
            "neutralMinionsKilledEnemyJungle": self.neutral_minions_killed_enemy_jungle,
            "largestMultiKill": self.largest_multi_kill,
            "largestKillingSpree": self.largest_killing_spree,
            "killingSprees": self.killing_sprees,
            "unrealKills": self.unreal_kills,
            "doubleKills": self.double_kills,
            "tripleKills": self.triple_kills,
            "quadraKills": self.quadra_kills,
            "pentaKills": self.penta_kills,
            "kills": self.kills,
            "deaths": self.deaths,
            "assists": self.assists,
            "firstBloodKill": self.first_blood_kill,
            "wardsKilled": self.wards_killed,
            "firstInhibitorKill": self.first_inhibitor_kill,
            "firstInhibitorAssist": self.first_inhibitor_assist,
            "firstTowerKill": self.first_tower_kill,
            "firstTowerAssist": self.first_tower_assist,
            "turretKills": self.turret_kills,
            "inhibitorKills": self.inhibitor_kills,
            "item0": self.item0,
            "item1": self.item1,
            "item2": self.item2,
            "item3": self.item3,
            "item4": self.item4,
            "item5": self.item5,
            "item6": self.item6,
            "perkPrimaryStyle": self.perk_primary_style,
            "perkSubStyle": self.perk_sub_style,
            "perk0": self.perk0,
            "perk1": self.perk1,
            "perk2": self.perk2,
            "perk3": self.perk3,
            "perk4": self.perk4,
            "perk5": self.perk5,
            "perk0Var1": self.perk0_var1,
            "perk0Var2": self.perk0_var2,
            "perk0Var3": self.perk0_var3,
            "perk1Var1": self.perk1_var1,
            "perk1Var2": self.perk1_var2,
            "perk1Var3": self.perk1_var3,
            "perk2Var1": self.perk2_var1,
            "perk2Var2": self.perk2_var2,
            "perk2Var3": self.perk2_var3,
            "perk3Var1": self.perk3_var1,
            "perk3Var2": self.perk3_var2,
            "perk3Var3": self.perk3_var3,
            "perk4Var1": self.perk4_var1,
            "perk4Var2": self.perk4_var2,
            "perk4Var3": self.perk4_var3,
            "perk5Var1": self.perk5_var1,
            "perk5Var2": self.perk5_var2,
            "perk5Var3": self.perk5_var3,
            }

    @classmethod
    def find_by_id(cls, game_id, team_id):
        """return Stats object for the given ids from the Database"""
        return session.query(cls).filter_by(id=int(str(game_id) + str(team_id))).first()

    @classmethod
    def get_all(cls):
        """returns all Stats from the Database"""
        return session.query(cls).all()

    def insert_to_db(self):
        session.add(self)
        session.commit()

    def add(self):
        session.add(self)

    @classmethod
    def commit(cls):
        session.commit()


class Participants(Base):
    __tablename__ = "Participants"

    id = Column(Integer, ForeignKey('Stats.id'),ForeignKey('Timeline.id'), primary_key=True)
    game_id = Column(Integer)
    participant_id = Column(Integer)
    spell1_id = Column(Integer)
    spell2_id = Column(Integer)
    highest_achiecved_season_tier = Column(String)
    team_id = Column(Integer)
    champion_id = Column(Integer)
    stats = relationship('Stats', viewonly=True)
    timeline = relationship('Timeline', viewonly=True)

    def __init__(self, gameId, spell1Id, participantId, highestAchievedSeasonTier, spell2Id, teamId, championId):        
        self.id = int(str(gameId)+ str(participantId))
        self.game_id = gameId
        self.spell1_id = spell1Id
        self.participant_id = participantId
        self.highest_achiecved_season_tier = highestAchievedSeasonTier
        self.spell2_id = spell2Id
        self.team_id = teamId
        self.champion_id = championId

    def to_dict(self):
        """returns the object as a dict"""
        return {
            "id": self.id,
            "gameId": self.game_id,
            "spell1Id": self.spell1_id,
            "spell2Id": self.spell2_id,
            "participantId": self.participant_id,
            "highestAchievedSeasonTier": self.highest_achiecved_season_tier,
            "teamId": self.team_id,
            "championId": self.champion_id
            }

    @classmethod
    def find_by_id(cls, _id):
        """id = gameId and participantId """
        return session.query(cls).filter_by(id=_id).first()

    @classmethod
    def get_all(cls):
        """return all Participants from the Database"""
        return session.query(cls).all()

    def insert_to_db(self):
        session.add(self)
        session.commit()

    def add(self):
        session.add(self)

    @classmethod
    def commit(cls):
        session.commit()


class Item(Base):

    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    plaintext = Column(String)
    description = Column(String)

    def __init__(self, id , name, description = '', plaintext = ''):
        """The Leauge of Legends Item some of the response dont have a description or plaintext so the default if an
        empty String"""
        self.id = id
        self.name = name
        self.plaintext = plaintext
        self.description = description

    def to_dict(self):
        """returns the object as a dict"""
        return {'id': self.id,
         'name': self.name,
         'plaintext': self.plaintext,
         'description': self.description}

    @classmethod
    def find_by_id(cls, id):
        """returns an item by the given id"""
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        """returns an item by the given name"""
        return session.query(cls).filter_by(name=name).first()

    @classmethod
    def get_all(cls):
        """returns all items from the Database"""
        return session.query(cls).all()

    def insert_to_db(self):
        session.add(self)
        session.commit()

    def add(self):
        session.add(self)

    @classmethod
    def commit(cls):
        session.commit()


#creates the database if it does not exist
Base.metadata.create_all(engine)
