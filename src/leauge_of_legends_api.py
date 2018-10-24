from Api.LeaugeOfLegendAPI import LeaugeSummoner, LeaugeLeauge, LeaugeMasteries, LeaugeMatches, LeaugeStatics
from Api.LeaugeOfLegendObjects import Summoner as ObSum, LeaugeRankedSolo5x5 as RANKED_SOLO_5x5,\
    LeaugeRankedFlexSR as RANKED_FLEX_SR, LeaugeRankedFlexTT as RANKED_FLEX_TT, ChampionMastery as ObMastery,\
    Matches, Champions, BigMatch, Participants, ParticipantIdentities, Stats, CsDiffPerMinDeltas, GoldPerMinDeltas,\
    XpDiffPerMinDeltas, CreepsPerMinDeltas, XpPerMinDeltas, DamageTakenDiffPerMinDeltas, DamageTakenPerMinDeltas,\
    Timeline, Team, Bans, Item as itemobj
import time


class Summoner:
    """ Inserte and update summoners in the DB by summonerName or accountId or summonerId"""

    def _handel(summoner, parameter):
        """Checks if the summoner exists and creats a Summoner Object which get returned """
        if summoner is None:
            print('No summoner with the name/accountId/summonerId {}'.format(parameter))
            return None
        if 'status' in summoner.keys():
            print(summoner)
            return None
        return ObSum(**summoner)

    def _update(summoner, header):
        """Updates the summoner by his account ID and return the updatet summoner Object"""
        updated_sum = LeaugeSummoner(header).get_summoner_by_account_id(summoner.account_id)
        if updated_sum is None:
            return None
        if 'status' in updated_sum.keys():
            return updated_sum
        updated_sum = ObSum(**updated_sum)
        summoner.account_id = updated_sum.account_id
        summoner.name = updated_sum.name
        summoner.profile_icon_id = updated_sum.profile_icon_id
        summoner.revision_date = updated_sum.revision_date
        summoner.summoner_id = updated_sum.summoner_id
        summoner.summoner_level = updated_sum.summoner_level
        return summoner

    @classmethod
    def insert_to_db_by_summoner_name(cls, header, summoner_name, update_summoner=True, just_add=False):
        """Inserting a summoner by his name or if he allready exists he get updated if update_summoner is True and returns the summoner"""
        sumer = ObSum.find_by_name(summoner_name)
        if sumer is None:
            sumer = cls._handel(LeaugeSummoner(header).get_summoner_by_name(summoner_name), summoner_name)
            if sumer:
                if just_add:
                    sumer.add()
                else:
                    sumer.insert_to_db()
        else:
            if update_summoner:
                sumer = cls._update(sumer, header)
                if sumer:
                    if just_add:
                        sumer.add()
                    else:
                        sumer.insert_to_db()
        return sumer

    @classmethod
    def insert_to_db_by_account_id(cls, header,account_id, update_summoner=True, just_add=False):
        """Inserting a summoner by his accountId or if he allready exists he get updated if update_summoner is True and returns the summoner"""
        sumer = ObSum.find_by_account_id(account_id)
        if sumer is None:
            sumer = cls._handel(LeaugeSummoner(header).get_summoner_by_account_id(account_id), account_id)
            if sumer:
                if just_add:
                    sumer.add()
                else:
                    sumer.insert_to_db()
        else:
            if update_summoner:
                sumer = cls._update(sumer, header)
                if sumer:
                    if just_add:
                        sumer.add()
                    else:
                        sumer.insert_to_db()
        return sumer

    @classmethod
    def insert_to_db_by_summoner_id(cls, header, summoner_id, update_summoner=True, just_add=False):
        """Inserting a summoner by his summonerId or if he allready exists he get updated if update_summoner is True and returns the summoner"""
        sumer = ObSum.find_by_summoner_id(summoner_id)
        if sumer is None:
            sumer = cls._handel(LeaugeSummoner(header).get_summoner_by_id(summoner_id), summoner_id)
            if sumer:
                if just_add:
                    sumer.add()
                else:
                    sumer.insert_to_db()
        else:
            if update_summoner:
                sumer = cls._update(sumer, header)
                if sumer:
                    if just_add:
                        sumer.add()
                    else:
                        sumer.insert_to_db()
        return sumer

    @classmethod
    def update_all_in_db(cls, header):
        """updates all Summoners in your DB and returns every one like a Generator"""
        for summoner in cls.get_all():
            yield cls.insert_to_db_by_account_id(header, summoner.account_id)

    @classmethod
    def get_all(cls):
        """returns all the summoner from the Database as a List"""
        return ObSum.get_all_summoners()

    @classmethod
    def find_by_name(cls, summoner_name):
        return ObSum.find_by_name(summoner_name)

    @classmethod
    def find_by_account_id(cls, account_id):
        return ObSum.find_by_account_id(account_id)

    @classmethod
    def find_by_summoner_id(cls, summoner_id):
        return ObSum.find_by_summoner_id(summoner_id)

    @classmethod
    def commit(cls):
        ObSum.commit()


