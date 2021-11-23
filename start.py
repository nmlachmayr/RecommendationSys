import csv
import json
import time


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
            print("error")
            #print out erronious string and wait.
            #print(x)
            #time.sleep(60)
        


    #print(len(data))
    #print(data[0]["description"])

    return data




def main():
    print("start main")
    reviewData = readCSV('ratings_Video_games.csv')
    #print(d[0])
    metaData = readJSON('meta_Video_Games.json')
    #print(d2[0])
    return 0

if __name__ == '__main__':
    main()