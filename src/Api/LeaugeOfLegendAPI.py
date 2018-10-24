import requests
import time
from src.Api.LeaugeOfLegendObjects import Summoner
s = requests.Session()
counter = 0


def _check_response_header(header):
    """shuld check the rate limits"""
    if 'Retry-After' in header.keys():
        print('X-Rate-Limit-Type: ' + str(header['X-Rate-Limit-Type']))
        print('Next retry in :' + str(int(header['Retry-After']) + 3 ))
        Summoner.commit()
        time.sleep(int(header['Retry-After']))


def _intern_send_request(url, APIKey, region):
    """Just the request"""
    global counter
    #print(APIKey[counter])
    header = {"X-Riot-Token": str(APIKey[counter])}
    counter +=1
    if counter >= len(APIKey):
        counter = 0
    try:
        response = s.get("https://"+region+".api.riotgames.com"+url, headers=header)
    except Exception as e:
        print("request exception: " + str(e))
        return None
    return response


def _send_request(url, APIKey, region="euw1"):
    """sends the request to RiotsGames"""
    response = _intern_send_request(url, APIKey, region)
    if response is not None: # with only response: it didnt work by response code like 404 or 403 or 429
        if response.status_code == 403:
            print('Update you API-Key !, message: ' + str(response.json()))
            Summoner.commit()
            exit()
            return None
        while response.status_code == 429:
            _check_response_header(response.headers)
            response = _intern_send_request(url,APIKey, region)
        if response.status_code == 404:
            print(response.json())
            return None
        if response:
            if response.status_code == 200:        
                return response.json()
    return None


class LeaugeMasteries:
    """Champion mastery V3"""
    def __init__(self, APIKey):
        self.APIKey = APIKey

    def get_champion_masteries_by_summoner_id(self, summoner_id):
        """All champion Masterypoints by summoner ID"""
        return _send_request('/lol/champion-mastery/v3/champion-masteries/by-summoner/{}'.format(summoner_id), self.APIKey)

    def get_champion_mastery_by_summoner_id_and_champion_id(self, summoner_id, champion_id):
        """champion mastery pionts by summoner id and champion ID"""
        return _send_request('/lol/champion-mastery/v3/champion-masteries/by-summoner/{}/by-champion/{}'.format(summoner_id,champion_id), self.APIKey)

    def get_summoner_mastery_score_by_summoner_id(self, summoner_id):
        """champion Mastery Score by Summoner ID"""
        return _send_request('/lol/champion-mastery/v3/scores/by-summoner/{}'.format(summoner_id), self.APIKeys)


class LeaugeChampions:
    """Champions"""
    def __init__(self, APIKeys):
        self.APIKey = APIKeys

    def get_all_champions(self):
        """All Champions"""
        return _send_request('/lol/platform/v3/champions?freeToPlay=false', self.APIKey)

    def get_champion_by_id(self, champion_id):
        """Get Champion by Champion ID"""
        return _send_request('/lol/platform/v3/champions/{}'.format(champion_id), self.APIKey)


class LeaugeLeauge:
    """Leauge"""
    def __init__(self, APIKeys):
        self.APIKey = APIKeys

    def get_leauge_by_queue(self, queue):
        """Get Leauge by queue"""
        return _send_request('/lol/league/v3/challengerleagues/by-queue/{}'.format(queue), self.APIKey)
    
    def get_leauges_by_leauge_id(self, leauge_id):
        """Get Leauges by Leauges ID"""
        return _send_request('/lol/league/v3/leagues/{}'.format(leauge_id),self.APIKey)

    def get_master_leauges_by_queue(self, queue):
        """Get Master Leauges by queue"""
        return _send_request('/lol/league/v3/masterleagues/by-queue/{}'.format(queue),self.APIKey)

    def get_leauge_positions_by_summoner_id(self, summoner_id):
        """Get Leauge positions by summoner ID"""
        return _send_request('/lol/league/v3/positions/by-summoner/{}'.format(summoner_id),self.APIKey)


