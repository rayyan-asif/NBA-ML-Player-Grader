import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from unidecode import unidecode

#make sure do not go over rate limit of 20 requests per minute. If over, sportsreference puts in "jail" for an hour
rate = 0
def checkRate(r):
    global rate
    if r > 16:
        rate = 0
        time.sleep(61)

#gets URL for the player inputted and returns url. url format is same for all players.
def scrapeURL(player1):

    global rate

    #remove punctuation for full name
    def nopunct(word):

        punctuations = '''!()-[];:'"\,<>./?@#$%^&*_~'''

        no_punct = ""
        for char in word:
            if char not in punctuations:
                no_punct = no_punct + char

        return no_punct

    #make player name usable without punctuation
    player1 = nopunct(player1)
    player1 = unidecode(player1)
    player1 = player1.lower()


    #creating first and last name variables for player
    names = player1.split()
    firstName = names[0]
    lastName = names[1]


    url = "https://www.basketball-reference.com/players/"


    #insert the player name part of the url which is first five letters of players last name.
    url += (lastName[0].lower() + "/")
    if len(lastName)>=5:
        for num in range(5):
            url += lastName[num].lower()
    else:
        url += lastName.lower()
    
    #then add first two letters of first name
    if len(firstName)>=2:
        for num in range (2):
            url += firstName[num].lower()
    else:
        url += firstName.lower()


    codeNum1 = 0
    codeNum2 = 2
    url += "01.html"

    #Finding name of player (made undercased and no punctuation) to check validity
    checkRate(rate)
    page = requests.get(url)
    rate += 1
    soup = BeautifulSoup(page.content, 'html.parser')
    player_name = soup.find('h1').text
    player_name = player_name.strip()
    player_name = nopunct(player_name)
    player_name = unidecode(player_name)
    player_name = player_name.lower()


    index = url.index("01")
    


    #url construction as some players have same 5 letters in last name and 2 in first. 
    #Adds 1 each time to test a new URL until player names match.
    while True:
        if player_name == player1:
            break
        else:

            #just to make sure not infinite loop
            if codeNum1>1 and codeNum2>4:
                print("Could not get URL. Name may have been misentered.")
                break

            url = url[:index]
            url = url + str(codeNum1) + str(codeNum2) + ".html"

            checkRate(rate)
            page = requests.get(url)
            rate += 1

            #get new player name and page content to test if this is now correct URL
            soup = BeautifulSoup(page.content, 'html.parser')

            player_name = soup.find('h1').text
            player_name = player_name.strip()
            player_name = unidecode(player_name)
            player_name = player_name.lower()
            player_name = nopunct(player_name)

            codeNum2 += 1



            #needed in case its very common name
            if (codeNum2 % 10)==0:
                codeNum1 += 1
                codeNum2 = codeNum2 - 10
    return soup


#returns dictionary of stats for player and season. inputs the page of html and season wanted.
def scrapeStats(page, season1):
    global rate
    dictionary = {}

    #Making table with soup and pandas
    table = page.find_all("table")

    #Ensure there is actually a dictionary.
    try:
        dfs1 = pd.read_html(str(table))[1]
    except:
        return dictionary
    
    #cleans dataframe, then makes new dictionary of table. Then gets the stats wanted for Grading.
    dfs1 = dfs1.fillna(0)
    baseDFS = dfs1.to_dict('index')
    baseStats = ["MP", "FG", "FGA", "3P", "3PA", "2P", "2PA", "FT", "FTA", "TRB", "AST", "STL", "BLK", "TOV", "PF", "PTS"]
    

    listID = 0

    #gets correct dictionary based on season by making sure it exists and matches season wanted. 
    while True:
        while True:
            try:
                seas = baseDFS[listID]["Season"]
            except:
                listID += 1
            else:
                break

            #make sure no infinite loop
            if listID>100:
                return dictionary
        
        #test validity of season
        if seas == season1:
            break
        else:
            listID += 1
    

    #make dictionary of just the stats wanted and just the season wanted.
    for stat in baseStats:
        try:
            dictionary[stat] = baseDFS[listID][stat]
        except:
            pass


    return dictionary

    

