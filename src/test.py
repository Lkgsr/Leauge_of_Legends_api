from leauge_of_legends_api import Summoner, LeaugeOfLegendLeauger, ChampionMastery, Match, CompleteMatch,\
    Item, Champion, ParticipantIdentities
from datetime import datetime




def update_data_base(update_masterys=True, update_leauger=True, update_matches=True):
    counter = 0
    match_counter = 0
    for sum in Summoner.get_all():
        Summoner.insert_to_db_by_account_id(header, sum.account_id)
        if update_masterys:
            ChampionMastery.insert_to_db_by_summoner_id(header, sum.summoner_id, just_add=False)
        if update_leauger:
            LeaugeOfLegendLeauger.insert_to_db_by_summoner_id(header, sum.summoner_id)
        if update_matches:
            match = None
            for match in Match.insert_to_db_by_account_id(header, sum.account_id):
                if match:
                    match = CompleteMatch.insert_to_db_by_game_id(header, match.game_id)
                    if match is None:
                        print('No Complete Match')
                    if match:
                        match_counter += 1
            if match:
                match.commit()
                print('commit')
        counter += 1
        if counter % 100 == 0:
            print("{} Summoners so far with and {} Matches".format(counter, match_counter))
            print("Current Summoner: {}".format(sum.name))


def get_all_sums_from_matches():
    counter = 0
    for participantidentities in ParticipantIdentities.get_all_with_limit(17000):
        Summoner.insert_to_db_by_account_id(header, participantidentities.account_id, update_summoner=True)
        counter += 1
        if counter % 1000 == 0:
            print('sums done: {}, Time: {}'.format(str(counter), str(datetime.now())))


"""Insert You summoner name by 'Place Your Summoner Name' ! ! ! """

if __name__ == "__main__":
    #for name in "Tyler 1 Hype", "Osman Patron", "WachtlingerJohan", "WachtlingerPeter", "BierKong":
    #summoner = Summoner.insert_to_db_by_summoner_name(header, name) #Place Your Summoner Name
    get_all_sums_from_matches()
    #update_data_base(update_leauger=True, update_masterys=True)
    #print(len(summoner.matches.all()))
    #Item.insert_all_to_db(header)
    #Champion.insert_all_champion_to_db(header)