class LeaugeOfLegendLeauger:
    """update and inserting the leaugs """

    def _create_leauge_for_db(leauger, queue_type):
        """creats the right leauger object from the leauges list and returns it"""
        for leauge in leauger:
            if leauge['queueType']== queue_type:
                leauge.pop('miniSeries', None)
                return eval(queue_type+'(**leauge)')
        return None


    
    def _update_leauge_in_db(old_leauge, new_leauge):
        """updates the given leaug object with a newer one and return the updated obj"""
        old_leauge.fresh_blood = new_leauge.fresh_blood
        old_leauge.hot_streak = new_leauge.hot_streak
        old_leauge.inactive = new_leauge.inactive
        old_leauge.leauge_id = new_leauge.leauge_id
        old_leauge.leauge_name = new_leauge.leauge_name
        old_leauge.leauge_points = new_leauge.leauge_points
        old_leauge.losses = new_leauge.losses
        old_leauge.player_or_team_id = new_leauge.player_or_team_id
        old_leauge.player_or_team_name = new_leauge.player_or_team_name
        old_leauge.queue_type = new_leauge.queue_type
        old_leauge.rank = new_leauge.rank
        old_leauge.tier = new_leauge.tier
        old_leauge.veteran = new_leauge.veteran
        old_leauge.wins = new_leauge.wins
        return old_leauge
    
        
    @classmethod
    def insert_to_db_by_summoner_id(cls, header, summoner_id, just_add=True):
        """Inserts or if it not exists in the Database all Leaugers of a summoner by his summonerId and return a tuple with
        all 3 leaugers if there is no leager it returns a None in the tuple"""
        leaugers = LeaugeLeauge(header).get_leauge_positions_by_summoner_id(summoner_id)
        if leaugers is None:
            print('There are no Leagers for the given summonerId {}'.format(summoner_id))
            return None
        if type(leaugers) is dict:
            if 'status' in leaugers.keys():
                print(leaugers)
                return None
        solo5x5 = RANKED_SOLO_5x5.find_by_summoner_id(summoner_id)
        if solo5x5 is None:
            solo5x5 = cls._create_leauge_for_db(leaugers,'RANKED_SOLO_5x5')
            if solo5x5 is not None:
                if just_add:
                    solo5x5.add()
                else:
                    solo5x5.insert_to_db()
            else:
                pass #print('No RANKED_SOLO_5x5 for the summonerId {}'.format(summoner_id))
        else:
            solo5x5 = cls._update_leauge_in_db(solo5x5, cls._create_leauge_for_db(leaugers, 'RANKED_SOLO_5x5'))
            if just_add:
                solo5x5.add()
            else:
                solo5x5.insert_to_db()
        
        flexSR = RANKED_FLEX_SR.find_by_summoner_id(summoner_id)
        if flexSR is None:
            flexSR = cls._create_leauge_for_db(leaugers, 'RANKED_FLEX_SR')
            if flexSR is not None:
                if just_add:
                    flexSR.add()
                else:
                    flexSR.insert_to_db()
            else:
                pass #print('No RANKED_FLEX_SR for the summonerId {}'.format(summoner_id))
        else:
            flexSR = cls._update_leauge_in_db(flexSR, cls._create_leauge_for_db(leaugers, 'RANKED_FLEX_SR'))
            if just_add:
                flexSR.add()
            else:
                flexSR.insert_to_db()

        TT3v3 = RANKED_FLEX_TT.find_by_summoner_id(summoner_id)
        if TT3v3 is None:
            TT3v3 = cls._create_leauge_for_db(leaugers, 'RANKED_FLEX_TT')
            if TT3v3 is not None:
                if just_add:
                    TT3v3.add()
                else:
                    TT3v3.insert_to_db()
            else:
                pass #print('No RANKED_FLEX_TT for the summonerId {}'.format(summoner_id))
        else:
            TT3v3 = cls._update_leauge_in_db(TT3v3, cls._create_leauge_for_db(leaugers, 'RANKED_FLEX_TT'))
            if just_add:
                TT3v3.add()
            else:
                TT3v3.insert_to_db()
        return (solo5x5, flexSR, TT3v3)

    @classmethod
    def get_all_solo5x5(cls):
        return RANKED_SOLO_5x5.get_all()

    @classmethod
    def get_all_flexSR(cls):
        return RANKED_FLEX_SR.get_all()

    @classmethod
    def get_all_TT3v3(cls):
        return RANKED_FLEX_TT.get_all()

    @classmethod
    def find_solo5x5_by_summoner_id(cls, summoner_id):
        """returns The Solo and Duo Queue Leauge Object"""
        return RANKED_SOLO_5x5.find_by_summoner_id(summoner_id)

    @classmethod
    def find_flexSR_by_summoner_id(cls, summoner_id):
        """returns The Flex Queue Leauge Object"""
        return RANKED_FLEX_SR.find_by_summoner_id(summoner_id)

    @classmethod
    def find_TT3v3_by_summoner_id(cls, summoner_id):
        """returns The TwistedTreeline Queue Leauge Object"""
        return RANKED_FLEX_TT.find_by_summoner_id(summoner_id)

    @classmethod
    def find_solo5x5_by_leauge_id(cls, leauge_id):
        return RANKED_SOLO_5x5.find_by_leauge_id(leauge_id)

    @classmethod
    def find_flexSR_by_leauge_id(cls, leauge_id):
        return RANKED_FLEX_SR.find_by_leauge_id(leauge_id)

    @classmethod
    def find_TT3v3_by_leauge_id(cls, leauge_id):
        return RANKED_FLEX_TT.find_by_leauge_id(leauge_id)


