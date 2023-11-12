import threading
import time
import requestHandler
import requestURLs
import queue
import jsonHandler
import urllib
import ssl
import certifi
import csv
import json

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
            
def scrapeMatch(region,matchID,p,h):
    url = requestURLs.match_from_matchID_url(region,matchID)
    matchJson = requestHandler.requestReturn(url,p)
    if matchJson == None:
        print("Error 3")
        return
    
    matchInfo = jsonHandler.getMatch(matchJson)
    h.add(matchInfo,matchID)

def scrapePlayer(region, sID, p, q):
    url = requestURLs.puuID_from_sID_url(region, sID)
    playerJson = requestHandler.requestReturn(url, p)
    if playerJson == None:
        print("Error 1")
        return
    puuid = jsonHandler.getPuuID(playerJson)

    url = requestURLs.matchIDs_from_puuID_url(region, puuid)
    matchesJson = requestHandler.requestReturn(url, p)
    if matchesJson == None:
        print("Error 2")
        return
    matchIDs = jsonHandler.getMatchIDs(matchesJson)
    q.put(matchIDs)


def scrapeLeague(region, h, history):
    print(("Starting collection from %s \n") % (region))
    p = requestHandler.Permits()
    
    s1 = stopper()
    t1 = threading.Thread(target=requestHandler.manager, args=(1.25,p,s1,))
    t1.start()

    s2 = stopper()
    t2 = threading.Thread(target=requestHandler.enforcer, args=(region,p,s2,))
    t2.start()

    url = requestURLs.gm_url(region)
    leagueJson = requestHandler.requestReturn(url, p)
    if leagueJson == None:
        print("Error 0")
        return

    sIDs = jsonHandler.getChallengers(leagueJson)

    print("Found %d Grandmaster players in %s! \n" % (len(sIDs),region))

    matchIDQueue = queue.Queue()

    for sID in sIDs:
        scrapePlayer(region,sID,p,matchIDQueue)

    matches = set()
    
    while not matchIDQueue.empty():
        remaining = matchIDQueue.get()
        if remaining != None:
            for ID in remaining:
                if not ID in history:
                    matches.add(ID)

    print("Scraping %d matches from %s \n" % (len(matches),region))
            
    for matchID in matches:
        scrapeMatch(region,matchID,p,h)
        
    s1.stop()
    s2.stop()
    t1.join()
    t2.join()
    
    print("Finished all games from %s \n" % (region))
        
        
if __name__ == '__main__':
    url = requestURLs.match_from_matchID_url('NA','NA1_4497499619')

    req = urllib.request.Request(url)

    response = urllib.request.urlopen(req,context=ssl.create_default_context(cafile=certifi.where()))

    cont = None
    
    if response.getcode() == 200:
        cont = json.loads(response.read().decode('utf-8'))

    matchInfo = jsonHandler.getMatch(cont)
    print(str(fix(matchInfo)))
    
