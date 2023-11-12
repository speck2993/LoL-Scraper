import csv

def unstack(statList):
    result = []
    for i in statList:
        if isinstance(i,list) and not isinstance(i,str):
            result2 = unstack(i)
            result = result + result2
        else:
            result.append(i)
    return result

def statParse(currentRows):
    stats = []
    for i in range(0,10):
        player = currentRows[i]
        playerStats = []
        time = float(player[23])
        kills = int(player[25])
        deaths = int(player[26])
        assists = int(player[27])
        damageDealt = int(player[69])
        damageTanked = float(player[72]) + float(player[73])
        gold = float(player[83])
        shield = 0 #not tracked by OE
        heal = 0 #not tracked by OE
        cs = float(player[92])
        cc = 0 #not tracked by OE
        turretDamage = 0 #not tracked by OE
        vision = float(player[80])
        factor = 60.0/time
        playerStats = [kills*factor, deaths*factor, assists*factor, damageDealt*factor, gold, heal*factor, shield*factor, cc*factor, turretDamage, cs, vision, damageDealt/(gold*time + 1), damageTanked/(deaths+1)]                  
        stats.append(playerStats)
    stats[3][5] = stats[3][5] + stats[4][5]         ############################
    stats[3][10] = stats[3][10] + stats[4][10]      # Pooling ADC and Sup      #
    stats[4][5] = stats[3][5]                       # gold and CS stats        #
    stats[4][10] = stats[3][10]                     # to account for           #
    stats[8][5] = stats[8][5] + stats[9][5]         # items like Targon's      #
    stats[8][10] = stats[8][10] + stats[9][10]      # and duos like Senna/Tahm #
    stats[9][5] = stats[8][5]                       #                          #
    stats[9][10] = stats[8][10]                     ############################
    return stats
    

with open('2022_OE_Data.csv', 'r') as file:
    with open('fixed_2022_OE_Data.csv', 'a+') as file2:
        reader = csv.reader(file)
        writer = csv.writer(file2,delimiter=',')
        currentRows = []
        rowsRead = 0
        burnedFirst = False
        for row in reader:
            if not burnedFirst:
                burnedFirst = True
            else:
                currentRows.append(row)
                rowsRead += 1
                if rowsRead == 12:
                    if currentRows[0][1] == 'complete':
                        newRow = []
                        initial_data = [currentRows[0][0],10,currentRows[0][9],(int(currentRows[10][24]) == 1)]
                        champs = [playerRow[17] for playerRow in currentRows[0:10]]
                        stats = statParse(currentRows[0:10])
                        players = [playerRow[14] for playerRow in currentRows[0:10]]
                        newRow = [initial_data,champs,stats,players]
                        newRow2 = unstack(newRow)
                        writer.writerow(newRow2)
                    rowsRead = 0
                    currentRows = []
    
    