class ChampionMastery:
    """inserting and updating the MasteryPoints"""
    @classmethod
    def _handler(cls, masteries, just_add):
        """handles the champion mastery"""
        masteres_obj = []
        for mastery in masteries:
            mastery = ObMastery(**mastery)
            masteres_obj.append(mastery)
            oldmas = ObMastery.find_by_summoner_and_champion_id(mastery.player_id, mastery.champion_id)
            if oldmas is None:
                if just_add:
                    mastery.add()
                else:
                    mastery.commit()
            else:
                oldmas = cls._update(oldmas, mastery)
                if just_add:
                    oldmas.add()
                else:
                    oldmas.commit()
        return masteres_obj

    
    def _update(old, new):
        """updates the given champion mastery object with a new one"""
        old.chest_granted = new.chest_granted
        old.champion_level = new.champion_level
        old.champion_points = new.champion_points
        old.champion_id = new.champion_id
        old.player_id = new.player_id
        old.champion_points_until_next_level = new.champion_points_until_next_level
        old.tokens_earned = new.tokens_earned
        old.champion_points_until_next_level = new.champion_points_until_next_level
        old.last_play_time = new.last_play_time
        return old

    @classmethod
    def insert_to_db_by_summoner_id(cls, header, summoner_id, just_add=True):
        """Insert or updates if the mastery all ready exists to the Database"""
        masteries = LeaugeMasteries(header).get_champion_masteries_by_summoner_id(summoner_id)
        if masteries is None:
            print('No Masteries for the given summonerId {}'.format(summoner_id))
            return None
        if type(masteries) is not list:
            if 'status' in masteries.keys():
                print(masteries)
                return None
        if masteries:
            masteries = cls._handler(masteries, just_add)
        return masteries

    @classmethod
    def get_all(cls):
        return ObMastery.get_all()

    @classmethod
    def find_all_by_champion_id(cls, champion_id):
        return ObMastery.find_by_champion_id(champion_id)

    @classmethod
    def find_by_summoner_and_champion_id(cls, summoner_id, champion_id):
        return ObMastery.find_by_summoner_and_champion_id(summoner_id, champion_id)

    @classmethod
    def find_all_by_summoner_id(cls, summoner_id):
        return ObMastery.find_by_player_id(summoner_id)


