import threading
import time
import urllib.request
import ssl
import certifi
import json
        
class Permits(object):
    def __init__(self, val = 0):
        self.lock = threading.Lock()
        self.availablePermits = val
        self.requestsProcessed = 0
        
    def addPermit(self):
        self.lock.acquire()
        try:
            self.availablePermits = min(self.availablePermits + 1,20)
        finally:
            self.lock.release()
            
    def usePermit(self):
        self.lock.acquire()
        worked = False
        try:
            if self.availablePermits > 0:
                self.availablePermits = self.availablePermits - 1
                self.requestsProcessed = self.requestsProcessed + 1
                worked = True
        finally:
            time.sleep(0.05)
            self.lock.release()
            return worked

def manager(waitTime,p,s):
    while s.running:
        time.sleep(waitTime)
        p.addPermit()

def enforcer(region,p,s):
    start_time = time.time()
    while s.running:
        time.sleep(90)
        print("%s has processed %d requests in %f seconds" % (region,p.requestsProcessed,time.time()-start_time))
            
def requestReturn(url,p):
    ready = False
    failures = 0
    while not ready:
        ready = p.usePermit()
        if failures < 4:
            failures += 1
        time.sleep(failures * 0.3)

    req = urllib.request.Request(url)

    try:
        response = urllib.request.urlopen(req,context=ssl.create_default_context(cafile=certifi.where()))
    except:
        print("Error opening url %s" % (url))
        return None
    
    if response.getcode() == 200:
        cont = json.loads(response.read().decode('utf-8'))
        return cont
    else:
        return None
   
def request(url,p,q):
    ready = False
    failures = 0
    while not ready:
        ready = p.usePermit()
        if failures < 4:
            failures += 1
        time.sleep(failures * 0.3)
    
    req = urllib.request.Request(url)
    
    try:
        response = urllib.request.urlopen(req,context=ssl.create_default_context(cafile=certifi.where()))
    except:
        print("Error opening url %s" % (url))
        q.put(None)
        
    if response.getcode() == 200:
        cont = json.loads(response.read().decode('utf-8'))
        q.put(cont)
    else:
        q.put(None)

def requestPage(url,p):
    ready = False
    failures = 0
    while not ready:
        ready = p.usePermit()
        if failures < 4:
            failures += 1
        time.sleep(failures * 0.3)

    req = urllib.request.Request(url)

    try:
        response = urllib.request.urlopen(req,context=ssl.create_default_context(cafile=certifi.where()))
    except:
        print("Error opening url %s" % (url))
        return None
    
    if response.getcode() == 200:
        return response
    else:
        return None
