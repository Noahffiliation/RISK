import turtle
import time
import random
from riskStructs import *
import P1
import P2
import P3
import P4

# Struct for player information
playerD = {1: {"armies": 30, "color": 'green', "loc": (-350, 257), "cards": []},
           2: {"armies": 30, "color": 'blue', "loc": (220, 257), "cards": []},
           3: {"armies": 30, "color": 'purple', "loc": (220, -289), "cards": []},
           4: {"armies": 30, "color": 'red', "loc": (-350, -289), "cards": []}}

# Automatic game or not
manual = False

# Bonus army counts
bookArmiesBonusList = [4, 6, 8, 10, 12, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]

# Draw a rectangle
def drawRectangle(t, x, y, width, height, text, fontSize, fontColor, offSet):
    t.up()
    t.goto(x, y)
    t.down()
    t.fillcolor("white")
    t.begin_fill()
    for i in range(2):
        t.forward(width)
        t.right(90)
        t.forward(height)
        t.right(90)
    t.end_fill()
    if text != "":
        t.up()
        t.goto(x + 5, y - height + offSet)
        t.color(fontColor)
        t.write(text, font = ('Arial', fontSize, 'bold'))
    t.down()

# Draw army count boxes for each player
def drawPlayerBoxes(t, text, whichOnes):
    for i in whichOnes:
        t.color(playerD[i]["color"])
        t.up()
        t.goto(playerD[i]["loc"])
        t.write("PLAYER " + str(i), font = ('Arial', 18, 'bold'))
        drawRectangle(t, playerD[i]["loc"][0] + 120, playerD[i]["loc"][1] + 30, 62, 30, text, 18, playerD[i]["color"], 0)

    t.color("black")

# Randomly assign countries to players
def autoAssignCountries(t, player):
    countryList = list(countryD.keys())
    while len(countryList) > 0:
        # Randomly assign a country to player and place army
        country = countryList.pop(random.randrange(0, len(countryList)))
        countryD[country]["owner"] = player
        countryD[country]["armies"] = 1
        playerD[player]["armies"] -= 1

        # Draw updates
        drawPlayerBoxes(t, str(playerD[player]["armies"]), [player])
        drawRectangle(t, countryD[country]["loc"][0], countryD[country]["loc"][1], 31, 15, "1", 12, playerD[player]["color"], -3)

        # Rotate to next player
        player = nextPlayer(player)

    return player

# Create card book for military units
def createCards(countryD):
    countryList = list(countryD.keys())
    cardList = []

    # Add two wild cards into the deck
    card = ["wild", "wild"]
    cardList.append(card)
    cardList.append(card)

    # Add units into deck
    for i in range(14):
        card = [countryList.pop(), "artillery"]
        cardList.append(card)

    for i in range(14):
        card = [countryList.pop(), "cavalry"]
        cardList.append(card)

    for i in range(14):
        card = [countryList.pop(), "infantry"]
        cardList.append(card)
    
    random.shuffle(cardList)

    return cardList

# Determine if players still have armies to place
def stillArmiesToPlace(player):
    return playerD[player]["armies"] > 0

# Get list of countries the player owns
def getPlayerCountryList(player):
    countryList = []
    for countryKey in countryD:
        if countryD[countryKey]["owner"] == player:
            countryList.append(countryKey)
    
    return countryList

# Place armies in a country
def armyPlacement(player, t):
    country, numberOfArmiesToPlace = eval("P" + str(player)).placeArmies(player, playerD, manual)
    countryD[country]["armies"] = countryD[country]["armies"] + numberOfArmiesToPlace
    playerD[player]["armies"] = playerD[player]["armies"] - numberOfArmiesToPlace

    print("\nPLAYER", player, "placing", numberOfArmiesToPlace, "armies", "\n")
    
    # Draw updates
    drawRectangle(t, countryD[country]["loc"][0], countryD[country]["loc"][1], 31, 15, countryD[country]["armies"], 12, playerD[player]["color"], -3)
    drawPlayerBoxes(t, str(playerD[player]["armies"]), [player])

# Rotate to the next player
def nextPlayer(player):
    player += 1
    if player == 5:
        player = 1
    
    return player

# Determine if a player owns every country
def gameOver():
    winnerList = []
    for key in countryD:
        winnerList.append(countryD[key]["owner"])
    
    return winnerList.count(winnerList[0]) == len(winnerList)