class Match:
    """Inserting and updating the small match"""

    @classmethod
    def insert_to_db_by_account_id(cls, header, account_id, just_add=True):
        """Insert all match to the Database and Ignores the matches that are all ready saved, returns all new inserted matches as a Generator"""
        response = LeaugeMatches(header).get_matchlist_by_id(account_id)
        if response is None:
            print('No Matches for the given AccountId {}'.format(account_id))
            return None
        if 'status' in response.keys():
            print(response)
            return None
        if 'matches' in response.keys():
            matches = response['matches']
            if matches is None:
                print(response)
                return None
            for match in matches:
                if Matches.find_by_id(int(str(account_id)+ str(match['gameId']))):
                    return None
                match['playerId'] = account_id
                if "role" not in match.keys():
                    match['role'] = ''
                if "lane" not in match.keys():
                    match['lane'] = ''
                match = Matches(**match)
                if just_add:
                    match.add()
                else:
                    match.insert_to_db()
                yield match

    @classmethod
    def get_all(cls):
        """Returns all matches from the Database as a List"""
        return Matches.get_all_matches()

    @classmethod
    def get_all_by_player_id(cls, account_id):
        """Returns all matches from a player as a List"""
        return Matches.find_all_by_id(account_id)

    @classmethod
    def find_by_id(cls, _id):
        """Returns one match by his id = account_id+game_id"""
        return Matches.find_by_id(_id)


class Champion:
    """Inserting and Updating the Champions"""

    def _update(old, new):
        """updates and old champion obf with a newer one"""
        old.id = new.id
        old.key = new.key
        old.name = new.name
        old.title = new.title

    @classmethod
    def insert_all_champion_to_db(cls, header):
        """Inserts or updates all Champions to the Database"""
        champions = LeaugeStatics(header).get_all_champions_static()
        if champions is None:
            print("There ar no champions found may here is a problem with you APIkey")
            return None
        if 'status' in champions.keys():
            print(champions)
            return None
        champions = champions['data']
        for champ in champions.values():
            newChamp = Champions(**champ)
            oldChamp = Champions.find_champion_by_id(newChamp.id)
            if oldChamp:
                cls._update(oldChamp, newChamp)
                oldChamp.insert_to_db()
            else:
                newChamp.insert_to_db()

    @classmethod
    def get_all(cls):
        return Champions.get_all()

    @classmethod
    def find_by_id(cls, champion_id):
        return Champions.find_by_id(champion_id)

    @classmethod
    def find_by_name(cls, name):
        return Champions.find_by_name(name)


