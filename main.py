#imports all the different files in Repo needed for running
import python_files.PlayerRanking as PlayerRanking
import python_files.Scraping as Scraping
import python_files.UserInput as UserInput

#get user input wanted
choice = UserInput.inputNum()

#get player wanted
player = UserInput.inputChoice(choice)

#get season and create desirable template for it to be used
choiceSecondary = 5
seasonFull = UserInput.inputChoice(choiceSecondary)
season = seasonFull[:5] + seasonFull[-2:] 

#get the dataframe of player, and then the stats for player
panda = Scraping.scrapeURL(player)
stats = Scraping.scrapeStats(panda, season)

#get season in template needed for percentile creation
seasonNum = seasonFull[-4:]
seasonNum = int(seasonNum)

#stats with minutes in it
statswmin = stats.copy()

#gets percentile dictionary
percentile = PlayerRanking.percentile(stats, seasonNum, player, False, True)

#gets position
pos = PlayerRanking.percentile(stats, seasonNum, player, True, False)

#normal grade
grade = PlayerRanking.grader(percentile, pos, False)

#per36 grade
per36 = PlayerRanking.per36(statswmin, seasonNum, player)

#prints out based on what the user requested.
print("")
if choice == 3:
    print(f"Regular grade: {grade}      Per 36 grade: {per36}")
elif choice == 2:
    print(f"Per 36 grade: {per36}")
elif choice == 1:
    print(f"Regular grade: {grade}")
