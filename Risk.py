import turtle
import time
import random
from riskStructs import countryD, continentD, armiesPerContinentD
import P1, P2, P3, P4

# Struct for player information
playerd = {1: {"armies": 30, "color": 'green', "loc": (-350, 257), "cards": []},
           2: {"armies": 30, "color": 'blue', "loc": (220, 257), "cards": []},
           3: {"armies": 30, "color": 'purple', "loc": (220, -289), "cards": []},
           4: {"armies": 30, "color": 'red', "loc": (-350, -289), "cards": []}}

# Automatic game or not
manual = False

# Bonus army counts
bookarmiesbonuslist = [4, 6, 8, 10, 12, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]

# Draw a rectangle
def drawrectangle(t, x, y, width, height, text, fontsize, fontcolor, offset):
    t.up()
    t.goto(x, y)
    t.down()
    t.fillcolor("white")
    t.begin_fill()
    for _ in range(2):
        t.forward(width)
        t.right(90)
        t.forward(height)
        t.right(90)
    t.end_fill()
    if text != "":
        t.up()
        t.goto(x + 5, y - height + offset)
        t.color(fontcolor)
        t.write(text, font = ('Arial', fontsize, 'bold'))
    t.down()

# Draw army count boxes for each player
def drawplayerboxes(t, text, whichones):
    for i in whichones:
        t.color(playerd[i]["color"])
        t.up()
        t.goto(playerd[i]["loc"])
        t.write("PLAYER " + str(i), font = ('Arial', 18, 'bold'))
        drawrectangle(t, playerd[i]["loc"][0] + 120, playerd[i]["loc"][1] + 30, 62, 30, text, 18, playerd[i]["color"], 0)

    t.color("black")

# Randomly assign countries to players
def autoassigncountries(t, player):
    countrylist = list(countryD.keys())
    while len(countrylist) > 0:
        # Randomly assign a country to player and place army
        country = countrylist.pop(random.randrange(0, len(countrylist)))
        countryD[country]["owner"] = player
        countryD[country]["armies"] = 1
        playerd[player]["armies"] -= 1

        # Draw updates
        drawplayerboxes(t, str(playerd[player]["armies"]), [player])
        drawrectangle(t, countryD[country]["loc"][0], countryD[country]["loc"][1], 31, 15, "1", 12, playerd[player]["color"], -3)

        # Rotate to next player
        player = nextplayer(player)

    return player

# Create card book for military units
def createcards(countryd):
    countrylist = list(countryd.keys())
    cardlist = []

    # Add two wild cards into the deck
    card = ["wild", "wild"]
    cardlist.append(card)
    cardlist.append(card)

    # Add units into deck
    for _ in range(14):
        card = [countrylist.pop(), "artillery"]
        cardlist.append(card)

    for _ in range(14):
        card = [countrylist.pop(), "cavalry"]
        cardlist.append(card)

    for _ in range(14):
        card = [countrylist.pop(), "infantry"]
        cardlist.append(card)

    random.shuffle(cardlist)

    return cardlist

# Determine if players still have armies to place
def stillarmiestoplace(player):
    return playerd[player]["armies"] > 0

# Get list of countries the player owns
def getplayercountrylist(player):
    countrylist = []
    for countrykey in countryD:
        if countryD[countrykey]["owner"] == player:
            countrylist.append(countrykey)

    return countrylist

# Place armies in a country
def armyplacement(player, t):
    country, numberofarmiestoplace = eval("P" + str(player)).place_armies(player, playerd, manual)
    countryD[country]["armies"] = countryD[country]["armies"] + numberofarmiestoplace
    playerd[player]["armies"] = playerd[player]["armies"] - numberofarmiestoplace

    print("\nPLAYER", player, "placing", numberofarmiestoplace, "armies", "\n")

    # Draw updates
    drawrectangle(t, countryD[country]["loc"][0], countryD[country]["loc"][1], 31, 15, countryD[country]["armies"], 12, playerd[player]["color"], -3)
    drawplayerboxes(t, str(playerd[player]["armies"]), [player])

# Rotate to the next player
def nextplayer(player):
    player += 1
    if player == 5:
        player = 1

    return player

# Determine if a player owns every country
def gameover():
    winnerlist = []
    for key in countryD:
        winnerlist.append(countryD[key]["owner"])

    return winnerlist.count(winnerlist[0]) == len(winnerlist)

