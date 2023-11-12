import threading
import time
import requestHandler
import requestURLs
import queue
import jsonHandler
import champDict
import json
import csv
import bs4
from bs4 import BeautifulSoup

series = {'LLA': ['Opening_Season','Opening_Playoffs','Closing_Season','Closing_Playoffs'],'CBLOL': ['Split_1','Split_1_Playoffs','Split_2','Split_2_Playoffs'],'LCS' : ['Spring_Season','Spring_Playoffs','Summer_Season','Championship'], 'LEC': ['Spring_Season','Spring_Playoffs','Summer_Season','Summer_Playoffs'], 'LCK': ['Spring_Season','Spring_Playoffs','Summer_Season','Summer_Playoffs'], 'LCK_CL':['Spring_Season','Spring_Playoffs','Summer_Season','Summer_Playoffs'], 'European_Masters': ['Spring_Main_Event','Summer_Main_Event'], 'NA_Academy_League': ['Spring_Season','Proving_Grounds_Spring','Summer_Season','Proving_Grounds_Summer']}
weights = {'LCK': 20, 'LEC': 18, 'LCS': 16, 'LCK_CL': 13, 'European_Masters': 12, 'NA_Academy_League': 9, 'LLA':10, 'CBLOL': 10}
international_events = {2022: ['https://lol.fandom.com/wiki/2022_Season_World_Championship/Main_Event','https://lol.fandom.com/wiki/2022_Mid-Season_Invitational']}
international_weights = {2022: [15,15]}
international_events = {2021: ['https://lol.fandom.com/wiki/2021_Season_World_Championship/Main_Event','https://lol.fandom.com/wiki/2021_Mid-Season_Invitational']}
international_weights = {2021: [15,15]}

def fix(statList):
    result = []
    for i in statList:
        if isinstance(i,list) and not isinstance(i,str):
            result2 = fix(i)
            result = result + result2
        else:
            result.append(i)
    return result

class stopper:
    def __init__(self):
        self.running = True
        
    def stop(self):
        self.running = False
    
class taskHolder(object):
    def __init__(self, destination, history):
        self.lock = threading.Lock()
        self.games = []
        self.gameIDs = []
        self.destination = destination
        self.history = history

    def add(self, game, matchID):
        self.lock.acquire()
        try:
            self.games.append(game)
            self.gameIDs.append(matchID)
        finally:
            self.lock.release()
            
    def size(self):
        self.lock.acquire()
        num = 0
        try:
            num = len(self.games)
        finally:
            self.lock.release()
            return num

    def flush(self):
        self.lock.acquire()
        try:
            parsed = []
            patches = []
            for i in range(0, len(self.games)):
                parsed.append(fix(self.games[i]))
            with open(self.destination, "a+") as my_csv:
                    csvWriter = csv.writer(my_csv, delimiter=',')
                    csvWriter.writerows(parsed)
            with open(self.history, "a+") as my_file:
                for ID in self.gameIDs:
                    my_file.write(ID + "\n")
                
            self.games = []
            self.gameIDs = []
        finally:
            self.lock.release()

def updater(threshold,h,s):
    while s.running:
        time.sleep(5)
        if h.size() > threshold:
            num = len(h.games)
            h.flush()
            print("Saved %d matches \n" % (num))
        else:
            print("%d matches unsaved \n" % (len(h.games)))
            
def scrapeWikiMatch(url,weight,matchType,p,h):
    soup = BeautifulSoup(requestHandler.requestPage(url,p),'lxml')
    matchJson = json.loads(soup.find("textarea").text)
    matchID = "ESPORTSTMNT02_" + str(matchJson['gameId'])
    if matchJson == None:
        print("Error 3")
        return False

    matchInfo = [False]
    if matchType == 5:
        matchInfo = jsonHandler.getWikiMatch5(matchJson,weight)

    if matchInfo[0] != False:
        h.add(matchInfo,matchID)
    else:
        print(matchID)

def scrapeSeason(season, h, history):
    print(("Starting collection from %s \n") % (season))
    p = requestHandler.Permits()
    
    s1 = stopper()
    t1 = threading.Thread(target=requestHandler.manager, args=(0.05,p,s1,))
    t1.start()

    s2 = stopper()
    t2 = threading.Thread(target=requestHandler.enforcer, args=(season,p,s2,))
    t2.start()

    splitURLs = international_events[season]
    splitWeights = international_weights[season]
    leagues = ["LCK","LCS","LEC","LCK_CL","European_Masters","NA_Academy_League","CBLOL","LLA"]
    for league in leagues:
        prefix = requestURLs.pro_url(league,season)
        for suffix in series[league]:
            splitURLs.append(prefix+suffix)
            splitWeights.append(weights[league])

    matchURLs = []
    matchWeights = []
    matchTypes = []

    for i in range(0,len(splitURLs)):
        url = splitURLs[i]
        page = requestHandler.requestPage(url,p)
        splitPage = BeautifulSoup(page,'html.parser')
        matchLinks = splitPage.select('a[href*="/wiki/V5_metadata:"]')
        for link in matchLinks:
            matchURLs.append("https://lol.fandom.com/V5_data:" + link.get("href")[18:] + "?action=edit")
            matchWeights.append(splitWeights[i])
            matchTypes.append(5)
        
    print("Found %d pro games played in %s! \n" % (len(matchURLs),season))
            
    for i in range(0,len(matchURLs)):
        matchURL = matchURLs[i]
        try:
            scrapeWikiMatch(matchURL,matchWeights[i],matchTypes[i],p,h)
        except:
            pass
        
    s1.stop()
    s2.stop()
    t1.join()
    t2.join()

    h.flush()
    
    print("Finished all games from %s \n" % (season))
        
        
if __name__ == '__main__':
    holder = taskHolder('gameDataPro.csv','parsedProMatches.txt')

    historyList = []

    with open('parsedMatches.txt','r') as historyFile:
        content = historyFile.read()
        historyList = content.split("\n")

    history = set(historyList)
    
    s = stopper()
    t1 = threading.Thread(target = updater, args=(50,holder,s,))
    t1.start()

    t = threading.Thread(target=scrapeSeason, args=(2021,holder,history,))
    t.start()
    
    t.join()
        
    s.stop()
    t1.join()
    
    print("Done!")
