import pandas as pd
import numpy as np
import ast
import json
import csv
import time
from scipy import stats
from scipy.spatial import distance

#from lightfm import LightFM

def readJSON(filen):
    with open(filen) as f:
        lines = f.readlines()

    data = {}
    for x in lines:
        j = ast.literal_eval(x)
        data[j['asin']] = j
    
    return data

def readCSV(filen):
    with open(filen, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    return data

def createDicOfUsers(users):
    d = {}
    for x in users:
        userID = x[0]
        gameID = x[1]
        rating = x[2]
        if userID in d:
            d[userID].append((gameID,rating))
        else:
            d[userID] = []
            d[userID].append((gameID,rating))
    return d


def calcPearson(dicofusers, gamesDic, listOfUserID, listOfGameID, user, N):

    temp1 = [0] * len(gamesDic)
    temp1[0] = float(listOfUserID.index(user))
    for y in dicofusers[user]:
        temp1[listOfGameID.index(y[0])+1] = 1
    data = []
    for x in listOfUserID[:N]:
        temp2 = [0] * len(gamesDic)
        temp2[0] = float(listOfUserID.index(x))
        for y in dicofusers[x]:
            temp2[listOfGameID.index(y[0])+1] = 1
    
        t1, t2 = stats.pearsonr(temp1, temp2)
        #print(x)
        #print(t1,t2)
        data.append((x, t1))
    data.sort(key=lambda x:x[1])
    return data#listofSimilarUsers

def calcCosine(dicofusers, gamesDic, listOfUserID, listOfGameID, user, N):
    
    temp1 = [0] * len(gamesDic)
    temp1[0] = float(listOfUserID.index(user))
    for y in dicofusers[user]:
        temp1[listOfGameID.index(y[0])+1] = 1
    data = []
    for x in listOfUserID[:N]:
        temp2 = [0] * len(gamesDic)
        temp2[0] = float(listOfUserID.index(x))
        for y in dicofusers[x]:
            temp2[listOfGameID.index(y[0])+1] = 1

        t1 = distance.cosine(temp1, temp2)
        data.append((x, t1))
    data.sort(key=lambda x:x[1])
    return data#listofSimilarUsers

def calcJaccard(dicofusers, gamesDic, listOfUserID, listOfGameID, user, N):
    
    temp1 = [0] * len(gamesDic)
    temp1[0] = float(listOfUserID.index(user))
    for y in dicofusers[user]:
        temp1[listOfGameID.index(y[0])+1] = 1
    data = []
    for x in listOfUserID[:N]:
        temp2 = [0] * len(gamesDic)
        temp2[0] = float(listOfUserID.index(x))
        for y in dicofusers[x]:
            temp2[listOfGameID.index(y[0])+1] = 1

        t1 = distance.jaccard(temp1, temp2)
        data.append((x, t1))
    data.sort(key=lambda x:x[1])
    return data#listofSimilarUsers

def getRecs(listOfsimilarUsers, dicofUsers, gamesDic):
    Recgames = []
    for x in listOfsimilarUsers:
        #print(x)
        for y in dicofUsers[x[0]]:
            #print(y)
            Recgames.append((y[0], x[1] * float(y[1])))
    Recgames.sort(key=lambda x:x[1])
    
    return Recgames

def checkResults(recs, expectedrecs):
    c = 0;
    for x in recs:
        if x[0] in expectedrecs:
            c += 1

    return c

def main():
    gamesDic = readJSON('meta_Video_Games.json')
    userList = readCSV('ratings_Video_Games.csv')
    #print(userList[0])
    #print(len(gamesDic))
    df = pd.DataFrame(userList)
    listOfGameID = []
    for x in gamesDic:
        listOfGameID.append(x)
    listOfGameID.sort()

    dicofusers = createDicOfUsers(userList)
    listOfUserID = []
    for x in dicofusers:
        listOfUserID.append(x)
    listOfUserID.sort()

    
    data = calcPearson(dicofusers, gamesDic, listOfUserID, listOfGameID, 'ARHP7M2HVVFLZ', 200000)#currently outputs Pval correctly but there is not much difference between the users
    data2 = calcCosine(dicofusers, gamesDic, listOfUserID, listOfGameID, 'ARHP7M2HVVFLZ', 200000)
    data3 = calcJaccard(dicofusers, gamesDic, listOfUserID, listOfGameID, 'ARHP7M2HVVFLZ', 200000)

    d = getRecs(data[-500:], dicofusers, gamesDic)
    d2 = getRecs(data2[-500:], dicofusers, gamesDic)
    d3 = getRecs(data3[-500:], dicofusers, gamesDic)
    


    l = []
    for x in dicofusers['ARHP7M2HVVFLZ']:
        #print(len(gamesDic[x[0]]['related']['also_bought']))
        for y in gamesDic[x[0]]['related']['also_bought']:
            l.append(y)
        for y in gamesDic[x[0]]['related']['buy_after_viewing']:
            l.append(y)
        for y in gamesDic[x[0]]['related']['bought_together']:
            l.append(y)

    c = checkResults(d, l)
    c2 = checkResults(d2, l)
    c3 = checkResults(d3, l)

    print("pearson: ", c)
    print("cosine: ", c2)
    print("jaccard: ", c3)
    return 0

if __name__ == '__main__':
    main()
