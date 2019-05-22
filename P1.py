from riskStructs import *
import random

def getPlayerCountryList(player, countryD):
    countryList = []
    for countryKey in countryD:
        if countryD[countryKey]["owner"] == player:
            countryList.append(countryKey)
    
    return countryList

def atLeastOneAdjacentEnemy(countryKey, player, countryD):
    atLeastOne = False
    for each in adjacentCountriesD[countryKey]:
        if countryD[each]["owner"] != player:
            atLeastOne = True
    
    return atLeastOne

def hasPickedABook(playerD, player, indexList):
    artCount = 0
    infCount = 0
    cavCount = 0
    wildCount = 0
    if len(indexList) < 3:
        return False
    cards = []
    for idx in indexList:
        cards.append(playerD[player]["cards"][idx])
    for card in cards:
        if card[1] == "artillery":
            artCount += 1
        elif card[1] == "infantry":
            infCount += 1
        elif card[1] == "cavalry":
            cavCount += 1
        else:
            wildCount += 1

    # Check for three of a kind
    if artCount >= 3 or infCount >= 3 or cavCount >= 3:
        return True
    if artCount >= 1 and infCount >= 1 and cavCount >= 1:
        return True
    if wildCount >= 1:
        return True
    
    return False

def attackFromCountry(player, countryD, bookArmiesBonusList, playerDMe, manual = True):
    countryList = []
    countList = []
    for countryKey in countryD:
        if countryD[countryKey]["owner"] == player and countryD[countryKey]["armies"] >= 2:
            if atLeastOneAdjacentEnemy(countryKey, player, countryD):
                countryList.append(countryKey)
                countList.append(countryD[countryKey]["armies"])
    
    if manual:
        if countryList == []:
            return "NO ATTACK"
        print("0. NO ATTACK")
        for i in range(1, len(countryList)+1):
            print(str(i) + "." + countryList[i-1])
        choice = -1
        while choice < 0 or choice>len(countryList):
            choice = input("From which country would you like to attack? => ")
            if choice == "":
                choice = 1
            elif choice.isnumeric() and int(choice) >= 1:
                choice = int(choice)
            else:
                choice = 0
        if choice == 0:
            return "NO ATTACK"
        else:
            return countryList[choice-1]
    else:
        if countryList == []:
            return "NO ATTACK"
        elif len(countryList) == 1:
            return countryList[0]
        else:
            for country in range(len(countryList)):
                for nextCountry in range(country+1, len(countryList)):
                    if nextCountry>country:
                        return countryList[nextCountry]
                    else:
                        return countryList[country]

def attackToCountry(player, countryD, bookArmiesBonusList, playerDMe, attackFromCountry, manual = True):
    # given the country attacking from
    # get the list of attached countries
    possiblesList = []
    for eachCountry in adjacentCountriesD[attackFromCountry]:
        if countryD[eachCountry]["owner"] != player:
            possiblesList.append(eachCountry)
    if manual: #MANUAL
        for index in range(len(possiblesList)):
            print(str(index)+".", possiblesList[index])
        choice = -1
        while choice < 0 or choice >= len(possiblesList):
            choice = input("Which country would you like to attack? => ")
            if choice.isnumeric():
                choice = int(choice)
            else:
                choice = 0
        return possiblesList[choice], countryD[possiblesList[choice]]["owner"]
    else: # AUTOMATIC
        randNum = random.randint(0, len(possiblesList)-1)
        if len(possiblesList)>1:
            for country in range(len(possiblesList)):
                for nextCountry in range(country+1, len(possiblesList)):
                    if nextCountry < country:
                        return possiblesList[nextCountry], countryD[possiblesList[nextCountry]]["owner"]
                    else:
                        return possiblesList[country], countryD[possiblesList[country]]["owner"]
        else:
            return possiblesList[randNum], countryD[possiblesList[randNum]]["owner"]

def continueAttack(player, countryD, bookArmiesBonusList, playerDMe, manual = True):
    if manual: # MANUAL
        return(input("Attack again? (Enter to attack, RETREAT and enter to end attack) => "))
    else: # AUTOMATIC
        return ""
        
