from riskStructs import *
import random

# Get list of countries that the player owns
def getPlayerCountryList(player):
    countryList = []
    for countryKey in countryD:
        if countryD[countryKey]["owner"] == player:
            countryList.append(countryKey)
    
    return countryList

# Determine if there is an enemy adjacent to a player's country
def atLeastOneAdjacentEnemy(countryKey, player):
    atLeastOne = False
    for each in adjacentCountriesD[countryKey]:
        if countryD[each]["owner"] != player:
            atLeastOne = True
    
    return atLeastOne

# Determine if a player has a book
def hasPickedABook(playerD, player, indexList):
    if len(indexList) < 3:
        return False

    # Convert indexes to cards
    cards = []
    for idx in indexList:
        cards.append(playerD[player]["cards"][idx])
    
    artCount = 0
    infCount = 0
    cavCount = 0
    wildCount = 0
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

def attackFromCountry(player, manual):
    # Build list of countries to attack from
    countryList = []
    for countryKey in countryD:
        if countryD[countryKey]["owner"] == player and countryD[countryKey]["armies"] >= 2:
            if atLeastOneAdjacentEnemy(countryKey, player):
                countryList.append(countryKey)
    
    if countryList == []:
        return "NO ATTACK"

    if manual:
        # List choices
        print("0. NO ATTACK")
        for i in range(1, len(countryList) + 1):
            print(str(i) + ". " + countryList[i - 1])
        
        # Get player choice
        choice = -1
        while choice < 0 or choice > len(countryList):
            choice = input("From which country would you like to attack? => ")
            # Default first country in list
            if choice == "":
                choice = 1
            elif choice.isnumeric() and int(choice) >= 1:
                choice = int(choice)
            else:
                choice = 0
        
        if choice == 0:
            return "NO ATTACK"
        else:
            return countryList[choice - 1]
    
    # AUTOMATIC
    else:
        if len(countryList) == 1:
            return countryList[0]
        else:
            # Determine country with largest number of armies
            maxArmies = ""
            for country in range(1, len(countryList)):
                if countryD[countryList[country]]["armies"] > countryD[countryList[country - 1]]["armies"]:
                    maxArmies = countryList[country]
                else:
                    maxArmies = countryList[country - 1]
            
            return maxArmies

# Determine which country to attack
def attackToCountry(player, attackFromCountry, manual):
    # Get list of possible targets
    possiblesList = []
    for eachCountry in adjacentCountriesD[attackFromCountry]:
        if countryD[eachCountry]["owner"] != player:
            possiblesList.append(eachCountry)
    
    if manual:
        # List possible targets
        for index in range(len(possiblesList)):
            print(str(index) + ". ", possiblesList[index])
        
        # Get player choice
        choice = -1
        while choice < 0 or choice >= len(possiblesList):
            choice = input("Which country would you like to attack? => ")
            if choice.isnumeric():
                choice = int(choice)
            else:
                choice = 0
        
        return possiblesList[choice], countryD[possiblesList[choice]]["owner"]
    
    # AUTOMATIC
    else:
        if len(possiblesList) == 1:
            return possiblesList[0], countryD[possiblesList[0]]["owner"]
        else:
            minArmies = ""
            for country in range(1, len(possiblesList)):
                if countryD[possiblesList[country]]["armies"] < countryD[possiblesList[country - 1]]["armies"]:
                    minArmies = possiblesList[country]
                else:
                    minArmies = possiblesList[country - 1]
            
            return minArmies, countryD[minArmies]["owner"]

# Determine if a player wants to attack again
def continueAttack(attackToArmies, attackFromArmies, manual):
    if manual:
        ret = (input("Attack again? (Enter to attack, RETREAT and enter to end attack) => "))
    
    # AUTOMATIC
    else:
        # Only attack if player has more than 2 armies above the other player
        if attackToArmies != 0 and attackFromArmies - attackToArmies <= 3:
            ret = "RETREAT"
        else:
            ret = ""

    return ret

# Get book indices to play
def getBookCardIndices(player, playerDMe, manual):
    print("IN PLAYER", player)
    listOfCardIndicesToPlay = []
    if manual:
        while not hasPickedABook(playerDMe, player, listOfCardIndicesToPlay):
            # List choices
            idx = 0
            for card in playerDMe[player]["cards"]:
                print(str(idx) + ". ", card)
                idx += 1
            print(str(idx) + ". ", "DO NOT play a book")
            
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
    else:
        listOfCardIndicesToPlay = []
        while not hasPickedABook(playerDMe, player, listOfCardIndicesToPlay):
            listOfCardIndicesToPlay = []
            listOfIndices = list(range(len(playerDMe[player]["cards"])))
            for i in range(3):
                listOfCardIndicesToPlay.append(listOfIndices.pop(random.randrange(0, len(listOfIndices))))
    
    return listOfCardIndicesToPlay

# Determine how many armies to move into the captured country
def tookCountryMoveArmiesHowMany(attackFrom, manual):
    if manual:
        howManyToMove = input("\nHow many of the " + str(countryD[attackFrom]["armies"] - 1) + " armies would you like to move? => ")
        # Move all armies by default
        if howManyToMove == "":
            howManyToMove = countryD[attackFrom]["armies"] - 1
        else:
            howManyToMove = int(howManyToMove)
    
    # AUTOMATIC
    else:
        # Always move half the armies
        if countryD[attackFrom]["armies"] == 0:
            howManyToMove = 1
        else:
            howManyToMove = (countryD[attackFrom]["armies"] - 1) // 2
            if howManyToMove == 0:
                howManyToMove = 1
    
    return howManyToMove

