import copy
import os
import random
import sys

from numpy import Infinity

gameData = {
    "A1": None,
    "A2": None,
    "A3": None,
    "B2": None,
    "B1": None,
    "B3": None,
    "C1": None,
    "C2": None,
    "C3": None,
}

Combinations = [['A1', 'C3', 'C1', 'C2'],['A2','C1','A1', 'A3']]

IAStart = True
IAvsIA = False

startSymbol = "X"

secondSymbol = "O"
if startSymbol == "O":
    secondSymbol = "X"

letters = ["A", "B", "C"]

def checkState(currentGameData = gameData):
    for i in range(3):
        state = True
        playSimbol = currentGameData[letters[i] + "1"]
        for x in range(3):
            if currentGameData[letters[i] + str(x+1)] != playSimbol:
                state = False
                break
        if state:
            return playSimbol
    for i in range(3):
        state = True
        playSimbol = currentGameData["A" + str(i+1)]
        for x in range(3):
            if currentGameData[letters[x] + str(i+1)] != playSimbol:
                state = False
                break
        if state:
            return playSimbol
    for i in range(0,3,2):
        state = True
        playSimbol = currentGameData[letters[i] + "1"]
        if(i == 0):
            for x in range(3):
                if currentGameData[letters[i+x] + str(x+1)] != playSimbol:
                    state = False
                    break
        else:
            for x in range(3):
                if currentGameData[letters[i-x] + str(x+1)] != playSimbol:
                    state = False
                    break
        if state:
            return playSimbol
    if len(getFreeSpaces(currentGameData)) == 0:
        return False
    return None

def getSymbol(letter, number,currentGameData = gameData):
    if (currentGameData[letter + str(number)]) == None:
        return "-"
    return currentGameData[letter + str(number)]


def printGame(currentGameData = gameData):
    os.system('clear')
    print("  1   2   3 ")
    for i in range(3):
        print(letters[i]+" "+getSymbol(letters[i],"1",currentGameData) + " | " + getSymbol(letters[i],"2",currentGameData) + " | " + getSymbol(letters[i],"3",currentGameData))

def getFreeSpaces(gameData):
    spaces = []
    for i in range(0,3):
        for x in range(1,4):
            if gameData[letters[i] + str(x)] == None:
                spaces.append(letters[i] + str(x))
    return spaces

def IAvsIAfun(currentGameData):
    while(checkState(currentGameData) == None):
        printGame(currentGameData)
        print("Player 1")
        if len(getFreeSpaces(currentGameData)) == 9:
            IAPlay = random.choice(getFreeSpaces(currentGameData))
        else :IAPlay = minimax(copy.deepcopy(currentGameData),True,startSymbol)[0]
        currentGameData[IAPlay] = startSymbol
        printGame(currentGameData)
        print("Player 2")
        IAPlay = minimax(copy.deepcopy(currentGameData),True,secondSymbol)[0]
        currentGameData[IAPlay] = secondSymbol
        printGame(currentGameData)
    return checkState(currentGameData)

def minimax(currentGameData,Player,IASymbol):
    #we put the current player at his worst possible score
    #if the IA Win the score is positive
    #if the IA Lose the score is negative
    #so the player want the IA to have a negative score
    if Player: 
        best = [None, -Infinity]
    else:
        best = [None, Infinity]
    if checkState(currentGameData) != None:#if the game is over
        if checkState(currentGameData) == IASymbol:
            return [None, 1]
        elif checkState(currentGameData) != False:
            return [None, -1]
        return [None, 0]
    for space in getFreeSpaces(currentGameData):#for each possible move
        temp = copy.deepcopy(currentGameData)
        if Player:
            temp[space] = IASymbol
        else:
            if IASymbol == "X":
                temp[space] = "O"
            else:
                temp[space] = "X"
        move = minimax(temp,not Player,IASymbol)
        if Player:#if the player is the IA we want the highest score to be played
            if move[1] > best[1]:
                best = [space, move[1]]
        else: #if the player is the other player we want the lowest score to be played
            if move[1] < best[1]:
                best = [space, move[1]]
    return best
        
if not IAvsIA:
    while(checkState() == None):
        printGame()
        print("Player 1")
        if IAStart:
            IAPlay = minimax(copy.deepcopy(gameData),True,startSymbol)[0]
            gameData[IAPlay] = startSymbol
        else:
            play = input("Enter the position: ")
            gameData[play] = startSymbol
        printGame()
        if(checkState() != None):
            break
        print("Player 2")
        if IAStart:
            play = input("Enter the position: ")
            gameData[play] = secondSymbol
        else:
            IAPlay = minimax(copy.deepcopy(gameData),True,secondSymbol)[0]
            gameData[IAPlay] = secondSymbol
        printGame()
        if(checkState() != None):
            break
    print("The winner is: " + str(checkState()))
else:
    value = False
    while(value == False):
        value = IAvsIAfun(copy.deepcopy(gameData))
    print("error")