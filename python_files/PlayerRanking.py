#importing needed libraries, tools, etc
from scipy import stats
import pandas as pd
import numpy as np
from itertools import chain
from unidecode import unidecode


#remove puncuation from words to allow for user to not have to use them. returns word/name without punctuation
def nopunct(word):

        punctuations = '''!()-[];:'"\,<>./?@#$%^&*_~'''

        no_punct = ""
        for char in word:
            if char not in punctuations:
                no_punct = no_punct + char

        return no_punct


#this function creates percentiles per position based on players stats and returns percentile dictionary
#variables needed are the dictionary of stats, year, player name, boolean (if true) returns position, and boolean (if true) removes MP
def percentile(stats1, year, name, posGetter, MPRemover):

    #Removes MP
    if MPRemover == True:
        try:
            stats1.pop("MP")
        except:
            pass

    #reads and cleans dataframe for all players to get percentile for that year. Has every player no matter what. Used to get position.
    dfAll = pd.read_csv("csv_files/AllPlayer.csv")
    dfAll["player"] = dfAll["player"].apply(nopunct)
    dfAll['player'] = dfAll['player'].str.lower()
    dfAll["player"] = dfAll["player"].apply(unidecode)
    dfAll = dfAll.fillna(0)
    dfAll = dfAll.drop('birth_year', axis=1)

    #data frame of players above 18 minutes to ensure accurate percentile and not include low minute players
    df1 = pd.read_csv("csv_files/Book2.csv")
    df1 = df1.drop('birth_year', axis=1)
    df1 = df1.fillna(0)

    #removes puncuation, makes it lower case and usable
    df1["player"] = df1["player"].apply(nopunct)
    df1['player'] = df1['player'].str.lower()
    df1["player"] = df1["player"].apply(unidecode)

    #removes puncuation, makes it lower case and usable
    name = nopunct(name)
    name = name.lower()
    name = unidecode(name)

    #get dataframe for only year entered. Makes it fair to people in different eras.
    df = df1[df1.season == year]
    df = df.reset_index()

    #get player position
    playerDF = dfAll[dfAll.player == name]
    playerDF = playerDF.reset_index()
    position = playerDF.iloc[0]["pos"]

    #since center abbreviation is only one letter did this.
    if (position[:1] == "C"):
        position = "C"
    else:
        position = position[:2]

    #if posGetter is true it just returns position. Needed because position is also needed for other functions.
    if posGetter == True:
        return position
    

    #makes dataframe only position wanted. Not fair to judge a point guard against a center.
    df = df[df.pos == position]
    df = df.reset_index()
    
    #for loop to create percentile dictionary 
    for key in stats1:

        #this is the number of whatever the player has in key stat
        current = stats1[key]


        #gets current stat/key/column of all values within it in the dataframe of players.
        header = df[df.columns[df.columns.str.contains(pat = key.lower())]] 
        array1 =  header.values.tolist()
        array1 = list(chain.from_iterable(array1))

        #uses the stats of all players in given position and key, and then the current stat number
        #created percentile based on the players stat compared to all the other players stats
        percent = stats.percentileofscore(list(array1), float(current))

        #updates the array in same position with percentile instead of stat
        stats1[key] = percent

    return stats1

#This function matches the array keys of the machine learning dictionary to the stats dictionary, and returns machine learning as dictionary
def fix2D(arr):

    x = 0
    arrNew = []

    while x < len(arr):
        #removes first four letters(which is "Play") from the array
        str = arr[x][0]
        str = str[4:]

        #removes "M", which is in 3PM/2PM/FTM, as wanted to match other dictionaries. Then alters TO to TOV.
        str = str.replace("M", "")
        if str == "TO":
            str = "TOV"
        
        #updates array with new first value
        array = [str, arr[x][1]]
        arrNew.append(array)

        x+=1

    #makes array into dictionary and returns it
    dictionary = dict(arrNew)
    return dictionary


#sorts dictionary so both stats and machine learning numbers are same order and returns sorted dictionary
def sorter(dictionary):
    myKeys = list(dictionary.keys())
    myKeys.sort()
    sortDict = {i: dictionary[i] for i in myKeys}
    return sortDict

        

