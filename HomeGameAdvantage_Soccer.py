import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf 
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report



# General function that isolates the full time result to see record of wins/losses/draws

def winRecords(data, leagueName, cat):
    
    ftr = data[cat]

    homeWins=0
    awayWins=0
    draws=0
    
    for i in range(0, len(ftr.to_numpy())-1):

        if (ftr.to_numpy()[i] == 'H'):
            homeWins += 1
            #print(j)
        elif (ftr.to_numpy()[i] == 'A'):
            awayWins += 1
        else:
            draws +=1

    #return leagueName, 'HomeWins: %s' % homeWins, 'Away Wins: %s' % awayWins, 'Draws: %s' % draws
    return [leagueName, homeWins]


#print(winRecords(pd.read_csv("serieA/serieA_season-1516.csv"), 'SerieA_15_16', 'FTR'))
#print(winRecords(pd.read_csv("serieA/serieA_season-1617.csv"), 'SerieA_16_17', 'FTR'))
#print(winRecords(pd.read_csv("serieA/serieA_season-1819.csv"), 'SerieA_18_19', 'FTR'))
#print(winRecords(pd.read_csv("epl_season-1819.csv"), 'EPL_18_19', 'FTR'))


# Let's start with the training/learning/evaluating/testing Machine Learning Method! First, we need to clean the data.
# Note: This script was written assuming all the data files will have the same default columns. This is true for the datasets that I've downloaded from the internet.
# I removed (in some of these files) the betting odds, as I figure these may influence results in ways outside of the determinants of the game. 
# Odds are set by bookkeepers, based on their own analysis.


def cleanData(dataFileCSV):

    data = pd.read_csv(dataFileCSV)

    # Dropping the Div and Dates

    data = data.drop('Div', axis=1)
    data = data.drop('Date', axis=1)

    # Dropping the Full Time Home Goals Scored, FTAG

    data = data.drop('FTAG', axis=1)
    data = data.drop('FTHG', axis=1)

    # Dropping the Half Time Home Goals Scored, HTAG, and the Half time result

    data = data.drop('HTHG', axis=1)
    data = data.drop('HTAG', axis=1)
    data = data.drop('HTR', axis=1)

    data['FTR'].unique()

    return data

# Change the string for Full Time Result (FTR), AKA the outcome to 0s and 1s. 1 if the Home Team wins, 0 if the Away Team won or if a Draw was achieved.
# We're looking for a categorical outcome, so it makes it easier to describe the events as a Home Win or a Away Win/Draw.

def fix_outcome(outcome):
    if outcome == 'H':
        return 1
    else:
        return 0


def trainModel(data):
    data['FTR'] = data['FTR'].apply(fix_outcome)

    # Train Test Split Data

    x_data = data.drop('FTR', axis=1)
    y_labels = data['FTR']
    X_train, X_test, y_train, y_test = train_test_split(x_data, y_labels, test_size=0.3, random_state=101)


    # Create tf.feature_columns for Categorical Values

    HomeTeam = tf.feature_column.categorical_column_with_hash_bucket('HomeTeam', hash_bucket_size=1000)
    AwayTeam = tf.feature_column.categorical_column_with_hash_bucket('AwayTeam', hash_bucket_size=1000)
    

    # Create tf.feature_columns for Numerical/Continuous Values

    HS   = tf.feature_column.numeric_column('HS')   # Home Shots
    AS   = tf.feature_column.numeric_column('AS')   # Away Shots
    HST  = tf.feature_column.numeric_column('HST')  # Home Shots on Target
    AST  = tf.feature_column.numeric_column('AST')  # Away Shots on Target
    HF  = tf.feature_column.numeric_column('HF')    # Home Fouls
    AF  = tf.feature_column.numeric_column('AF')    # Away Fouls
    HC  = tf.feature_column.numeric_column('HC')    # Home Corners
    AC  = tf.feature_column.numeric_column('AC')    # Away Corners
    HY  = tf.feature_column.numeric_column('HY')    # Home Yellow Cards
    AY  = tf.feature_column.numeric_column('AY')    # Away Yellow Cards
    HR  = tf.feature_column.numeric_column('HR')    # Home Red Cards
    AR  = tf.feature_column.numeric_column('AR')    # Away Red Cards

    # Compile into one features column
    
    feature_cols = [HomeTeam,AwayTeam,HS,AS,HST,AST,HF,AF,HC,AC,HY,AY,HR,AR]

    

    # Building an input function

    input_fnc = tf.estimator.inputs.pandas_input_fn(x=X_train, y=y_train, batch_size=100, num_epochs=None, shuffle=True)

    # Using Linear Classifier to create a model with tf.Estimator

    model = tf.estimator.LinearClassifier(feature_columns=feature_cols)

    model.train(input_fn=input_fnc, steps=5000)

    return model, X_test, y_test

# Now to make 'predictions'

def predict(data):

    model, X_test, y_test = trainModel(data)

    pred_fn = tf.estimator.inputs.pandas_input_fn(x=X_test, batch_size = len(X_test), shuffle=False)
    predictions = list(model.predict(input_fn=pred_fn))

    print(predictions[0])

    final_preds= []
    for pred in predictions:
        final_preds.append(pred['class_ids'][0])

    print(final_preds[:10])

    # Import Classification report from SkLearn-Metrics to evaluate the performance of the test model

    print(classification_report(y_test, final_preds))
    return final_preds


# Compiling everything into a 'main' function - this is reminiscent of OOP principles, something I'd do in Java - but it's nice to keep things compact, even in Python

def mainP(data):
    return predict(cleanData(data))

# I suppose I could very easily just create one main function and wrap the other 'predict' and 'cleanData' methods into the main function, but I'm still undecided as to whether that is better documentation than splitting it up.

#main('serieA_season-1819.csv')
mainP('serieA/serieeA_season-1718_1819.csv')
#main('serieA_season-1516_1617_1718_1819.csv')

def modelTrain(data):
    return trainModel(cleanData(data))

def modelPred(test, model):
    if (test.shape != (1,14)):
        test = test.reshape(14,)
    test = pd.DataFrame({'HomeTeam': test[0], 'AwayTeam': test[1], 'HS': test[2], 'AS': test[3],'HST': test[4], 'AST': test[5], 'HF': test[6], 'AF': test[7],
    'HC': test[8], 'AC': test[9], 'HY': test[10], 'AY': test[11], 'HR': test[12], 'AR': test[13]}, index=[0])
    pred_fn = tf.estimator.inputs.pandas_input_fn(x=test, batch_size = len(test), shuffle=False)
    predictions = list(model.predict(input_fn=pred_fn))
    if (predictions[0]['class_ids'] == 0):
        return str('Home Team Victory!')
    else:
        return str('Likely a draw or a loss for the home team')

