import csv
import json
import time
from scipy import stats
import scipy
import ast

'''
Reads video games ratings, adds to list of tuples

UserID, GameID, Rating, timestamp
AB9S9279OZ3QO,0078764343,5.0,1373155200
'''
def readCSV(filen):
    with open(filen, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    return data


'''
Meta video games not in correct JSON format('s instead of "s)
replace all 's for "s and then convert to JSON then add to data (list of dics)

as of now 30k/50k work, rest throw error for some reason that i cant figure out
'''
def readJSON(filen):
    with open(filen) as f:
        lines = f.readlines()

    data = {}
    for x in lines:
        j = ast.literal_eval(x)
        data[j['asin']] = j
    
    return data
'''
Create dic of lists
asin of games is the keys of dictionaries, values are a tuple of (UserID,score)

Users input:
['AB9S9279OZ3QO', '0078764343', '5.0', '1373155200']

'''
def createDicOfGames(users):
    d = {}
    for x in users:
        userID = x[0]
        gameID = x[1]
        rating = x[2]
        if gameID in d:
            d[gameID].append((userID,rating))
        else:
            d[gameID] = []
            d[gameID].append((userID,rating))

    
    return d

'''
Create dic of lists
UserID is the keys of dictionaries, values are a tuple of (asin,score)

Users input:
['AB9S9279OZ3QO', '0078764343', '5.0', '1373155200']

'''
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
        temp1[listOfGameID.index(y[0])+1] = float(y[1])

    for x in listOfUserID:
        temp2 = [0] * len(gamesDic)
        temp2[0] = float(listOfUserID.index(x))
        for y in dicofusers[x]:
            temp2[listOfGameID.index(y[0])+1] = float(y[1])
    

        t1, t2 = stats.pearsonr(temp1, temp2)
        print(x)
        print(t1,t2)

    return 0



def main():
    print("start main")
    #reviewData = readCSV('ratings_Video_games.csv')
    #print(reviewData[1])
    #metaData = readJSON('meta_Video_Games.json')
    #print(metaData[0]['asin'])


    #dGames = createDicOfGames(reviewData)
    #dUsers = createDicOfUsers(reviewData)
    #print(dGames['B00LGBJIQ4'])#[('AEEMJX418B5RC', '5.0'), ('A265KF0CQ058RZ', '5.0'), ('A20J2PMC9ZPD4F', '5.0'), ('A3HMVWAGUCNA1K', '5.0')]
    #print(dUsers['A265KF0CQ058RZ'])#[('B004RMK4BC', '5.0'), ('B00KKAQYXM', '5.0'), ('B00LGBJIQ4', '5.0')]

    #print("Number of Items: ",len(dGames))#Number of Items:  50210
    #print("Number of Users: ", len(dUsers))#Number of Users:  826767

    gamesDic = readJSON('meta_Video_Games.json')
    userList = readCSV('ratings_Video_Games.csv')
    print(userList[0])
    print(len(gamesDic))

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
    calcPearson(dicofusers, gamesDic, listOfUserID, listOfGameID, 'ARHP7M2HVVFLZ')

    
    return 0

if __name__ == '__main__':
    main()


    '''
    Notes:

    What we could do with the Pearson score is go through every User/Game and calculate the 
    similarity score for each User/Game then we could find a number of nearest neighbors
    
    Then we could recommend games from these n number of similar games or games that similar
     users have reiviewed highly

    we could also attempt to predict a review score for each game based on the pearson score. 
    We could then use this to recommend games.
    
    '''