class LeaugeStatics:
    """Leauge Static Data"""
    def __init__(self, APIKeys):
        self.APIKey = APIKeys

    def get_all_champions_static(self):
        """All Champions"""
        return _send_request('/lol/static-data/v3/champions',self.APIKey)

    def get_champion_by_id_static(self, champion_id):
        """Champion by ID"""
        return _send_request('/lol/static-data/v3/champions/{}'.format(champion_id),self.APIKey)

    def get_all_items_static(self):
        """All Items"""
        return requests.get('http://ddragon.leagueoflegends.com/cdn/6.24.1/data/de_DE/item.json').json()

    def get_item_by_id_static(self, item_id):
        """Item by ID"""
        return _send_request('/lol/static-data/v3/items/{}'.format(item_id),self.APIKey)

    def get_languages_string_static(self):
        """Languages-Strings"""
        return _send_request('/lol/static-data/v3/language-strings',self.APIKey)

    def get_languages_static(self):
        """Languages"""
        return _send_request('/lol/static-data/v3/languages',self.APIKey)

    def get_all_maps_static(self):
        """Maps"""
        return _send_request('/lol/static-data/v3/maps',self.APIKey)

    def get_alls_masteries_static(self):
        """Masteries"""
        return _send_request('/lol/static-data/v3/masteries',self.APIKey)

    def get_mastery_by_id_static(self, mastery_id):
        """Mastery by ID"""
        return _send_request('/lol/static-data/v3/masteries/{}'.format(mastery_id),self.APIKey)

    def get_all_profile_icons_static(self):
        """Profileicons"""
        return _send_request('/lol/static-data/v3/profile-icons',self.APIKey)
        
    def get_realms_static(self):
        """Realms"""
        return _send_request('/lol/static-data/v3/realms',self.APIKey)

    def get_reforged_rune_paths_static(self):
        """Reforged Rune Paths"""
        return _send_request('/lol/static-data/v3/reforged-rune-paths',self.APIKey)

    def get_reforged_rune_paths_by_id_static(self, rune_path_id):
        """Reforged Rune Paths by ID"""
        return _send_request('/lol/static-data/v3/reforged-rune-paths/{}'.format(rune_path_id),self.APIKey)

    def get_all_reforged_runes_static(self):
        """Reforged Runes"""
        return _send_request('/lol/static-data/v3/reforged-runes',self.APIKey)

    def get_all_reforged_runes_static_by_id(self, reforged_runes_id):
        """Reforged Runes by ID"""
        return _send_request('/lol/static-data/v3/reforged-runes/{}'.format(reforged_runes_id),self.APIKey)

    def get_all_runes_static(self):
        """Runes"""
        return _send_request('/lol/static-data/v3/runes',self.APIKey)

    def get_rune_by_id_static(self, rune_id):
        """Runes by ID"""
        return _send_request('/lol/static-data/v3/runes/{}'.format(rune_id),self.APIKey)

    def get_all_summoner_spelles_static(self):
        """Summoner Spelles"""
        return _send_request('/lol/static-data/v3/summoner-splles',self.APIKey)

    def get_summoner_spelle_by_id_static(self, spelle_id):
        """Summoner Spelles by ID"""
        return _send_request('/lol/static-data/v3/summoner-splles/{}'.format(spelle_id),self.APIKey)

    def get_tarball_links_static(self):
        """Tarball Links"""
        return _send_request('/lol/static-data/v3/tarball-links', self.APIKey)

    def get_versions_static(self):
        """Versions"""
        return _send_request('/lol/static-data/v3/versions', self.APIKey)


class LeaugeStatus:
    """Leauge of Legends Status"""
    def __init__(self, APIKeys):
        self.APIKey = APIKeys

    def get_all_leauge_server_status(self):
        """shared data"""
        return _send_request('/lol/status/v3/shard-data',self.APIKey)