# Determine how many armies to move during troop movement phase
def troopMove(player, manual):
    if manual:
        troopMovementCandidateFromList = []
        for countryKey in countryD:
            if countryD[countryKey]["owner"] == player and countryD[countryKey]["armies"] > 1:
                for eachCountry in adjacentCountriesD[countryKey]:
                    if countryD[eachCountry]["owner"] == player:
                        if countryKey not in troopMovementCandidateFromList:
                            troopMovementCandidateFromList.append(countryKey)
        
        # List choices to move armies from
        print("0. NO TROOP MOVEMENT")
        for idx in range(0, len(troopMovementCandidateFromList)):
            print(str(idx + 1) + ". "+ troopMovementCandidateFromList[idx])
        
        # Determine player choice
        fromChoice = -1
        while fromChoice < 0 or fromChoice > len(troopMovementCandidateFromList):
            fromChoice = input("Troop Movement From? ")
            if fromChoice.isnumeric() and fromChoice != "0":
                fromChoice = int(fromChoice) - 1
            elif fromChoice == "":
                return "", "", 0
            # Default is no movement
            else:
                return "", "", 0

        fromCountry = troopMovementCandidateFromList[fromChoice]
        
        # List choices to move armies to
        troopMovementCandidateToList = []
        for each in adjacentCountriesD[troopMovementCandidateFromList[fromChoice]]:
            if countryD[each]["owner"] == player:
                troopMovementCandidateToList.append(each)

        # List choices
        for idx in range(0, len(troopMovementCandidateToList)):
            print(str(idx) + ". " + troopMovementCandidateToList[idx])
        
        # Determine player choice
        toChoice = -1
        while toChoice < 0 or toChoice > len(troopMovementCandidateToList):
            toChoice = input("Troop Movement TO? ")
            if toChoice.isnumeric():
                toChoice = int(toChoice) - 1
            elif toChoice == "":
                toChoice = 0
            else:
                return "", "", 0

        toCountry = troopMovementCandidateToList[toChoice]
        howManyToMove = -1
        while howManyToMove < 0 or howManyToMove > countryD[troopMovementCandidateFromList[fromChoice]]["armies"] - 1:
            howManyToMove = input("\nHow many of the " + str(countryD[fromCountry]["armies"] - 1) + " armies would you like to move? => ")
            if howManyToMove.isnumeric():
                howManyToMove = int(howManyToMove)
            else:
                howManyToMove = countryD[troopMovementCandidateFromList[fromChoice]]["armies"] - 1
    
    # AUTOMATIC
    else:
        # Build list to determine where to move armies from
        troopMovementCandidateFromList = []
        for countryKey in countryD:
            if countryD[countryKey]["owner"] == player and countryD[countryKey]["armies"] > 1:
                for eachCountry in adjacentCountriesD[countryKey]:
                    if countryD[eachCountry]["owner"] == player:
                        if countryKey not in troopMovementCandidateFromList:
                            troopMovementCandidateFromList.append(countryKey)

        # If we can't move any extra armies
        if len(troopMovementCandidateFromList) == 0 or len(troopMovementCandidateFromList) == 1:
            return "", "", 0
        
        # Determine which player's countries have the largest army
        maxArmiesFrom = ""
        for country in range(1, len(troopMovementCandidateFromList)):
            if countryD[troopMovementCandidateFromList[country]]["armies"] > countryD[troopMovementCandidateFromList[country - 1]]["armies"]:
                maxArmiesFrom = troopMovementCandidateFromList[country]
            else:
                maxArmiesFrom = troopMovementCandidateFromList[country - 1]

        # Build list to determine where to move armies to
        troopMovementCandidateToList = []
        for each in adjacentCountriesD[maxArmiesFrom]:
            if countryD[each]["owner"] == player:
                troopMovementCandidateToList.append(each)

        if len(troopMovementCandidateToList) == 0:
            return "", "", 0

        # Determine where to move armies to
        minArmies = ""
        for country in range(1, len(troopMovementCandidateToList)):
            if countryD[troopMovementCandidateToList[country]]["armies"] < countryD[troopMovementCandidateToList[country - 1]]["armies"]:
                minArmies = troopMovementCandidateToList[country]
            else:
                minArmies = troopMovementCandidateToList[country - 1]

        howManyToMove = (countryD[maxArmiesFrom]["armies"] - 1) // 2
        if howManyToMove == 1:
            howManyToMove = 0

    return maxArmiesFrom, minArmies, howManyToMove

# Determine where and how many armies to place
def placeArmies(player, playerDMe, manual):
    countryList = getPlayerCountryList(player)
    
    if manual:
        # List choices
        for index in range(len(countryList)):
            print(str(index) + ". " + countryList[index])

        # Determine player country choice 
        countryIndex = -1
        while countryIndex < 0 or countryIndex >= len(countryList):
            valIn = input("Player " + str(player) + ", WHERE do you wish to place armies? => ")
            if valIn == "":
                countryIndex = 0
            elif valIn.isnumeric():
                countryIndex = int(valIn)
            else:
                countryIndex = 0
        
        # Determine player army count choice
        numberOfArmiesToPlace = -1
        while numberOfArmiesToPlace < 1 or numberOfArmiesToPlace > playerDMe[player]["armies"]:
            valIn = input("HOW MANY of the " + str(playerDMe[player]["armies"]) + " armies do you wish to place in " + countryList[countryIndex] + " => ")
            if valIn == "":
                numberOfArmiesToPlace = playerDMe[player]["armies"]
            elif valIn.isnumeric():
                numberOfArmiesToPlace = int(valIn)
            else:
                numberOfArmiesToPlace = 0
    
    # AUTOMATIC
    else:
        # Randomly pick a country to place all armies
        numberOfArmiesToPlace = playerDMe[player]["armies"]
        countryIndex = random.randint(0, len(countryList) - 1)
    
    return countryList[countryIndex], numberOfArmiesToPlace
