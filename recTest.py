import pandas as pd
import numpy as np
import ast
import json
import csv
import time
from scipy import stats

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


def calcPearson(dicofusers, gamesDic, listOfUserID, listOfGameID, user):

    temp1 = [0] * len(gamesDic)
    temp1[0] = float(listOfUserID.index(user))
    for y in dicofusers[user]:
        temp1[listOfGameID.index(y[0])+1] = 1
    data = []
    for x in listOfUserID[:100]:
        temp2 = [0] * len(gamesDic)
        temp2[0] = float(listOfUserID.index(x))
        for y in dicofusers[x]:
            temp2[listOfGameID.index(y[0])+1] = 1
    
        t1, t2 = stats.pearsonr(temp1, temp2)
        #print(x)
        #print(t1,t2)
        data.append((x, t1))
    
    return data

def getRecs(listOfsimilarUsers, dicofUsers, gamesDic):
    Recgames = []
    for x in listOfsimilarUsers:
        for y in dicofUsers[x[0]]:
            Recgames.append((y[0], x[1] * float(y[1])))
    Recgames.sort(key=lambda x:x[1])
    print(Recgames)
    return Recgames



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
    print("pearson testing")
    data = calcPearson(dicofusers, gamesDic, listOfUserID, listOfGameID, 'ARHP7M2HVVFLZ')#currently outputs Pval correctly but there is not much difference between the users
    print("done")
    data.sort(key=lambda x:x[1])
    
    getRecs(data[-5:], dicofusers, gamesDic)


    #for x in userList:
    #    templ = [0] * len(gamesDic)



    return 0

if __name__ == '__main__':
    main()
