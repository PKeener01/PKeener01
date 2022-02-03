# Written by Patrick Keener on 11/26/2020
# Video Link:  https://youtu.be/nd2D1IPLTgA
# Honor Statement:  "I have not given or received any unauthorized assistence 
#                    on this assignment"
#
# DSC 430: Python Programming
# Assignment 1002: Crymland Analysis

import os.path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random


# def rename_cols():
    # for file in os.listdir('MC_Run_1'):
    #     filePath = os.path.join('MC_Run_1', file)
    #     df = pd.read_csv(filePath)

#         newCols = {'gangstersNotJailed': 'gangstersNotJailed', 
#         ' gangstersJailed': 'gangstersJailed', 
#         ' mrBiggPersonalWealth': 'mrBiggPersonalWealth',
#         ' bribesAccepted': 'bribesAccepted',
#         ' winner':'winner'}

#         df = df.rename(newCols, axis = 'columns')

#         df.to_csv(filePath)

#     print('Done')

# rename_cols()



def saveAggregates(filePath, df):
    """ saves files to filePath as CSV"""
    df.to_csv(filePath, index = False)

def aggregateResults(inputFile, outputFile):
    """ Aggregate the results into files containing only like-outputs so analysis
     may be conducted 
     """

    df_notJailed = list()
    df_Jailed = list()
    df_biggWealth = list()
    df_bribes = list()
    df_winner = list()
    df_working = list()
    
    for file in os.listdir(inputFile):
        filePath = os.path.join(inputFile, file)
        df_working = pd.read_csv(filePath)

        # Break file into list of lists that will eventually be converted 
        # into a dataframe.  Lists used first so new objects aren't created
        # from every merge.
        df_notJailed.append(df_working['gangstersNotJailed'].tolist())
        df_Jailed.append(df_working['gangstersJailed'].tolist())
        df_biggWealth.append(df_working['mrBiggPersonalWealth'].tolist())
        df_bribes.append(df_working['bribesAccepted'].tolist())
        df_winner.append(df_working['winner'].tolist())

    
    
    # Convert to data frames after aggregation and save to file
    filePath = os.path.join(outputFile, 'notJailed.csv')
    saveAggregates(filePath, pd.DataFrame(df_notJailed))

    filePath = os.path.join(outputFile, 'Jailed.csv')
    saveAggregates(filePath, pd.DataFrame(df_Jailed))

    filePath = os.path.join(outputFile, 'biggWealth.csv')
    saveAggregates(filePath, pd.DataFrame(df_biggWealth))
    
    filePath = os.path.join(outputFile, 'bribes.csv')
    saveAggregates(filePath, pd.DataFrame(df_bribes))

    filePath = os.path.join(outputFile, 'winner.csv')
    saveAggregates(filePath, pd.DataFrame(df_winner))   

    return


def singleLine(subject, mean, stdev, inputFile):
    """ creates a plot with a single line and error bars """
    CI = 2.78 # Corresponds to 95% confidence interval

    # plot initial lines
    plt.plot(mean, color = 'steelblue')
    plt.plot(mean + stdev * CI, color = 'lightsteelblue')
    plt.plot(mean - stdev * CI, color = 'lightsteelblue')

    # add error shading
    plt.fill_between(range(0,500),mean + stdev * CI, mean, color = 'lightsteelblue')
    plt.fill_between(range(0,500),mean - stdev * CI, mean, color = 'lightsteelblue')

    # find max x value ignoring NaN
    maxX = np.nanmax(mean + stdev * CI)*1.0375

    # adjust axis to better fit the chart
    plt.axis([0,500, 0, maxX]) 
    plt.xticks(np.arange(1, 500, 50))

    # add axes lables
    plt.title('Average and 95% Error Bars of ' + subject)
    plt.ylabel(subject)
    plt.xlabel('Week')
    
    # save chart to file
    outfile = os.path.join(inputFile, subject.strip() + '_Avg_95.jpeg')
    plt.savefig(outfile)

    # show & flush the chart
    plt.show()
    

def multipleLines(df, subject, inputFile):
    """ creates a plot with multiple lines """

    # Cycle through each simulation and add line to chart
    for sim in range(len(df)):
        plt.plot(df.iloc[sim])

    # find max x value ignoring NaN
    maxX = np.nanmax(df)*1.0375

    # adjust axis to better fit the chart
    plt.axis([0,500, 0, maxX]) 
    plt.xticks(np.arange(1, 500, 50))

    # add axes lables
    plt.title('Monte Carlo Paths of ' + subject)
    plt.ylabel(subject)
    plt.xlabel('Week')
    
    # save chart to file
    outfile = os.path.join(inputFile, subject.strip() + '_MC.jpeg')
    plt.savefig(outfile)

    # show & flush the chart
    plt.show()