def getBookCardIndices(player, countryD, bookArmiesBonusList, playerDMe, manual = True):
    # print("IN PLAYER", player)
    listOfCardIndicesToPlay = []
    if manual: # MANUAL
        while not hasPickedABook(playerDMe, player, listOfCardIndicesToPlay):
            idx = 0
            for card in playerDMe[player]["cards"]:
                print(str(idx)+".", card)
                idx += 1
            print(str(idx)+".", "DO NOT play a book")
            for i in range(3):
                answer = "-1"
                while int(answer) < 0 or int(answer)>idx or int(answer) in listOfCardIndicesToPlay:
                    answer = input("Play card => ")
                if int(answer) == idx:
                    return []
                else:
                    listOfCardIndicesToPlay.append(int(answer))
            if not hasPickedABook(playerDMe, player, listOfCardIndicesToPlay):
                listOfCardIndicesToPlay = []
    else: # AUTOMATIC
        listOfCardIndicesToPlay = []
        while not hasPickedABook(playerDMe, player, listOfCardIndicesToPlay):
            listOfCardIndicesToPlay = []
            listOfIndices = list(range(len(playerDMe[player]["cards"])))
            for i in range(3):
                listOfCardIndicesToPlay.append(listOfIndices.pop(random.randrange(0, len(listOfIndices))))
    return listOfCardIndicesToPlay

def tookCountryMoveArmiesHowMany(player, countryD, bookArmiesBonusList, playerDMe, attackFrom, manual = True):
    if manual: # MANUAL
        howManyToMove = input("\nHow many of the " + str(countryD[attackFrom]["armies"]-1) + " armies would you like to move? => ")
        if howManyToMove == "":
            howManyToMove = countryD[attackFrom]["armies"]-1
        else:
            howManyToMove = int(howManyToMove)
        while howManyToMove < 1 or howManyToMove>countryD[attackFrom]["armies"]-1:
            print("Invalid number of armies to move!!")
            howManyToMove = input("How many of the " + str(countryD[attackFrom]["armies"]-1) + " armies would you like to move? => ")
            if howManyToMove == "":
                howManyToMove = countryD[attackFrom]["armies"]-1
            else:
                howManyToMove = int(howManyToMove)
    else: # AUTOMATIC
        howManyToMove = (countryD[attackFrom]["armies"]-1)
        if howManyToMove == 2:
            howManyToMove = 1
        else:
            if howManyToMove%2 == 0:
                howManyToMove = howManyToMove//2
            elif howManyToMove%2 == 1:
                howManyToMove = (howManyToMove-1)//2
        if howManyToMove == 0:
            howManyToMove = 1
    return howManyToMove

