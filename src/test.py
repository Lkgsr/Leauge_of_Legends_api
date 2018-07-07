from leauge_of_legends_api import Summoner, LeaugeOfLegendLeauger, ChampionMastery, Match, CompleteMatch, Item, Champion

header = ["RGAPI-5e68516c-82b4-4854-9727-23ca48845efb"]


def update_data_base(update_masterys=True, update_leauger=True, update_matches=True):
    counter = 0
    match_counter = 0
    for sum in Summoner.get_all():
        Summoner.insert_to_db_by_account_id(header, sum.account_id)
        if update_masterys:
            ChampionMastery.insert_to_db_by_summoner_id(header,sum.summoner_id)
        if update_leauger:
            LeaugeOfLegendLeauger.insert_to_db_by_summoner_id(header,sum.summoner_id)
        if update_matches:
            match = None
            for match in Match.insert_to_db_by_account_id(header, sum.account_id):
                if match:
                    match = CompleteMatch.insert_to_db_by_game_id(header, match.game_id)
                    if match:
                        match_counter += 1
            if match:
                match.commit()
        counter += 1
        if counter % 100 == 0:
            print("{} Summoners so far with and {} Matches".format(counter, match_counter))
            print("Current Summoner: {}".format(sum.name))


"""Insert You summoner name by 'Place Your Summoner Name' ! ! ! """

if __name__ == "__main__":
    #Summoner.insert_to_db_by_summoner_name(header, "I am not tilted") #Place Your Summoner Name
    #update_data_base(update_leauger=True, update_masterys=True)
    Item.insert_all_to_db(header)
    Champion.insert_all_champion_to_db(header)
