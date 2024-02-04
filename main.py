import copy
import os
import time

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

IAStart = False
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

def getCross(gameData):
    count = 0
    for i in range(0,3):
        for x in range(1,4):
            if gameData[letters[i] + str(x)] == "X":
                count += 1
    return count

def getCircle(gameData):
    count = 0
    for i in range(0,3):
        for x in range(1,4):
            if gameData[letters[i] + str(x)] == "O":
                count += 1
    return count

def getFreeSpaces(gameData):
    spaces = []
    for i in range(0,3):
        for x in range(1,4):
            if gameData[letters[i] + str(x)] == None:
                spaces.append(letters[i] + str(x))
    return spaces

def getStartSymbol(gameData):
    if startSymbol == "O":
        return getCircle(gameData)
    return getCross(gameData)

def getSecondSymbol(gameData):
    if startSymbol == "O":
        return getCross(gameData)
    return getCircle(gameData)

def IAvsIAfun(currentGameData):
    while(checkState(currentGameData) == None):
        printGame(currentGameData)
        print("Player 1")
        IAPlay = getIAPlay(copy.deepcopy(currentGameData),True,startSymbol)
        currentGameData[IAPlay] = startSymbol
        printGame(currentGameData)
        print("Player 2")
        IAPlay = getIAPlay(copy.deepcopy(currentGameData),True,secondSymbol)
        currentGameData[IAPlay] = secondSymbol
        printGame(currentGameData)
    print("The winner is: " + str(checkState(currentGameData)))

def getIAPlay(currentGameData,iteration,IASymbol):
    play = ""
    otherSymbol = "O"
    if IASymbol == "O":
        otherSymbol = "X"
    if getStartSymbol(currentGameData) > getSecondSymbol(currentGameData):
        play = secondSymbol
    else:
        play = startSymbol
    freeSpaces = getFreeSpaces(currentGameData)
    state = checkState(currentGameData)
    if state == IASymbol:
        return 2
    elif state == otherSymbol:
        return -2
    if len(freeSpaces) == 0:
        return 1
    playEnd = {}
    
    for space in freeSpaces:
        newGameData = copy.deepcopy(currentGameData)
        newGameData[space] = play
        playEnd[space] = getIAPlay(newGameData,False,IASymbol)

    result = sum(playEnd.values())
    if not iteration:
        return result
    finalPlay = ""
    print(playEnd)
    for i in playEnd:
        print(i)
        if finalPlay == "":
            finalPlay = i
        else:
            if playEnd[i] > playEnd[finalPlay]:
                finalPlay = i
    return finalPlay

if not IAvsIA:
    while(checkState() == None):
        printGame()
        print("Player 1")
        if IAStart:
            IAPlay = getIAPlay(gameData,True,startSymbol)
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
            IAPlay = getIAPlay(gameData,True,secondSymbol)
            gameData[IAPlay] = secondSymbol
        if(checkState() != None):
            break
    print("The winner is: " + str(checkState()))
else:
    while(True):
        IAvsIAfun(copy.deepcopy(gameData))