import csv
import json
import time
from scipy import stats
import scipy

'''
Reads video games ratings, adds to list of tuples

UserID, GameID, Rating, GameID(??)
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

    tweets = []
    f = open(filen, 'r')

    l = []
    for line in f:
        n = line.replace("'", '"')
        l.append(n)  
        
    data = []
    for x in l:
        try:
            t = json.loads(x) 
            data.append(t)
        
        except(Exception):
            time.sleep(0);
            #print("error")
            #print out erronious string and wait.
            #print(x)
            #time.sleep(60)
        
    #print(len(data))
    #print(data[0]["description"])

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


def topNclosestNeighborsPearson(N, d, key):
    l = []
    for x in d:
        #print(d[key], d[x])
        m = min(len(d[key]),len(d[x]))
        #print(m)
        #print(d[key][:m], d[x][:m])
        if m > 2:
            t1 = extractItemFromTuples(d[key][:m], 1)
            t2 = extractItemFromTuples(d[x][:m], 1)
            #print(x)
            #print("t1: ", t1)
            #print("t2: ", t2)
            val1, val2 = stats.pearsonr(t1, t2)
            #print(val1, val2)
            l.append((x, val2))
        else:
            #if m < 2 then pearsonr doesnt work so score it 0
            l.append((x, 0))

    l.sort(key=lambda x:x[1])#sort each list by second element in tuple(pearson score)

    return l[:N]

def extractItemFromTuples(t, i):
    l = []
    for x in t:
        l.append(float(x[i]))

    return l

def main():
    print("start main")
    reviewData = readCSV('ratings_Video_games.csv')
    #print(reviewData[1])
    metaData = readJSON('meta_Video_Games.json')
    #print(metaData[0]['asin'])


    dGames = createDicOfGames(reviewData)
    dUsers = createDicOfUsers(reviewData)
    #print(dGames['B00LGBJIQ4'])#[('AEEMJX418B5RC', '5.0'), ('A265KF0CQ058RZ', '5.0'), ('A20J2PMC9ZPD4F', '5.0'), ('A3HMVWAGUCNA1K', '5.0')]
    #print(dUsers['A265KF0CQ058RZ'])#[('B004RMK4BC', '5.0'), ('B00KKAQYXM', '5.0'), ('B00LGBJIQ4', '5.0')]

    print("Number of Items: ",len(dGames))#Number of Items:  50210
    print("Number of Users: ", len(dUsers))#Number of Users:  826767


    d = topNclosestNeighborsPearson(10, dGames, 'B00KKAQYXM')
    print(d)
    
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