# Calculate base army count
def calcBaseArmiesBeginningOfTurn(player):
    count = 0
    for key in countryD:
        if countryD[key]["owner"] == player:
            count += 1

    # Return minimum base of 3 armies
    return max(3, count // 3)

# Determine continent bonus armies
def findContinentsBonusBeginningOfTurn(player):
    continentBonusTotal = 0
    countryList = getPlayerCountryList(player)
    for eachContinentKey in continentD:
        ownsContinent = True
        for eachCountry in continentD[eachContinentKey]:
            if eachCountry not in countryList:
                ownsContinent = False

        if ownsContinent:
            continentBonusTotal += armiesPerContinentD[eachContinentKey]

    return continentBonusTotal

# Pick a country to attack
def pickAttackTo(country, player):
    return eval("P" + str(player)).attackToCountry(player, country, manual)

# Draw the dice
def drawDice(t, aDice, dDice):
    t.up()
    
    x = -80
    y = 300
    for die in aDice:
        drawRectangle(t, x, y, 40, 40, die, 26, "black", 0)
        x = x + 50

    x = -80
    y = 250
    for die in dDice:
        drawRectangle(t, x, y, 40, 40, die, 26, "black", 0)
        x = x + 50
    
    # Determine armies lost
    attackIncrement = 0
    defendIncrement = 0
    if aDice[0] > dDice[0]:
        defendIncrement -= 1
    else:
        attackIncrement -= 1

    if len(dDice) == 2 and len(aDice) > 1:
        if aDice[1] > dDice[1]:
            defendIncrement -= 1
        else:
            attackIncrement -= 1

    return attackIncrement, defendIncrement

# Roll the dice
def rollDice(t, attackingPlayer, attackFrom, attackTo):
    # Determine how many attack dice to roll
    if countryD[attackFrom]["armies"] == 3:
        attackNumDice = 2
    elif countryD[attackFrom]["armies"] == 2:
        attackNumDice = 1
    else:
        attackNumDice = 3
    
    # Roll the dice
    aDice = []
    for i in range(attackNumDice):
        aDice.append(random.randint(1, 6))

    aDice.sort(reverse = True)

    # Determine how many defend dice to roll
    if countryD[attackTo]["armies"] == 1:
        defendNumDice = 1
    else:
        defendNumDice = 2
    
    # Roll the dice
    dDice = []
    for i in range(defendNumDice):
        dDice.append(random.randint(1, 6))

    dDice.sort(reverse = True)

    # Battle of armies
    attackIncrement, defendIncrement = drawDice(t, aDice, dDice)
    countryD[attackFrom]["armies"] += attackIncrement
    countryD[attackTo]["armies"] += defendIncrement

    print("Attacking armies:", countryD[attackFrom]["armies"], "Defending armies:", countryD[attackTo]["armies"])

    # If defending army is defeated, attacking player owns country
    if countryD[attackTo]["armies"] <= 0:
        countryD[attackTo]["armies"] = 0
        countryD[attackTo]["owner"] = attackingPlayer

    # Draw updates
    drawRectangle(t, countryD[attackFrom]["loc"][0], countryD[attackFrom]["loc"][1], 31, 15, countryD[attackFrom]["armies"], 12, playerD[attackingPlayer]["color"], -3)
    drawRectangle(t, countryD[attackTo]["loc"][0], countryD[attackTo]["loc"][1], 31, 15, countryD[attackTo]["armies"], 12, playerD[countryD[attackTo]["owner"]]["color"], -3)

# Determine if a player owns any countries
def noDefendingPlayerLeft(defendingPlayer):
    noneLeft = True
    for country in countryD:
        if countryD[country]["owner"] == defendingPlayer:
            noneLeft = False
    
    return noneLeft

# Determine if a player successfully captures a country
def attackNeighboringCountry(t, player):
    # Use temporary turtle to deal with ataccking/defending army counts
    dT = turtle.Turtle()
    dT.ht()
    countryCaptured = False
    attackFrom = eval("P" + str(player)).attackFromCountry(player, manual)
    print("Attacking from", attackFrom)
    while attackFrom != "NO ATTACK":
        # present list of countries owned with more than one army, 0 element is no attack
        attackTo, defendingPlayer = pickAttackTo(attackFrom, player)
        print("\nAttacking", attackTo)

        # Determine if a player can continue attacking
        continueAttack = ""
        while continueAttack != "RETREAT" and countryD[attackTo]["armies"] > 0 and countryD[attackFrom]["armies"] > 1:
            # Roll dice for battle
            rollDice(dT, player, attackFrom, attackTo)

            # Determine if the attacking player wants to attack again
            continueAttack = eval("P" + str(player)).continueAttack(countryD[attackTo]["armies"], countryD[attackFrom]["armies"], manual)

            dT.clear()

        # Attacking player takes over the country
        if continueAttack != "RETREAT" and countryD[attackTo]["armies"] <= 0:
            countryCaptured = True
            print("\nYou took over " + attackTo + "!")
            # Determine how many armies the player wants to move to the new country
            howManyToMove = eval("P"+str(player)).tookCountryMoveArmiesHowMany(attackFrom, manual)
            print("Moving", howManyToMove, "armies\n")

            countryD[attackFrom]["armies"] -= howManyToMove
            countryD[attackTo]["armies"] = howManyToMove
            attackFromCountryIndex = countryD[attackFrom]["loc"]
            attackToCountryIndex = countryD[attackTo]["loc"]

            # Draw updates
            drawRectangle(t, attackFromCountryIndex[0], attackFromCountryIndex[1], 31, 15, countryD[attackFrom]["armies"], 12, playerD[player]["color"], -3)
            drawRectangle(t, attackToCountryIndex[0], attackToCountryIndex[1], 31, 15, countryD[attackTo]["armies"], 12, playerD[countryD[attackTo]["owner"]]["color"], -3)

            # Attacking player has wiped out another player
            if noDefendingPlayerLeft(defendingPlayer):
                print("You destroyed player", defendingPlayer, "- his cards are now yours!")
                
                # Give the defenders cards to the player
                playerD[player]["cards"] += (playerD[defendingPlayer]["cards"])
                playerD[defendingPlayer]["cards"] = []

                # Determine new army count
                bookArmies = 0
                while hasABook(player):
                    bookArmies += playBooks(player, t)

                playerD[player]["armies"] = bookArmies

                # Draw updates
                drawPlayerBoxes(t, bookArmies, [player])

                # Repeat until no armies left in corner
                while stillArmiesToPlace(player):
                    # Display list and ask for country choice and number to place, update displays
                    armyPlacement(player, t)

        # Attacker chose to retreat or attacker ran out of armies
        else:
            if continueAttack == "RETREAT":
                print("\nAttacker chose to RETREAT!")
            else:
                print("Attacker ran out of armies!")

        attackFromCountryIndex = countryD[attackFrom]["loc"]
        attackToCountryIndex = countryD[attackTo]["loc"]

        # Draw updates
        drawRectangle(t, attackFromCountryIndex[0], attackFromCountryIndex[1], 31, 15, countryD[attackFrom]["armies"], 12, playerD[player]["color"], -3)
        drawRectangle(t, attackToCountryIndex[0], attackToCountryIndex[1], 31, 15, countryD[attackTo]["armies"], 12, playerD[countryD[attackTo]["owner"]]["color"], -3)
        
        attackFrom = eval("P" + str(player)).attackFromCountry(player, manual)
        print("Attacking from", attackFrom)
    
    return countryCaptured

# Move troops to a new location
def troopMovement(player, t):
    # Get movement info from player
    fromCountry, toCountry, howManyToMove = eval("P" + str(player)).troopMove(player, manual)

    # Movement is optional
    if fromCountry != "" and howManyToMove != 0:
        countryD[fromCountry]["armies"] -= howManyToMove
        countryD[toCountry]["armies"] += howManyToMove

        print("\nPLAYER", player, "moved", howManyToMove, "armies from", fromCountry, "to", toCountry)

        # Draw updates
        drawRectangle(t, countryD[fromCountry]["loc"][0], countryD[fromCountry]["loc"][1], 31, 15, countryD[fromCountry]["armies"], 12, playerD[player]["color"], -3)
        drawRectangle(t, countryD[toCountry]["loc"][0], countryD[toCountry]["loc"][1], 31, 15, countryD[toCountry]["armies"], 12, playerD[player]["color"], -3)

# Determine if a player has countries
def playerHasNoCountries(player):
    return len(eval("P" + str(player)).getPlayerCountryList(player)) == 0

# Determine if a player has a book
def hasABook(player):
    if len(playerD[player]["cards"]) < 3:
        return False
    
    # Count each unit type
    artCount = 0
    infCount = 0
    cavCount = 0
    wildCount = 0
    for card in playerD[player]["cards"]:
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

def playBooks(player, t):
    bookArmies = 0

    # Display the player's cards with and index number beside them, also display a menu item to exit
    bookCardIndices = eval("P" + str(player)).getBookCardIndices(player, playerD, manual)
    print("INDICES", bookCardIndices)
    print("CARDS", playerD[player]["cards"])

    if len(bookCardIndices) != 0:
        bookCardIndices.sort(reverse = True)
        bookArmies += bookArmiesBonusList.pop(0)

    countryList = getPlayerCountryList(player)
    for index in bookCardIndices:
        # Allocate 2 armies to any country in my book and get rid of the played cards
        print("Popping", index)
        print(playerD[player]["cards"])
        card = playerD[player]["cards"].pop(index)
        if card[0] in countryList:
            print("Country OWNED IN BOOK BONUS")
            # Put two armies on that country
            countryD[card[0]]["armies"] = countryD[card[0]]["armies"] + 2
            drawRectangle(t, countryD[card[0]]["loc"][0], countryD[card[0]]["loc"][1], 31, 15, countryD[card[0]]["armies"], 12, playerD[countryD[card[0]]["owner"]]["color"], -3)
    
    return bookArmies

def drawCountryArmies(t):
    for country in countryD:
        drawRectangle(t, countryD[country]["loc"][0], countryD[country]["loc"][1], 31, 15, countryD[country]["armies"], 12, playerD[countryD[country]["owner"]]["color"], -3)    
    
def riskMain():
    # Screen and turtle setup
    bob = turtle.Turtle()
    bob.ht()
    screen = turtle.Screen()
    screen.tracer(1000, 1000)
    screen.setup(width = 836, height = 625, startx = 100, starty = 300)
    screen.bgpic("Risk01.gif")

    # Draw player army count boxes
    drawPlayerBoxes(bob, "30", [1, 2, 3, 4])

    # Randomly set the first player
    player = random.randrange(1, 5)
    player = autoAssignCountries(bob, player)

    # Place armies while players still have armies to place
    while stillArmiesToPlace(player):
        armyPlacement(player, bob)
        player = nextPlayer(player)

    # Create the card deck of military units
    riskCards = createCards(countryD)

    print("\n\n" + "*" * 30+ "\nBEGINNING OF GAME PLAY\n" + "*" * 30)

    # Main game loop
    while not gameOver():
        print("\nSTART PLAYER", player, "TURN")
        # Print cards
        if playerD[player]["cards"] != 0:
            print("PLAYER", player, "CARDS:")
            for card in playerD[player]["cards"]:
                print(card)

        print("NEXT BOOK:", bookArmiesBonusList[0])

        # Calculate total number of armies to place
        bookArmies = 0
        if hasABook(player):
            bookArmies = playBooks(player, bob)

        armiesToPlace = calcBaseArmiesBeginningOfTurn(player)
        continentsBonus = findContinentsBonusBeginningOfTurn(player)
        totalArmies = armiesToPlace + continentsBonus + bookArmies
        playerD[player]["armies"] = totalArmies
        drawPlayerBoxes(bob, totalArmies, [player])

        # Repeat until no armies left
        while stillArmiesToPlace(player):
            # Display list and ask for country choice and number to place, update displays
            armyPlacement(player, bob)

        # Determing if a player catpured a country
        countryCaptured = attackNeighboringCountry(bob, player)
        if countryCaptured and len(riskCards) > 0:
            playerD[player]["cards"].append(riskCards.pop())

        # Move troops after attacking
        troopMovement(player, bob)

        print("\nEND PLAYER", player, "TURN")

        # Rotate to next player
        player = nextPlayer(player)
        while playerHasNoCountries(player):
            player = nextPlayer(player)
        
        time.sleep(1)

    # Win message
    print("Congratulations player " + str(countryD["Western United States"]["owner"]) + ", you are the winner!!!")

# Run the game
riskMain()
