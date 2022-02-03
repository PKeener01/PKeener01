# Written by Patrick Keener on 10/10/2020
# Video Link: https://youtu.be/sKIO0GYnyw0
# Honor Statement:  "I have not given or received any unauthorized assistence 
#                    on this assignment"
#
# Checks:
# 1. [x] Docstrings for all functions
# 2. [x] All requirements met
# 3. [x] Fully tested
#
# Requirements:
# 1. [x] Recursive function - def humanPyreamid(row, columns)
#        Takes as input the row & column of person
# 2. [x] Make this interactive!!!
# 3. [x] Returns total weight on person's back (excludes their own)
# 4. [x] Row & column are 0-indexed (0,0 = top)
# 5. [x] NO LOOPS
#
# Notes:
# Bottom row is base case
# Everyone weighs 128 lbs (2^7)

def pyramidCalc(row, column):
    """ This program calculates the weight on the shoulders of the person
    at the nth position in the human pyramid """

    if row == 0:  # base Case- the dude or duddette at the top
        return 0

    elif column == 0: # edge case- left side
        person1 = (128 + pyramidCalc(row-1, column))/2
        return person1

    elif column == row: # edge case- right side
        person1 = (128 + pyramidCalc(row-1, column-1))/2
        return person1

    else:
        # include own weight and the weight of each individual
        Self = 128
        person1 = (pyramidCalc(row-1, column-1))/2
        person2 = (pyramidCalc(row-1, column))/2 
        return person1 + person2 + Self

    return None


def pyramidInput():
    """ Gets input from users"""

    print('Welcome to the pyramid weight calculator written by P. Keener')
    row = int(input('Please input the row of the participant you\'d like to check'))
    column = int(input('Please input the column of the participant you\'d like to check'))
    
    return row, column

def humanPyramid():
    """ Main controlling function for the human pyramid weight calculator"""

    row, column = pyramidInput() # get user inputs
    weight = pyramidCalc(row, column) # find the weight
    print('The weight of the individual in position ({}, {}) is {}!'\
        .format(row, column, weight))

    return None

humanPyramid()