# Calculate base army count
def calcbasearmiesbeginningofturn(player):
    count = 0
    for key in countryD:
        if countryD[key]["owner"] == player:
            count += 1

    # Return minimum base of 3 armies
    return max(3, count // 3)

# Determine continent bonus armies
def findcontinentsbonusbeginningofturn(player):
    continentbonustotal = 0
    countrylist = getplayercountrylist(player)
    for eachcontinentkey in continentD:
        ownscontinent = True
        for eachcountry in continentD[eachcontinentkey]:
            if eachcountry not in countrylist:
                ownscontinent = False

        if ownscontinent:
            continentbonustotal += armiesPerContinentD[eachcontinentkey]

    return continentbonustotal

# Pick a country to attack
def pick_attack_to(country, player):
    return eval("P" + str(player)).attack_to_country(player, country, manual)

# Draw the dice
def drawdice(t, adice, ddice):
    t.up()

    x = -80
    y = 300
    for die in adice:
        drawrectangle(t, x, y, 40, 40, die, 26, "black", 0)
        x = x + 50

    x = -80
    y = 250
    for die in ddice:
        drawrectangle(t, x, y, 40, 40, die, 26, "black", 0)
        x = x + 50

    # Determine armies lost
    attackincrement = 0
    defendincrement = 0
    if adice[0] > ddice[0]:
        defendincrement -= 1
    else:
        attackincrement -= 1

    if len(ddice) == 2 and len(adice) > 1:
        if adice[1] > ddice[1]:
            defendincrement -= 1
        else:
            attackincrement -= 1

    return attackincrement, defendincrement

# Roll the dice
def rolldice(t, attackingplayer, attackfrom, attackto):
    # Determine how many attack dice to roll
    if countryD[attackfrom]["armies"] == 3:
        attacknumdice = 2
    elif countryD[attackfrom]["armies"] == 2:
        attacknumdice = 1
    else:
        attacknumdice = 3

    # Roll the dice
    adice = []
    for _ in range(attacknumdice):
        adice.append(random.randint(1, 6))

    adice.sort(reverse = True)

    # Determine how many defend dice to roll
    if countryD[attackto]["armies"] == 1:
        defendnumdice = 1
    else:
        defendnumdice = 2

    # Roll the dice
    ddice = []
    for _ in range(defendnumdice):
        ddice.append(random.randint(1, 6))

    ddice.sort(reverse = True)

    # Battle of armies
    attackincrement, defendincrement = drawdice(t, adice, ddice)
    countryD[attackfrom]["armies"] += attackincrement
    countryD[attackto]["armies"] += defendincrement

    print("Attacking armies:", countryD[attackfrom]["armies"], "Defending armies:", countryD[attackto]["armies"])

    # If defending army is defeated, attacking player owns country
    if countryD[attackto]["armies"] <= 0:
        countryD[attackto]["armies"] = 0
        countryD[attackto]["owner"] = attackingplayer

    # Draw updates
    drawrectangle(t, countryD[attackfrom]["loc"][0], countryD[attackfrom]["loc"][1], 31, 15, countryD[attackfrom]["armies"], 12, playerd[attackingplayer]["color"], -3)
    drawrectangle(t, countryD[attackto]["loc"][0], countryD[attackto]["loc"][1], 31, 15, countryD[attackto]["armies"], 12, playerd[countryD[attackto]["owner"]]["color"], -3)

# Determine if a player owns any countries
def nodefendingplayerleft(defendingplayer):
    noneleft = True
    for country in countryD:
        if countryD[country]["owner"] == defendingplayer:
            noneleft = False

    return noneleft

# Determine if a player successfully captures a country
def attackneighboringcountry(t, player):
    # Use temporary turtle to deal with attacking/defending army counts
    dt = turtle.Turtle()
    dt.ht()
    countrycaptured = False
    attackfrom = eval("P" + str(player)).attack_from_country(player, manual)
    print("Attacking from", attackfrom)
    while attackfrom != "NO ATTACK":
        # present list of countries owned with more than one army, 0 element is no attack
        attackto, defendingplayer = pick_attack_to(attackfrom, player)
        print("\nAttacking", attackto)

        # Determine if a player can continue attacking
        continueattack = ""
        while continueattack != "RETREAT" and countryD[attackto]["armies"] > 0 and countryD[attackfrom]["armies"] > 1:
            # Roll dice for battle
            rolldice(dt, player, attackfrom, attackto)

            # Determine if the attacking player wants to attack again
            continueattack = eval("P" + str(player)).continue_attack(countryD[attackto]["armies"], countryD[attackfrom]["armies"], manual)

            dt.clear()

        # Attacking player takes over the country
        if continueattack != "RETREAT" and countryD[attackto]["armies"] <= 0:
            countrycaptured = True
            print("\nYou took over " + attackto + "!")
            # Determine how many armies the player wants to move to the new country
            howmanytomove = eval("P"+str(player)).took_country_move_armies_how_many(attackfrom, manual)
            print("Moving", howmanytomove, "armies\n")

            countryD[attackfrom]["armies"] -= howmanytomove
            countryD[attackto]["armies"] = howmanytomove
            attackfromcountryindex = countryD[attackfrom]["loc"]
            attacktocountryindex = countryD[attackto]["loc"]

            # Draw updates
            drawrectangle(t, attackfromcountryindex[0], attackfromcountryindex[1], 31, 15, countryD[attackfrom]["armies"], 12, playerd[player]["color"], -3)
            drawrectangle(t, attacktocountryindex[0], attacktocountryindex[1], 31, 15, countryD[attackto]["armies"], 12, playerd[countryD[attackto]["owner"]]["color"], -3)

            # Attacking player has wiped out another player
            if nodefendingplayerleft(defendingplayer):
                print("You destroyed player", defendingplayer, "- his cards are now yours!")

                # Give the defenders cards to the player
                playerd[player]["cards"] += (playerd[defendingplayer]["cards"])
                playerd[defendingplayer]["cards"] = []

                # Determine new army count
                bookarmies = 0
                while has_a_book(player):
                    bookarmies += playbooks(player, t)

                playerd[player]["armies"] = bookarmies

                # Draw updates
                drawplayerboxes(t, bookarmies, [player])

                # Repeat until no armies left in corner
                while stillarmiestoplace(player):
                    # Display list and ask for country choice and number to place, update displays
                    armyplacement(player, t)

        # Attacker chose to retreat or attacker ran out of armies
        else:
            if continueattack == "RETREAT":
                print("\nAttacker chose to RETREAT!")
            else:
                print("Attacker ran out of armies!")

        attackfromcountryindex = countryD[attackfrom]["loc"]
        attacktocountryindex = countryD[attackto]["loc"]

        # Draw updates
        drawrectangle(t, attackfromcountryindex[0], attackfromcountryindex[1], 31, 15, countryD[attackfrom]["armies"], 12, playerd[player]["color"], -3)
        drawrectangle(t, attacktocountryindex[0], attacktocountryindex[1], 31, 15, countryD[attackto]["armies"], 12, playerd[countryD[attackto]["owner"]]["color"], -3)

        attackfrom = eval("P" + str(player)).attack_from_country(player, manual)
        print("Attacking from", attackfrom)

    return countrycaptured

# Move troops to a new location
def troop_movement(player, t):
    # Get movement info from player
    from_country, to_country, how_many_to_move = eval("P" + str(player)).troop_move(player, manual)

    # Movement is optional
    if from_country != "" and how_many_to_move != 0:
        countryD[from_country]["armies"] -= how_many_to_move
        countryD[to_country]["armies"] += how_many_to_move

        print("\nPLAYER", player, "moved", how_many_to_move, "armies from", from_country, "to", to_country)

        # Draw updates
        drawrectangle(t, countryD[from_country]["loc"][0], countryD[from_country]["loc"][1], 31, 15, countryD[from_country]["armies"], 12, playerd[player]["color"], -3)
        drawrectangle(t, countryD[to_country]["loc"][0], countryD[to_country]["loc"][1], 31, 15, countryD[to_country]["armies"], 12, playerd[player]["color"], -3)

# Determine if a player has countries
def player_has_no_countries(player):
    return len(eval("P" + str(player)).get_player_country_list(player)) == 0

# Determine if a player has a book
def has_a_book(player):
    if len(playerd[player]["cards"]) < 3:
        return False

    # Count each unit type
    artcount = 0
    infcount = 0
    cavcount = 0
    wildcount = 0
    for card in playerd[player]["cards"]:
        if card[1] == "artillery":
            artcount += 1
        elif card[1] == "infantry":
            infcount += 1
        elif card[1] == "cavalry":
            cavcount += 1
        else:
            wildcount += 1

    # Check for three of a kind
    if artcount >= 3 or infcount >= 3 or cavcount >= 3:
        return True
    if artcount >= 1 and infcount >= 1 and cavcount >= 1:
        return True
    if wildcount >= 1:
        return True

    return False

def playbooks(player, t):
    bookarmies = 0

    # Display the player's cards with and index number beside them, also display a menu item to exit
    bookcardindices = eval("P" + str(player)).get_book_card_indices(player, playerd, manual)
    print("INDICES", bookcardindices)
    print("CARDS", playerd[player]["cards"])

    if len(bookcardindices) != 0:
        bookcardindices.sort(reverse = True)
        bookarmies += bookarmiesbonuslist.pop(0)

    countrylist = getplayercountrylist(player)
    for index in bookcardindices:
        # Allocate 2 armies to any country in my book and get rid of the played cards
        print("Popping", index)
        print(playerd[player]["cards"])
        card = playerd[player]["cards"].pop(index)
        if card[0] in countrylist:
            print("Country OWNED IN BOOK BONUS")
            # Put two armies on that country
            countryD[card[0]]["armies"] = countryD[card[0]]["armies"] + 2
            drawrectangle(t, countryD[card[0]]["loc"][0], countryD[card[0]]["loc"][1], 31, 15, countryD[card[0]]["armies"], 12, playerd[countryD[card[0]]["owner"]]["color"], -3)

    return bookarmies

def drawcountryarmies(t):
    for country in countryD:
        drawrectangle(t, countryD[country]["loc"][0], countryD[country]["loc"][1], 31, 15, countryD[country]["armies"], 12, playerd[countryD[country]["owner"]]["color"], -3)

def riskmain():
    # Screen and turtle setup
    bob = turtle.Turtle()
    bob.ht()
    screen = turtle.Screen()
    screen.tracer(1000, 1000)
    screen.setup(width = 836, height = 625, startx = 100, starty = 300)
    screen.bgpic("Risk01.gif")

    # Draw player army count boxes
    drawplayerboxes(bob, "30", [1, 2, 3, 4])

    # Randomly set the first player
    player = random.randrange(1, 5)
    player = autoassigncountries(bob, player)

    # Place armies while players still have armies to place
    while stillarmiestoplace(player):
        armyplacement(player, bob)
        player = nextplayer(player)

    # Create the card deck of military units
    riskcards = createcards(countryD)

    print("\n\n" + "*" * 30+ "\nBEGINNING OF GAME PLAY\n" + "*" * 30)

    # Main game loop
    while not gameover():
        print("\nSTART PLAYER", player, "TURN")
        # Print cards
        if playerd[player]["cards"] != 0:
            print("PLAYER", player, "CARDS:")
            for card in playerd[player]["cards"]:
                print(card)

        print("NEXT BOOK:", bookarmiesbonuslist[0])

        # Calculate total number of armies to place
        bookarmies = 0
        if has_a_book(player):
            bookarmies = playbooks(player, bob)

        armiestoplace = calcbasearmiesbeginningofturn(player)
        continentsbonus = findcontinentsbonusbeginningofturn(player)
        totalarmies = armiestoplace + continentsbonus + bookarmies
        playerd[player]["armies"] = totalarmies
        drawplayerboxes(bob, totalarmies, [player])

        # Repeat until no armies left
        while stillarmiestoplace(player):
            # Display list and ask for country choice and number to place, update displays
            armyplacement(player, bob)

        # Determing if a player catpured a country
        countrycaptured = attackneighboringcountry(bob, player)
        if countrycaptured and len(riskcards) > 0:
            playerd[player]["cards"].append(riskcards.pop())

        # Move troops after attacking
        troop_movement(player, bob)

        print("\nEND PLAYER", player, "TURN")

        # Rotate to next player
        player = nextplayer(player)
        while player_has_no_countries(player):
            player = nextplayer(player)

        time.sleep(1)

    # Win message
    print("Congratulations player " + str(countryD["Western United States"]["owner"]) + ", you are the winner!!!")

# Run the game
riskmain()