def troopMove(player, countryD, bookArmiesBonusList, playerDMe, manual = True):
    fromCountry = ""
    toCountry = ""
    howManyToMove = 0
    if manual: # MANUAL
        troopMovementCandidateFromList = []
        for countryKey in countryD:
            if countryD[countryKey]["owner"] == player and countryD[countryKey]["armies"] > 1:
                for eachCountry in adjacentCountriesD[countryKey]:
                    if countryD[eachCountry]["owner"] == player:
                        if countryKey not in troopMovementCandidateFromList:
                            troopMovementCandidateFromList.append(countryKey)
        print("0. NO TROOP MOVEMENT")
        for idx in range(0, len(troopMovementCandidateFromList)):
            print(str(idx+1)+". "+ troopMovementCandidateFromList[idx])
        fromChoice = -1
        while fromChoice < 0 or fromChoice>len(troopMovementCandidateFromList):
            fromChoice = input("Troop Movement From? ")
            if fromChoice.isnumeric() and fromChoice != "0":
                fromChoice = int(fromChoice)-1
            elif fromChoice == "":
                return "", "", 0
            else:
                return "", "", 0
        fromCountry = troopMovementCandidateFromList[fromChoice]
        troopMovementCandidateToList = []
        for each in adjacentCountriesD[troopMovementCandidateFromList[fromChoice]]:
            if countryD[each]["owner"] == player:
                troopMovementCandidateToList.append(each)
        for idx in range(0, len(troopMovementCandidateToList)):
            print(str(idx)+". "+ troopMovementCandidateToList[idx])
        toChoice = -1
        while toChoice < 0 or toChoice>len(troopMovementCandidateToList):
            toChoice = input("Troop Movement TO? ")
            if toChoice.isnumeric():
                toChoice = int(toChoice)-1
            elif toChoice == "":
                toChoice = 0
            else:
                return "", "", 0
        toCountry = troopMovementCandidateToList[toChoice]
        howManyToMove = -1
        while howManyToMove < 0 or howManyToMove>countryD[troopMovementCandidateFromList[fromChoice]]["armies"]-1:
            howManyToMove = input("\nHow many of the " + str(countryD[fromCountry]["armies"]-1) + " armies would you like to move? => ")
            if howManyToMove.isnumeric():
                howManyToMove = int(howManyToMove)
            else:
                howManyToMove = countryD[troopMovementCandidateFromList[fromChoice]]["armies"]-1
    else: # AUTOMATIC
        troopMovementCandidateFromList = []
        for countryKey in countryD:
            if countryD[countryKey]["owner"] == player and countryD[countryKey]["armies"]>1:
                for eachCountry in adjacentCountriesD[countryKey]:
                    if countryD[eachCountry]["owner"] == player:
                        if countryKey not in troopMovementCandidateFromList:
                            troopMovementCandidateFromList.append(countryKey)
        if len(troopMovementCandidateFromList) == 0:
            return "", "", 0
        elif (len(troopMovementCandidateFromList)-1) == 0:
            return "", "", 0
        elif (len(troopMovementCandidateFromList)-1) <= 2:
            fromChoice = 0
        else:
            fromChoice = random.randint(0, len(troopMovementCandidateFromList)-1)
        fromCountry = troopMovementCandidateFromList[fromChoice]
        troopMovementCandidateToList = []
        for each in adjacentCountriesD[fromCountry]:
            if countryD[each]["owner"] == player:
                troopMovementCandidateToList.append(each)
        if (len(troopMovementCandidateToList)-1) <= 1:
            toChoice = 0
        else:
            toChoice = random.randint(0, len(troopMovementCandidateToList)-1)
        toCountry = troopMovementCandidateToList[toChoice]
        howManyToMove = (countryD[fromCountry]["armies"]-1)//2
        if howManyToMove == 1:
            howManyToMove = 0
        pass
    return fromCountry, toCountry, howManyToMove

def placeArmies(player, countryD, bookArmiesBonusList, playerDMe, manual = True):
    # print("PLAYER:", player)
    countryList = getPlayerCountryList(player, countryD)
    if manual: # MANUAL
        for index in range(len(countryList)):
            print(index, countryList[index])
        countryIndex = -1
        while countryIndex < 0 or countryIndex >= len(countryList):
            valIn = input("Player "+str(player)+", WHERE do you wish to place armies? => ")
            if valIn == "":
                countryIndex = 0
            elif valIn.isnumeric():
                countryIndex = int(valIn)
            else:
                countryIndex = 0
        numberOfArmiesToPlace = -1
        while numberOfArmiesToPlace < 1 or numberOfArmiesToPlace>playerDMe[player]["armies"]:
            valIn = input("HOW MANY of the " + str(playerDMe[player]["armies"]) + " armies do you wish to place in " + countryList[countryIndex] + " => ")
            if valIn == "":
                numberOfArmiesToPlace = playerDMe[player]["armies"]
            elif valIn.isnumeric():
                numberOfArmiesToPlace = int(valIn)
            else:
                numberOfArmiesToPlace = 0
    else: # AUTOMATIC
        countryIndex = random.randint(0, len(countryList)-1)
        numberOfArmiesToPlace = playerDMe[player]["armies"]
    return countryList[countryIndex], numberOfArmiesToPlace