#returns machine learning array per each position. The numbers in array were obtained through machine learning, which is another file in this.
def getMach(pos):
    if pos=="PG":
        pg = [('playFGA', -0.6150401765027368), ('play2PA', -0.587864365884284), ('playFTA', -0.43491558462527713), ('play3PA', -0.372335754008891), ('playTO', -0.2928814224610756), ('playPF', -0.21098437240768603), ('playBLK', 0.1607203258682319), ('play2PM', 0.16970767529741962), ('playSTL', 0.2307367083975762), ('playTRB', 0.3280044638238135), ('playFGM', 0.3860068254120804), ('play3PM', 0.3885696291049632), ('playAST', 0.4340716794242032), ('playFTM', 0.4986970041813066), ('playPTS', 0.5123155820884346)]
        return pg
    elif pos == "SG":
        sg = [('playFGA', -0.5394601807104613), ('play3PA', -0.4226450679851406), ('play2PA', -0.38847502768030084), ('playTO', -0.37851264541517937), ('playFTA', -0.3560830001350487), ('playPF', -0.19058922050186472), ('playSTL', 0.20076801251805312), ('play2PM', 0.21858355994425616), ('playBLK', 0.21884991319551686), ('playTRB', 0.22452380083770562), ('playAST', 0.3847809434667279), ('play3PM', 0.3867531084521919), ('playFGM', 0.389942298665165), ('playFTM', 0.43540004026663887), ('playPTS', 0.4440208814758081)]
        return sg   
    elif pos == "SF":
        sf = [('play2PA', -0.6949341852121492), ('playFGA', -0.5539534572415938), ('playFTA', -0.37271630971478287), ('play3PA', -0.32617368122717455), ('playTO', -0.292560060445031), ('playPF', -0.18966488922021896), ('playSTL', 0.2130443038796281), ('playBLK', 0.21956545401258257), ('play3PM', 0.252398868164148), ('play2PM', 0.29101695857098564), ('playTRB', 0.3296591587600502), ('playFGM', 0.37544977442064303), ('playAST', 0.4519355903475483), ('playFTM', 0.4692108137885785), ('playPTS', 0.48576316464987757)]
        return sf  
    elif pos == "PF":
        pf = [('playFGA', -0.481603346153922), ('play2PA', -0.4086075137909164), ('playFTA', -0.33928498367018256), ('play3PA', -0.2362922921301261), ('playTO', -0.22111994729848708), ('playPF', -0.1588337721367012), ('playSTL', 0.08743556501032963), ('playTRB', 0.2290695793540878), ('playBLK', 0.24163199883496972), ('play3PM', 0.2709024273789652), ('play2PM', 0.28199162905124636), ('playFGM', 0.3600807368975874), ('playFTM', 0.3696791716807797), ('playAST', 0.4294005020600464), ('playPTS', 0.4658518614032071)]
        return pf
    elif pos == "C":
        c = [('playFGA', -0.457832179033364), ('play3PA', -0.36380637111678527), ('play2PA', -0.32728140285931084), ('playTO', -0.2537699464438458), ('playPF', -0.06858812708365918), ('playFTA', 0.05099487092167494), ('playSTL', 0.07873503986931603), ('playFTM', 0.09525562326899843), ('play2PM', 0.23571383953609684), ('playTRB', 0.24661538427329757), ('play3PM', 0.28770826333841515), ('playPTS', 0.3187824588087106), ('playFGM', 0.32039212543291645), ('playBLK', 0.35344011274347376), ('playAST', 0.3791307874748197)]
        return c
    
#this is the main grader which is based on percentiles and position. returns grade.
#takes in percentile dictionary, position, and boolean that removes MP (if true)
def grader(perc, pos, MPRemover):
    
    #removes MP
    if MPRemover == True:
        perc.pop("MP")

    x = 0
    posit = 0
    negat = 0

    #makes machLearning and perc match each other
    machList = getMach(pos)
    machLearner = fix2D(machList)
    machLearner = sorter(machLearner)
    perc = sorter(perc)

    #Where all grading is done
    for key in perc:
        
        machNum = machLearner[key]
        percNum = perc[key]
    
        #Gives more emphasis on points and less punishment on the negatives. 
        #This is needed or else star players are ranked far too low, as it is too harsh of a punisher and points are too low.
        #multiplies percentile by coefficient from machine learning and adds them all
        if machNum>0:
            if key == "PTS":
                posit = posit + machNum*2
                x += machNum*percNum*2
            else: 
                posit+=machNum
                x += machNum*percNum
        else:
            machNum = machNum*.5
            negat = negat + (machNum)
            x += machNum*percNum


    #this is done so all positions are on same scale. If not done, positions with less positive factors are rated too harshly.
    x = x/(posit+negat)

    return x

#this makes the stats based on per36 and then grades them based on this and returns per36 grade
def per36(stats, year, name):

    #gets mp and multiplier needed
    mp = stats["MP"]
    mp = float(mp)
    num = (36/mp)

    #makes stats on per36 basis
    for key in stats:
        stat = stats[key]
        stat = float(stat)
        stats[key] = stat*num

    #removes MP and then does grading system done before with percentile, position, then grader.
    stats.pop("MP")
    percentDict = percentile(stats, year, name, False, False)
    pos = percentile(stats, year, name, True, False)
    grade = grader(percentDict, pos, False)

    return grade