def getStats(df):
    """ Calculate some summary statistics """
    
    mean = df.mean(axis=0, skipna=True)
    stdev = df.std(axis=0, skipna=True)
    return mean, stdev


def visualize(inputFile, fileName, subject):
    """ visualizes the data """

    df = openDF(inputFile, fileName)

    multipleLines(df, subject, inputFile)
    mean, stdev = getStats(df)
    singleLine(subject, mean, stdev, inputFile)


def winChart(detWinVector, inputFile):
    """ Creates a chart of detective wins over time """
    x = np.arange(0, 500, 1)
    plt.fill_between(x,detWinVector,color = 'steelblue')

    # find max x value ignoring NaN
    maxX = np.nanmax(detWinVector)*1.0375

    # adjust axis to better fit the chart
    plt.axis([0,500, 0, maxX]) 
    plt.xticks(np.arange(0, 500, 50))

    # add axes lables
    plt.title('Detective Wins by Week')
    plt.ylabel('Detective Wins')
    plt.xlabel('Week')
    
    # save chart to file
    outfile = os.path.join(inputFile, 'DetectiveWins.jpeg')
    plt.savefig(outfile)

    # show & flush the chart
    plt.show()


def winComparison(biggWins, detWins, inputFile):
    """ Creates a bar chart comparing absolute number of mr bigg and detective wins """
    
    winList = [biggWins, detWins]
    
    x = np.arange(1,3)
    width = 0.25

    plt.bar(.5, biggWins, width, label='Mr. Bigg')    
    plt.bar(1.5, detWins, width, label='Detectives')

    # find max x value ignoring NaN
    maxX = max(biggWins, detWins)*1.0375

    # adjust axis to better fit the chart
    plt.axis([0,2, 0, maxX]) 
    plt.xticks(np.arange(0, 2, 1))

    # add axes lables
    plt.title('Mr Bigg vs Detective Wins by Week')
    plt.ylabel('Wins')

    # add legend
    plt.legend()
    
    # save chart to file
    outfile = os.path.join(inputFile, 'winComparison.jpeg')
    plt.savefig(outfile)

    # show & flush the chart
    plt.show()



def getWinStats(df):
    """ get win stats """

    detWins = abs(int(np.nansum(df[df == 1])))
    biggWins = abs(int(np.nansum(df[df == -1])))
    
    p_Det = detWins/(detWins+biggWins)
    p_MrBigg = 1-p_Det

    detWinVector = df.sum()
    detWinVector[-1] = biggWins + detWinVector[-1] # adjust for Mr Bigg wins

    return round(p_MrBigg, 4), biggWins, round(p_Det, 4), detWins, detWinVector


def visualizeWins(inputFile, fileName):
    """ This functions visualizes the winner """

    df = openDF(inputFile, fileName)

    # replace outcomes with digits for counting
    df.replace({' detectives': 1, ' mrBigg': -1, ' ongoing': 0}, inplace = True)

    p_MrBigg, biggWins, p_Det, detWins, detWinVector = getWinStats(df)

    winChart(detWinVector, inputFile) # Generate time series chart of wins
    winComparison(biggWins, detWins, inputFile) # Generate comparison of wins

# Generates a tuple of random numbers between 0 and 1 to be used for random colors
# for the graphs
def genRandomColor(): return (random.random(), random.random(), random.random())


def openDF(inputFile, fileName):
    """ opens file as  a csv """

    filePath = os.path.join(inputFile, fileName)
    df = pd.read_csv(filePath)
    return df

def visualizeResults(outputFile):
    """ Visualization for the results """

    visualize(outputFile, 'notJailed.csv', 'Active Criminals')
    visualize(outputFile, 'Jailed.csv', 'Jailed Criminals')
    visualize(outputFile, 'biggWealth.csv', "Mr Bigg's Wealth")
    visualize(outputFile, 'bribes.csv', 'Bribes Accepted')
    visualizeWins(outputFile, 'winner.csv')


def analysis():
    inputFile = 'MC_Run_1\\'
    # inputFile = 'outputs\\'
    outputFile = 'aggregatedDS\\'

    # aggregateResults(inputFile, outputFile)

    visualizeResults(outputFile)


    print('Fin.')



analysis()