class CompleteMatch:
    """updating and inserting the compled match with everything"""


    def _timeline_things(timeliething):
        """Just needt for intern handling of the timline  """
        dicts = {
            'eins': None,
            'zwei': None,
            'drei': None,
            'vier': None,
            'fünf': None,
            'sechs': None,
            'sieben': None,
            'acht': None,
            'neun': None,
            'zehn': None
            }
        for key in timeliething.keys():
            switcher = {
                '0-10': {'eins': timeliething[key]},
                '0-end':{'eins': timeliething[key]},
                '10-20':{'zwei': timeliething[key]},
                '10-end':{'zwei': timeliething[key]},
                '20-30':{'drei': timeliething[key]},
                '20-end':{'drei': timeliething[key]},
                '30-40':{'vier': timeliething[key]},
                '30-end':{'vier': timeliething[key]},
                '40-50':{'fünf': timeliething[key]},
                '40-end':{'fünf': timeliething[key]},
                '50-60':{'sechs': timeliething[key]},
                '50-end':{'sechs': timeliething[key]},
                '60-70':{'sieben': timeliething[key]},
                '60-end':{'sieben': timeliething[key]},
                '70-80':{'acht': timeliething[key]},
                '70-end':{'acht': timeliething[key]},
                '80-90':{'neun': timeliething[key]},
                '80-end':{'neun': timeliething[key]},
                '90-100':{'zehn': timeliething[key]},
                '90-end':{'zehn': timeliething[key]}
                }
            dicts.update(switcher.get(key))
        return dicts


    def _participantIdentities(gameId,participantIdentities):
        """Goes through all the participantIdenteties and creat a the obj and returns all a a Generator"""
        ppireturn = []
        for raw_participant_identety in participantIdentities:
            if 'player' not in raw_participant_identety.keys():
                print('no player in participantsIdentety')
                return None
            player = raw_participant_identety['player']
            player['participantId'] = raw_participant_identety['participantId']
            player['gameId'] = gameId
            if "summonerId" not in player.keys():
                print('No summonerId in response')
                return None
            if "gameId" not in player.keys():
                print('no gameID')
                return None
            if "participantId" not in player.keys():
                print('no ID')
                return None
            #if not ParticipantIdentities.find_by_id(int(str(gameId) + str(player['participantId']))):
            yield (ParticipantIdentities(**player))


    @classmethod
    def _team(cls, teams, gameId):
        for team in teams:
            team['gameId'] = gameId
            bans = team.pop("bans")
            if "firstRiftHerald" not in team.keys():
                #print("No rift harald")
                return None
            if "riftHeraldKills" not in team.keys():
                #print("No hearaldkills")
                return None
            if "win" not in team.keys():
                #print("No win condtion")
                return None
            team = Team(**team)
            if bans:
                ban = cls._bans(bans,gameId, team.team_id)
                ban.add()
            yield team

    def _bans(bans, gameId, team_id):
        new_ban = {
            'championId1': None,
            'championId2': None,
            'championId3': None,
            'championId4': None,
            'championId5': None, }
        for ban in bans:
            key = ban['pickTurn']
            switcher = {
                1: {'championId1': ban['championId']},
                2: {'championId2': ban['championId']},
                3: {'championId3': ban['championId']},
                4: {'championId4': ban['championId']},
                5: {'championId5': ban['championId']},
                6: {'championId1': ban['championId']},
                7: {'championId2': ban['championId']},
                8: {'championId3': ban['championId']},
                9: {'championId4': ban['championId']},
                10: {'championId5': ban['championId']}
            }
            new_ban.update(switcher.get(key))
        new_ban['gameId'] = gameId
        new_ban['teamId'] = team_id
        return Bans(**new_ban)

    @classmethod
    def _timeline_and_deltas(cls,timeline, gameId, participantId):
        if 'goldPerMinDeltas' in timeline.keys():
            goldPerMinDeltas = timeline.pop("goldPerMinDeltas")
            goldPerMinDeltas = cls._timeline_things(goldPerMinDeltas)
            goldPerMinDeltas['participantId'] = participantId
            goldPerMinDeltas['gameId'] = gameId
            goldPerMinDeltas = GoldPerMinDeltas(**goldPerMinDeltas)
            goldPerMinDeltas.add()

        if 'creepsPerMinDeltas' in timeline.keys():
            creepsPerMinDeltas = timeline.pop("creepsPerMinDeltas")
            creepsPerMinDeltas = cls._timeline_things(creepsPerMinDeltas)
            creepsPerMinDeltas['participantId'] = participantId
            creepsPerMinDeltas['gameId'] = gameId
            creepsPerMinDeltas = CreepsPerMinDeltas(**creepsPerMinDeltas)
            creepsPerMinDeltas.add()

        if 'xpPerMinDeltas' in timeline.keys():
            xpPerMinDeltas = timeline.pop("xpPerMinDeltas")
            xpPerMinDeltas = cls._timeline_things(xpPerMinDeltas)
            xpPerMinDeltas['participantId'] = participantId
            xpPerMinDeltas['gameId'] = gameId
            xpPerMinDeltas = XpPerMinDeltas(**xpPerMinDeltas)
            xpPerMinDeltas.add()

        if 'damageTakenPerMinDeltas' in timeline.keys():
            damageTakenPerMinDeltas = timeline.pop("damageTakenPerMinDeltas")
            damageTakenPerMinDeltas = cls._timeline_things(damageTakenPerMinDeltas)
            damageTakenPerMinDeltas['participantId'] = participantId
            damageTakenPerMinDeltas['gameId'] = gameId
            damageTakenPerMinDeltas = DamageTakenPerMinDeltas(**damageTakenPerMinDeltas)
            damageTakenPerMinDeltas.add()

        if 'csDiffPerMinDeltas' in timeline.keys():
            csDiffPerMinDeltas = timeline.pop("csDiffPerMinDeltas")
            csDiffPerMinDeltas = cls._timeline_things(csDiffPerMinDeltas)
            csDiffPerMinDeltas['participantId'] = participantId
            csDiffPerMinDeltas['gameId'] = gameId
            csDiffPerMinDeltas = CsDiffPerMinDeltas(**csDiffPerMinDeltas)
            csDiffPerMinDeltas.add()

        if 'xpDiffPerMinDeltas' in timeline.keys():
            xpDiffPerMinDeltas = timeline.pop("xpDiffPerMinDeltas")
            xpDiffPerMinDeltas = cls._timeline_things(xpDiffPerMinDeltas)
            xpDiffPerMinDeltas['participantId'] = participantId
            xpDiffPerMinDeltas['gameId'] = gameId
            xpDiffPerMinDeltas = XpDiffPerMinDeltas(**xpDiffPerMinDeltas)
            xpDiffPerMinDeltas.add()

        if 'damageTakenDiffPerMinDeltas' in timeline.keys():
            damageTakenDiffPerMinDeltas = timeline.pop("damageTakenDiffPerMinDeltas")
            damageTakenDiffPerMinDeltas = cls._timeline_things(damageTakenDiffPerMinDeltas)
            damageTakenDiffPerMinDeltas['participantId'] = participantId
            damageTakenDiffPerMinDeltas['gameId'] = gameId
            damageTakenDiffPerMinDeltas = DamageTakenDiffPerMinDeltas(**damageTakenDiffPerMinDeltas)
            damageTakenDiffPerMinDeltas.add()

        timeline['gameId'] = gameId
        timeline = Timeline(**timeline)
        return timeline

    @classmethod
    def _participants(cls, participants, gameId):
        ppreturn = []
        for participant in participants:
            stats = participant.pop("stats")
            if stats is None:
                #print("No stats")
                return None
            if "timeline" not in participant.keys():
                return None
            timeline = participant.pop("timeline")
            if timeline is None:
                #print("No timeline")
                return None
            participant['gameId'] = gameId
            if "masteries" in participant.keys():
                #print("Old Masteries")
                return None
            if "runes" in participant.keys():
                #print("Old Runes")
                return None
            if "highestAchievedSeasonTier" not in participant.keys():
                participant['highestAchievedSeasonTier'] = None
            stats = cls._stats(stats, gameId)
            if stats is None:
                #print("No Stats")
                return None
            participant = Participants(**participant)
            timeline = cls._timeline_and_deltas(timeline, gameId, participant.participant_id)
            stats.add()
            timeline.add()
            yield participant

    def _stats(stats, gameId):
        stats['gameId'] = gameId
        if "neutralMinionsKilledTeamJungle" not in stats.keys():
            stats['neutralMinionsKilledTeamJungle'] = None
        if "wardsKilled" not in stats.keys():
            stats['wardsKilled'] = None
        if "neutralMinionsKilledEnemyJungle" not in stats.keys():
            stats['neutralMinionsKilledEnemyJungle'] = None
        if "wardsPlaced" not in stats.keys():
            stats['wardsPlaced'] = None
        if "firstInhibitorKill" not in stats.keys():
            stats['firstInhibitorKill'] = None
        if "firstInhibitorAssist" not in stats.keys():
            stats['firstInhibitorAssist'] = None
        try:
            stats = Stats(**stats)
        except Exception as e:
            print("Some Arrgumets are missing "+str(e))
            return None
        return stats
        '''if "neutralMinionsKilledTeamJungle" not in stats.keys():
            stats['neutralMinionsKilledTeamJungle'] = None
        if "wardsKilled" not in stats.keys():
            stats['wardsKilled'] = None
        if "neutralMinionsKilledEnemyJungle" not in stats.keys():
            stats['neutralMinionsKilledEnemyJungle'] = None
        if "wardsPlaced" not in stats.keys():
            stats['wardsPlaced'] = None
        if "firstInhibitorKill" not in stats.keys():
            stats['firstInhibitorKill'] = None
        if "firstInhibitorAssist" not in stats.keys():
            stats['firstInhibitorAssist'] = None
        if "firstBloodAssist" not in stats.keys():
            stats['firstBloodAssist'] = None
        if "firstBloodKill" not in stats.keys():
            stats['firstBloodKill'] = None
        if "firstTowerAssist" not in stats.keys():
            stats['firstTowerAssist'] = None
        if "firstTowerKill" not in stats.keys():
            stats['firstTowerKill'] = None
        if "perkSubStyle" not in stats.keys():
            stats['perkSubStyle'] = None
        if "perk1Var1" not in stats.keys():
            stats['perk1Var1'] = None
        if "perk1Var3" not in stats.keys():
            stats['perk1Var3'] = None
        if "perk1Var2" not in stats.keys():
            stats['perk1Var2'] = None
        if "perk5" not in stats.keys():
            stats['perk5'] = None
        if "perk4" not in stats.keys():
            stats['perk4'] = None
        if "perk5Var1" not in stats.keys():
            stats['perk5Var1'] = None
        if "perk5Var3" not in stats.keys():
            stats['perk5Var3'] = None
        if "perk5Var2" not in stats.keys():
            stats['perk5Var2'] = None
        if "perk2Var2" not in stats.keys():
            stats['perk2Var2'] = None
        if "perk2Var3" not in stats.keys():
            stats['perk2Var3'] = None
        if "perk2Var1" not in stats.keys():
            stats['perk2Var1'] = None
        if "perk4Var1" not in stats.keys():
            stats['perk4Var1'] = None
        if "perk4Var3" not in stats.keys():
            stats['perk4Var3'] = None
        if "perk1" not in stats.keys():
            stats['perk1'] = None
        if "perk0" not in stats.keys():
            stats['perk0'] = None
        if "perk3" not in stats.keys():
            stats['perk3'] = None
        if "perk2" not in stats.keys():
            stats['perk2'] = None
        if "perk3Var3" not in stats.keys():
            stats['perk3Var3'] = None
        if "perk3Var2" not in stats.keys():
            stats['perk3Var2'] = None
        if "perk3Var1" not in stats.keys():
            stats['perk3Var1'] = None
        if "perk0Var2" not in stats.keys():
            stats['perk0Var2'] = None
        if "perk4Var2" not in stats.keys():
            stats['perk4Var2'] = None
        if "perkPrimaryStyle" not in stats.keys():
            stats['perkPrimaryStyle'] = None
        if "perk0Var1" not in stats.keys():
            stats['perk0Var1'] = None
        if "perk0Var3" not in stats.keys():
            stats['perk0Var3'] = None
        if "turretKills" not in stats.keys():
            stats['turretKills'] = None
        if "inhibitorKills" not in stats.keys():
            stats['inhibitorKills'] = None'''

    @classmethod
    def insert_to_db_by_game_id(cls, header, game_id):
        if BigMatch.find_by_id(game_id):
            #print('Match allread exists')
            return None
        response = LeaugeMatches(header).get_match_by_id(game_id)
        if response is None:
            #print('No match for the given gameId {}'.format(game_id))
            return None
        if "status" in response.keys():
            print(response)
            return None
        teams = response.pop('teams')
        if teams is None:
            print('No teams')
            return None
        participants = response.pop('participants')
        if participants is None:
            print('No participans')
            return None
        ppidenteties = response.pop("participantIdentities")
        if ppidenteties is None:
            print('No participansIdenteties')
            return None
        match = BigMatch(**response)
        gameId = match.game_id
        #print(f'{len(participantIdenteties)}=={len(participants)}')
        for participantsIdentity, participant in zip(cls._participantIdentities(gameId, ppidenteties), cls._participants(participants, gameId)):
            if participantsIdentity and participant:
                #print(f'{participantsIdentity.key_for_stats}=={participant.id}')
                participantsIdentity.add()
                participant.add()
            else:
                print('Fail')
                return None
        for team in cls._team(teams, gameId):
            if team:
                team.add()
            else:
                print("something is missing by teams")
                return None
        #for participant in cls._participants(participants, gameId):
        #    if participant:
        #        participant.add()
        #    else:
        #        #print("something is missing by participants")
        #        return None
        match.add()
        #match.commit()
        return match

    @classmethod
    def add_all_big_matches(cls,header, ids):
        if ids:
            for _id in ids:
                starttimr = time.time()
                cls.insert_to_db_by_game_id(header, _id)
                starttimr = time.time() - starttimr
                print(starttimr)

    @classmethod
    def get_all(cls):
        return BigMatch.get_all()

    @classmethod
    def find_by_id(cls, game_id):
        return BigMatch.find_by_id(game_id)

    @classmethod
    def get_complete_match_by_game_id(cls, game_id):
        """Not ready"""
        match = []
        match.append(BigMatch.find_by_id(game_id))
        """Comming Soon"""


