# Written by Patrick Keener on 11/16/2020
# Video Link:  https://youtu.be/Xjqn4xgg83E
# Honor Statement:  "I have not given or received any unauthorized assistence 
#                    on this assignment"
#
# DSC 430: Python Programming
# Assignment 0902: Game of life
#
# Visualization done using matplotlib Hinton diagram example from the matplotlib 
# example page.  Initial idea from David Warde-Farley on the SciPy Cookbook
# Source:
# https://matplotlib.org/gallery/specialty_plots/hinton_demo.html#sphx-glr-gallery-specialty-plots-hinton-demo-py
#

import numpy as np
import matplotlib.pyplot as plt



# \/\/\/\/\/\/\/\/\/\/  Sourced from matplotlib.org \/\/\/\/\/\/\/\/\/\/

def hinton(matrix, max_weight=None, ax=None):
    """Draw Hinton diagram for visualizing a weight matrix."""
    ax = ax if ax is not None else plt.gca()

    if not max_weight:
        max_weight = 2 ** np.ceil(np.log2(np.abs(matrix).max()))

    ax.patch.set_facecolor('black')
    ax.set_aspect('equal', 'box')
    ax.xaxis.set_major_locator(plt.NullLocator())
    ax.yaxis.set_major_locator(plt.NullLocator())

    for (x, y), w in np.ndenumerate(matrix):
        color = 'white' if w > 0 else 'black'
        size = np.sqrt(abs(w) / max_weight)
        rect = plt.Rectangle([x - size / 2, y - size / 2], size, size,
                             facecolor=color, edgecolor=color)
        ax.add_patch(rect)

    ax.autoscale_view()
    ax.invert_yaxis()

    plt.show()

# /\/\/\/\/\/\/\/\/\/\  Sourced from matplotlib.org /\/\/\/\/\/\/\/\/\/\



def conway(s = 10, p = .1):
    """ Generates a conway board 

    inputs:
    s - an integer representing the length of one side of a square board (ex. 10)
    p - the probability of a 'live' cell
    
    """
    # Use boolean mask on a matrix of ones to return the board
    return (np.ones((s,s)) * [np.random.rand(s,s) < p]).reshape(s,s)


def advance(board, t):
    """
    Advances the conway board 

    inputs:
    b - a conway board (ndarray of 1s and 0s)
    t - number of turns to advance
    """
    
    print("\n\nStarting Board\nWhite is life, black is no life.")
    print(board)
    hinton(board)
    
    for i in range(t): # Number of terms

        board = updateBoard(board)

        plt.pause(0.1)
        print("Board #{}\nWhite is life, black is no life.".format(i+1))
        hinton(board)
        
    print("\n\nFinal Board\nWhite is life, black is no life.")
    print(board)

    return board


def updateBoard(board):
    """ Evalutes the state of the board """
    border = board.shape[0]
    board = board.astype(int)
    newBoard = np.zeros((border, border)).astype(int)
        
    for row in range(border): # iterate through rows
        for column in range(border): # iterate through columns

            # sum the 8 squares surrounding each cell; loop around as needed using modulus
            total = (
                board[row, (column-1)%border] + board[row, (column+1)%border]
                + board[(row-1)%border, column] + board[(row+1)%border, column]
                + board[(row-1)%border, (column-1)%border] + board[(row+1)%border, (column+1)%border]
                + board[(row-1)%border, (column+1)%border] + board[(row+1)%border, (column-1)%border]
            )
            newBoard[row,column] = applyRules(total, board[row,column])
    board = newBoard
    
    return board


def applyRules(total, state):
    """ Applies the rules of the sim """        
    if state == 1:
        if total < 2: return 0 # if 0 or 1: be dead
        if total <= 3: return 1 # if 2 or 3: be alive
        else: return 0 # if 4: be dead
    elif total == 3: return 1 # if 3 and dead: be alive
    else: return 0

    return None


def gameOfLife(s = 10, p = .1, t = 1):
    """ Simulates Conway's Game of Life 
    
    inputs:
    s - an integer representing the length of one side of a square board (ex. 10)
    p - the probability of a 'live' cell
    t - turns to advance
    
    """
    board = conway(s, p).astype(int)
    advance(board, t)

gameOfLife(s = 10, p = .1, t = 1)



# gameOfLife(s = 15, p = .25, t = 5)

# s = 5
# p = .25
# print(np.random.rand(s,s))
# print([np.random.rand(s,s) < p])
# print(np.ones((s,s)))