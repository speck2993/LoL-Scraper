import config

key = config.api_key

#order KR, NA1, EUW1
indices = {"KR": 0, "NA": 1, "EUW": 2}

challenger_league = ["https://kr.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5",
                     "https://na1.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5",
                     "https://euw1.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5"]

gm_league = ["https://kr.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5",
             "https://na1.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5",
             "https://euw1.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5"]

puuID_from_sID = ["https://kr.api.riotgames.com/lol/summoner/v4/summoners/",
                  "https://na1.api.riotgames.com/lol/summoner/v4/summoners/",
                  "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/"]

matchIDs_from_puuID = ["https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/",
                      "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/",
                      "https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/"]

match_from_matchID = ["https://asia.api.riotgames.com/lol/match/v5/matches/",
                        "https://americas.api.riotgames.com/lol/match/v5/matches/",
                        "https://europe.api.riotgames.com/lol/match/v5/matches/"]

def pro_url(region,season):
    return "https://lol.fandom.com/wiki/" + str(region) + "/" + str(season) + "_Season/"

def challenger_url(region):
    return challenger_league[indices[region]] + "/?api_key=" + key

def gm_url(region):
    return gm_league[indices[region]] + "/?api_key=" + key

def puuID_from_sID_url(region,sID):
    return puuID_from_sID[indices[region]] + sID + "/?api_key=" + key

def matchIDs_from_puuID_url(region,puuID):
    return matchIDs_from_puuID[indices[region]] + puuID + "/ids?type=ranked&start=0&count=100&api_key=" + key

def match_from_matchID_url(region,matchID):
    return match_from_matchID[indices[region]] + matchID + "/?api_key=" + key
