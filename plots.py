import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt

from winRecords import winRecords, binaryFTR, updateFTR, sumFoul



# Loading the files, right now just doing this by each line, later I'll use OS and import them all from folder

s1819 = pd.read_csv("serieA/serieA_season-1819.csv")
s1718 = pd.read_csv("serieA/serieA_season-1718.csv")
s1617 = pd.read_csv("serieA/serieA_season-1617.csv")
s1516 = pd.read_csv("serieA/serieA_season-1516.csv")
s1415 = pd.read_csv("serieA/serieA_season-1415.csv")
s1314 = pd.read_csv("serieA/serieA_season-1314.csv")
s1213 = pd.read_csv("serieA/serieA_season-1213.csv")
s1112 = pd.read_csv("serieA/serieA_season-1112.csv")
s1011 = pd.read_csv("serieA/serieA_season-1011.csv")
s0910 = pd.read_csv("serieA/serieA_season-0910.csv")

totalcol=[s0910, s1011, s1112, s1213, s1314, s1415, s1516, s1617, s1718, s1819]

wins = np.zeros(len(totalcol))
losses = np.zeros(len(totalcol))
draws = np.zeros(len(totalcol))
homeFouls = np.zeros(len(totalcol))
awayFouls = np.zeros(len(totalcol))
homeY = np.zeros(len(totalcol))
awayY = np.zeros(len(totalcol))
homeR = np.zeros(len(totalcol))
awayR = np.zeros(len(totalcol))

# winRecords function input: data, leagueName, category
# winRecords function output: homeWins, awayWins, draws


for i in range(len(totalcol)):
    wins[i] = winRecords(totalcol[i], 'Serie A', 'FTR')[0]
    losses[i] = winRecords(totalcol[i], 'SerieA', 'FTR')[1]
    draws[i] = winRecords(totalcol[i], 'SerieA', 'FTR')[2]

# sumFoul function input: data, category
# sumFoul function output: Sum of Fouls

for j in range(len(totalcol)):
    homeFouls[j] = sumFoul(totalcol[j], 'HF')
    awayFouls[j] = sumFoul(totalcol[j], 'AF')

    # Using sumFoul to sum up the home yellow, red; away yellow, red cards given out

    homeY[j] = sumFoul(totalcol[j], 'HY')
    homeR[j] = sumFoul(totalcol[j], 'HR')
    awayY[j] = sumFoul(totalcol[j], 'AY')
    awayR[j] = sumFoul(totalcol[j], 'AR')


seasons = np.arange(10)
my_xticks = ['2009/10','2010/11','2011/12','2012/13', '2013/14', '2014/15', '2015/16', '2016/17', '2017/18', '2018/19']

finDF = pd.DataFrame({'Season': my_xticks, 'Home Wins': wins, 'Away Wins': losses, 'Draws': draws})
#finDF.to_csv('SumRes.csv')
foulsDF = pd.DataFrame({'Season': my_xticks, 'Home Fouls': homeFouls, 'Away Fouls': awayFouls, 'Home - Away Fouls': (homeFouls - awayFouls)})
#foulsDF.to_csv('SumFouls.csv')
cardsDF = pd.DataFrame({'Season': my_xticks, 'Home Yellow Cards': homeY, 'Away Yellow Cards': awayY, 'Home Red Cards': homeR, 'Away Red Cards': awayR, 'Home - Away Yellow Cards': homeY - awayY, 'Home - Away Red Cards': homeR - awayR})
cardsDF.to_csv('SumCards.csv')


'''
plt.xticks(seasons, my_xticks)
plt.plot(seasons, homeFouls)
plt.xlabel('Season')
plt.ylabel('Home Fouls')
plt.show()

plt.xticks(seasons, my_xticks)
plt.plot(seasons, awayFouls)
plt.xlabel('Season')
plt.ylabel('Away Fouls')
plt.show()


plt.xticks(seasons, my_xticks)
plt.bar(seasons, homeFouls - awayFouls)
plt.xlabel('Season')
plt.ylabel('Home - Away Fouls')
plt.show()


plt.xticks(seasons, my_xticks)
plt.plot(seasons, wins)
plt.xlabel('Season')
plt.ylabel('Home Wins')
plt.show()

plt.xticks(seasons, my_xticks)
plt.plot(seasons, losses)
plt.xlabel('Season')
plt.ylabel('Away Wins')
plt.show()

plt.xticks(seasons, my_xticks)
plt.scatter(seasons, draws)
plt.xlabel('Season')
plt.ylabel('Draws')
plt.show()
'''