class Item:
    @classmethod
    def insert_all_to_db(cls, header):
        response = LeaugeStatics(header).get_all_items_static()
        items = response['data']
        for i, item in items.items():
            olditem = itemobj.find_by_id(i)
            if olditem:
                olditem.name = item['name']
                if 'description' in item.keys():
                    olditem.description = item['description']
                olditem.id = i
                if 'plaintext' in item.keys():
                    olditem.plaintext = item['plaintext']
                olditem.insert_to_db()
            else:
                del item['colloq']
                del item['into']
                del item['image']
                del item['gold']
                del item['tags']
                del item['maps']
                del item['stats']
                if 'from' in item.keys():
                    del item['from']
                if 'depth' in item.keys():
                    del item['depth']
                if 'effect' in item.keys():
                    del item['effect']
                if 'hideFromAll' in item.keys():
                    del item['hideFromAll']
                if 'consumed' in item.keys():
                    del item['consumed']
                if 'stacks' in item.keys():
                    del item['stacks']
                if 'inStore' in item.keys():
                    del item['inStore']
                if 'consumeOnFull' in item.keys():
                    del item['consumeOnFull']
                if 'specialRecipe' in item.keys():
                    del item['specialRecipe']
                if 'requiredChampion' in item.keys():
                    del item['requiredChampion']
                item['id'] = i
                item = itemobj(**item)
                item.insert_to_db()

    @classmethod
    def get_all(cls):
        return itemobj.get_all()

    @classmethod
    def find_by_id(cls, item_id):
        return itemobj.find_by_id(item_id)

    @classmethod
    def find_by_name(cls, name):
        return itemobj.find_by_name(name)