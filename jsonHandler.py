from champDict import idToName, keyDict, nameList

weights = {"KR": 3, "EU": 2, "NA": 2}
posOrder = {"TOP":0,"JUNGLE":1,"MIDDLE":2,"BOTTOM":3,"UTILITY":4}

def getPlayers(leagueJson):
    jsonPlayers = leagueJson['entries']
    IDs = []
    for i in jsonPlayers:
        IDs.append(i['summonerId'])
    return IDs

def getPuuID(playerJson):
    return playerJson['puuid']

def getMatchIDs(matchesJson):
    return matchesJson

def getMatch(matchJson):
    try:
        game_time = matchJson['info']['gameDuration']
        if game_time < 900:
            print("Game too short, invalid")
            return [False]
        initial_data = [matchJson['metadata']['matchId'], weights[matchJson['metadata']['matchId'][0:2]], matchJson['info']['gameVersion'], matchJson['info']['teams'][0]['win']]
        order = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        participants = matchJson['info']['participants']
        for i in range(0,10):
            position = int(5*(participants[i]['teamId']/100 - 1) + posOrder[participants[i]['teamPosition']])
            order[position]=i
        champs = []
        ids = []
        stats = []
        for i in range(0,10):
            player = participants[order[i]]
            champs.append(idToName[str.lower(player['championName'])])
            ids.append(player['puuid'])
            playerStats = []
            time = float(player['timePlayed'])
            kills = player['kills']
            deaths = player['deaths']
            assists = player['assists']
            damageDealt = player['totalDamageDealtToChampions']
            damageTanked = player['totalDamageTaken']+player['damageSelfMitigated']
            gold = player['goldEarned']
            shield = player['totalDamageShieldedOnTeammates']
            heal = player['totalHealsOnTeammates']
            cs = player['totalMinionsKilled'] + player['neutralMinionsKilled']
            cc = player['timeCCingOthers']
            turretDamage = player['damageDealtToBuildings']
            vision = player['visionScore']
            factor = 60.0/time
            playerStats = [kills*factor, deaths*factor, assists*factor, damageDealt*factor, damageTanked*factor, gold*factor, heal*factor, shield*factor, cc*factor, turretDamage, cs*factor, vision*factor, damageDealt/(gold+1), damageTanked/(deaths+1)]                  
            stats.append(playerStats)
        stats[3][5] = stats[3][5] + stats[4][5]         ############################
        stats[3][10] = stats[3][10] + stats[4][10]      # Pooling ADC and Sup      #
        stats[4][5] = stats[3][5]                       # gold and CS stats        #
        stats[4][10] = stats[3][10]                     # to account for           #
        stats[8][5] = stats[8][5] + stats[9][5]         # items like Targon's      #
        stats[8][10] = stats[8][10] + stats[9][10]      # and duos like Senna/Tahm #
        stats[9][5] = stats[8][5]                       #                          #
        stats[9][10] = stats[8][10]                     ############################
        
            
        return [initial_data,champs,stats,ids]
    except:
        print("Error accessing players in game")
        return [False]
        
def getWikiMatch5(matchJson,weight):
    try:
        game_time = matchJson['gameDuration']
        if game_time < 900:
            print("Game too short, invalid")
            return [False]
        initial_data = ['ESPORTSTMNT02_' + str(matchJson['gameId']), weight, matchJson['gameVersion'], matchJson['teams'][0]['win']]
        champs = []
        ids = []
        stats = []
        participants = matchJson['participants']
        for i in range(0,10):
            player = participants[i]
            champs.append(idToName[str.lower(player['championName'])])
            ids.append(player['summonerName'])
            playerStats = []
            time = float(player['timePlayed'])
            kills = player['kills']
            deaths = player['deaths']
            assists = player['assists']
            damageDealt = player['totalDamageDealtToChampions']
            damageTanked = player['totalDamageTaken']+player['damageSelfMitigated']
            gold = player['goldEarned']
            shield = player['totalDamageShieldedOnTeammates']
            heal = player['totalHealsOnTeammates']
            cs = player['totalMinionsKilled'] + player['neutralMinionsKilled']
            cc = player['timeCCingOthers'] #cc stats are messed up for no reason :(
            turretDamage = player['damageDealtToBuildings']
            vision = player['visionScore']
            factor = 60.0/time
            playerStats = [kills*factor, deaths*factor, assists*factor, damageDealt*factor, damageTanked*factor, gold*factor, heal*factor, shield*factor, cc*factor, turretDamage, cs*factor, vision*factor, damageDealt/(gold+1), damageTanked/(deaths+1)]                  
            stats.append(playerStats)
        stats[3][5] = stats[3][5] + stats[4][5]         ############################
        stats[3][10] = stats[3][10] + stats[4][10]      # Pooling ADC and Sup      #
        stats[4][5] = stats[3][5]                       # gold and CS stats        #
        stats[4][10] = stats[3][10]                     # to account for           #
        stats[8][5] = stats[8][5] + stats[9][5]         # items like Targon's      #
        stats[8][10] = stats[8][10] + stats[9][10]      # and duos like Senna/Tahm #
        stats[9][5] = stats[8][5]                       #                          #
        stats[9][10] = stats[8][10]                     ############################
            
        return [initial_data,champs,stats,ids]
    except:
        print("Error accessing players in game")
        return [False]
