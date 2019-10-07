import numpy as np
import pandas as pd


def winRecords(data, leagueName, cat):
    
    ftr = data[cat]

    homeWins=0
    awayWins=0
    draws=0
    
    for i in range(0, len(ftr.to_numpy())):

        if (ftr.to_numpy()[i] == 'H'):
            homeWins += 1
            #print(j)
        elif (ftr.to_numpy()[i] == 'A'):
            awayWins += 1
        else:
            draws +=1

    #return leagueName, 'HomeWins: %s' % homeWins, 'Away Wins: %s' % awayWins, 'Draws: %s' % draws
    return [homeWins, awayWins, draws]


def binaryFTR(data, cat):
    ftr = data[cat]

    
    for i in range(0, len(ftr.to_numpy())):

        if (ftr.to_numpy()[i] == 'H'):
            ftr.to_numpy()[i] = 0
            #print(j)
        elif (ftr.to_numpy()[i] == 'A'):
            ftr.to_numpy()[i] = 1
        else:
            ftr.to_numpy()[i] = 2
        #ftr.to_numpy()[len(ftr.to_numpy)] =

    #return leagueName, 'HomeWins: %s' % homeWins, 'Away Wins: %s' % awayWins, 'Draws: %s' % draws
    return ftr