class LeaugeMatches:
    """Matches"""
    def __init__(self, APIKeys):
        self.APIKey = APIKeys

    def get_match_by_id(self, match_id):
        """Get Match by match ID"""
        return _send_request('/lol/match/v3/matches/{}'.format(match_id),self.APIKey)

    def get_matchlist_by_id(self, account_id):
        """Get matchlist for games played on given account Id and platform Id and filtered using filter parameters"""
        return _send_request('/lol/match/v3/matchlists/by-account/{}'.format(account_id),self.APIKey)

    def get_matchlist_for_last_20_games_by_id(self, account_id):
        """Get matchlist for last 20 matches played on given account Id and platform ID"""
        return _send_request('/lol/match/v3/matchlists/by-account/{}/recent'.format(account_id),self.APIKey)

    def get_match_timelines_by_id(self, match_id):
        """Get match Ids by timeline by match ID"""
        return _send_request('/lol/match/v3/timelines/by-match/{}'.format(match_id),self.APIKey)

    def get_match_timelines_by_tournament_code(self, tournament_code):
        """Get match Ids by tournament code"""
        return _send_request('/lol/match/v3/matches/by-tournament-code/{}/ids'.format(tournament_code),self.APIKey)

    def get_match_by_id_and_tournament_code(self, tournament_code,match_id):
        """Get match by match Id and tournament code"""
        return _send_request('/lol/match/v3/matches/{}/by-tournament-code/{}'.format(match_id, tournament_code),self.APIKey)


class LeaugeSpectator:
    """Spectator"""
    def __init__(self, APIKeys):
        self.APIKey = APIKeys

    def get_active_game_by_id(self, summoner_id):
        """Get current game inforamtion for the given summoner ID"""
        return _send_request('/lol/spectator/v3/active-games/by-summoner/{}'.format(summoner_id),self.APIKey)

    def get_list_of_active_featured_games(self):
        """Get list of featured games"""
        return _send_request('/lol/spectator/v3/featured-games',self.APIKey)


class LeaugeSummoner:
    """Summoner"""
    def __init__(self, APIKeys):
        self.APIKey = APIKeys

    def get_summoner_by_account_id(self, account_id):
        """Get a summoner by account ID"""
        return _send_request('/lol/summoner/v3/summoners/by-account/{}'.format(account_id),self.APIKey)

    def get_summoner_by_name(self, summoner_name):
        """Get summoner by summoner name"""
        return _send_request('/lol/summoner/v3/summoners/by-name/{}'.format(summoner_name),self.APIKey)

    def get_summoner_by_id(self, summoner_id):
        """#Get summoner by summoner ID"""
        return _send_request('/lol/summoner/v3/summoners/{}'.format(summoner_id),self.APIKey)


class LeaugeThirdPartyCode:
    """Third party code"""
    def __init__(self, APIKeys):
        self.APIKey = APIKeys

    def get_third_party_code_by_id(self, summoner_id):
        """Get third party code for given summoner Id"""
        return _send_request('/lol/platform/v3/third-party-code/by-summoner/{}'.format(summoner_id),self.APIKey)


class LeaugeTournament:
    """Tournament Stub"""
    def __init__(self, APIKeys):
        self.APIKey = APIKeys

    def post_create_tournament_stub_code(self):
        """Create a mock tournament code for the given tournament"""
        return _send_request('/lol/tournament-stub/v3/codes',self.APIKey)

    def get_mocklist_lobby_events_by_code(self, tournament_code):
        """Gets a mock list of lobby events by tournament code"""
        return _send_request('/lol/tournament-stub/v3/lobby-events/by-code/{}'.format(tournament_code),self.APIKey)

    def get_creates_mock_tournament_provider(self):
        """#Creates a mock tournament provider and return ID"""
        return _send_request('/lol/tournament-stub/v3/providers',self.APIKey)

    def get_creates_mock_tournament(self):
        """Creates a mock tournament and returns its ID"""
        return _send_request('/lol/tournament-stub/v3/tournaments',self.APIKey)