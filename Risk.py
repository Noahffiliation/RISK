import cTurtle
import random
from riskStructs import *
import P1
import P2
import P3
import P4
#modnames = ['P1', 'P2', 'P3', 'P4']
#playerModuleNames = map(__import__, modnames)
#print(playerModuleNames)

countryD={
    "Alaska":{"loc":[-372,161],"owner":0},
    "Northwest Territory":{"loc":[-292,165],"owner":0},
    "Greenland":{"loc":[-149,196],"owner":0},
    "Alberta":{"loc":[-301,118],"owner":0},
    "Ontario":{"loc":[-243,110],"owner":0},
    "Eastern Canada":{"loc":[-197,106],"owner":0},
    "Western United States":{"loc":[-294,54],"owner":0},
    "Eastern United States":{"loc":[-231,38],"owner":0},
    "Central America":{"loc":[-276,5],"owner":0},

    "Venezuela":{"loc":[-233,-40],"owner":0},
    "Peru":{"loc":[-206,-106],"owner":0},
    "Brazil":{"loc":[-165,-90],"owner":0},
    "Argentina":{"loc":[-183,-143],"owner":0},

    "North Africa":{"loc":[-38,-77],"owner":0},
    "Egypt":{"loc":[30,-50],"owner":0},
    "East Africa":{"loc":[55,-99],"owner":0},
    "Central Africa":{"loc":[23,-108],"owner":0},
    "South Africa":{"loc":[25,-195],"owner":0},
    "Madagascar":{"loc":[116,-190],"owner":0},

    "Western Europe":{"loc":[-77,3],"owner":0},
    "Southern Europe":{"loc":[0,23],"owner":0},
    "Northern Europe":{"loc":[-28,67],"owner":0},
    "Russia":{"loc":[64,117],"owner":0},
    "Great Britain":{"loc":[-92,73],"owner":0},
    "Iceland":{"loc":[-71,140],"owner":0},
    "Scandinavia":{"loc":[-6,130],"owner":0},

    "Ural":{"loc":[149,120],"owner":0},
    "Siberia":{"loc":[193,142],"owner":0},
    "Yakutsk":{"loc":[249,185],"owner":0},
    "Kamchatka":{"loc":[313,186],"owner":0},
    "Irkutsk":{"loc":[226,121],"owner":0},
    "Japan":{"loc":[343,68],"owner":0},
    "Mongolia":{"loc":[243,76],"owner":0},
    "China":{"loc":[222,30],"owner":0},
    "Afghanistan":{"loc":[127,53],"owner":0},
    "Middle East":{"loc":[72,-5],"owner":0},
    "India":{"loc":[169,-13],"owner":0},
    "Southeast Asia":{"loc":[235,-4],"owner":0},

    "Indonesia":{"loc":[231,-104],"owner":0},
    "New Guinea":{"loc":[304,-87],"owner":0},
    "Western Australia":{"loc":[262,-174],"owner":0},
    "Eastern Australia":{"loc":[338,-156],"owner":0}}

playerD={1:{"armies":30,"color":'green',"loc":(-350,257),"cards":[]},
          2:{"armies":30,"color":'blue',"loc":(220,257),"cards":[]},
          3:{"armies":30,"color":'purple',"loc":(220,-289),"cards":[]},
          4:{"armies":30,"color":'red',"loc":(-350,-289),"cards":[]}}

bookArmiesBonusList=[4,6,8,10,12,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]

def drawPlayerBoxes(t,text,whichOnes):
    for i in whichOnes:
        t.color(playerD[i]["color"])
        t.up()
        t.goto(playerD[i]["loc"])
        t.write("PLAYER "+str(i),font=('Arial',18,'bold'))
        drawRectangle(t,playerD[i]["loc"][0]+120,playerD[i]["loc"][1]+30,62,30,text,18,playerD[i]["color"],0)
    t.color("black")

def drawRectangle(t,x,y,width,height,text,fontSize,fontColor,offSet):
    t.up()
    t.goto(x,y)
    t.down()
    t.fillcolor("white")
    t.begin_fill()
    for _ in range(2):
        t.forward(width)
        t.right(90)
        t.forward(height)
        t.right(90)
    t.end_fill()
    if text!="":
        t.up()
        t.goto(x+5,y-height+offSet)
        t.color(fontColor)
        t.write(text,font=('Arial',fontSize,'bold'))
    t.down()

def autoAssignCountries(t,player):
    countryList=list(countryD.keys())
    while len(countryList)>0:
        country=countryList.pop(random.randrange(0,len(countryList)))
        drawRectangle(t,countryD[country]["loc"][0],countryD[country]["loc"][1],31,15,"1",12,playerD[player]["color"],-3)
        countryD[country]["owner"]=player
        countryD[country]["armies"]=1
        playerD[player]["armies"]=playerD[player]["armies"]-1
        drawPlayerBoxes(t,str(playerD[player]["armies"]),[player])
        player=nextPlayer(player)
    return player

def createCards(countryD):
    countryList=list(countryD.keys())
    cardList=[]
    card=["wild","wild"]
    cardList.append(card)
    card=["wild","wild"]
    cardList.append(card)
    for i in range(14):
        card=[countryList.pop(),"artillery"]
        cardList.append(card)
    for i in range(14):
        card=[countryList.pop(),"cavalry"]
        cardList.append(card)
    for i in range(14):
        card=[countryList.pop(),"infantry"]
        cardList.append(card)
    random.shuffle(cardList)
    return cardList

def stillArmiesToPlace(playerD):
    for playerKey in playerD:
        if playerD[playerKey]["armies"]>0:
            return True
    return False

def getPlayerCountryList(player):
    countryList=[]
    for countryKey in countryD:
        if countryD[countryKey]["owner"]==player:
            countryList.append(countryKey)
    return countryList

def armyPlacement(player,t,phase):
    if playerD[player]["armies"]>0:
        country,numberOfArmiesToPlace=eval("P"+str(player)).placeArmies(player,countryD,bookArmiesBonusList,{player:playerD[player]})
        #country,numberOfArmiesToPlace=playerModuleNames[player-1].placeArmies(player,countryD,bookArmiesBonusList,{player:playerD[player]})
        countryD[country]["armies"]=countryD[country]["armies"]+numberOfArmiesToPlace
        playerD[player]["armies"]=playerD[player]["armies"]-numberOfArmiesToPlace
        drawRectangle(t,countryD[country]["loc"][0],countryD[country]["loc"][1],31,15,countryD[country]["armies"],12,playerD[player]["color"],-3)
        drawPlayerBoxes(t,str(playerD[player]["armies"]),[player])

def nextPlayer(player):
    player+=1
    if player==5:
        player=1
    return player

def gameOver():
    winnerList=[]
    for key in countryD:
        winnerList.append(countryD[key]["owner"])
    if winnerList.count(winnerList[0]) != len(winnerList):
        return False
    else:
        return True

def calcBaseArmiesBeginningOfTurn(player):
    count=0
    for key in countryD:
        if countryD[key]["owner"]==player:
            count+=1
    return max(3,count//3)

def findContinentsBonusBeginningOfTurn(player):
    continentBonusTotal=0
    countryList=getPlayerCountryList(player)
    for eachContinentKey in continentD:
        ownsContinent=True
        for eachCountry in continentD[eachContinentKey]:
            if eachCountry not in countryList:
                ownsContinent=False
        if ownsContinent:
            continentBonusTotal+=armiesPerContinentD[eachContinentKey]
    return continentBonusTotal

def pickAttackTo(country,player):
    return eval("P"+str(player)).attackToCountry(player,countryD,bookArmiesBonusList,{player:playerD[player]},country)
    #return playerModuleNames[player-1].attackToCountry(player,countryD,bookArmiesBonusList,{player:playerD[player]},country)

def drawDice(t,aDice,dDice):
    t.up()
    x=-80
    y=300
    for die in aDice:
        drawRectangle(t,x,y,40,40,die,26,"black",0)
        x=x+50
    x=-80
    y=250
    for die in dDice:
        drawRectangle(t,x,y,40,40,die,26,"black",0)
        x=x+50
    attackIncrement=0
    defendIncrement=0
    if aDice[0]>dDice[0]:
        defendIncrement-=1
    else:
        attackIncrement-=1
    if len(dDice)==2 and len(aDice)>1:
        if aDice[1]>dDice[1]:
            defendIncrement-=1
        else:
            attackIncrement-=1
    return attackIncrement, defendIncrement

def rollDice(dT,attackingPlayer,attackFrom,defendingPlayer,attackTo):
    attackNumDice=3
    if countryD[attackFrom]["armies"]==3:
        attackNumDice=2
    elif countryD[attackFrom]["armies"]==2:
        attackNumDice=1
    aDice=[]
    for i in range(attackNumDice):
        aDice.append(random.randint(1,6))
    aDice.sort(reverse=True)
    defendNumDice=2
    if countryD[attackTo]["armies"]==1:
        defendNumDice=1
    dDice=[]
    for i in range(defendNumDice):
        dDice.append(random.randint(1,6))
    dDice.sort(reverse=True)
    attackIncrement,defendIncrement=drawDice(dT,aDice,dDice)
    countryD[attackFrom]["armies"]+=attackIncrement
    countryD[attackTo]["armies"]+=defendIncrement
    #print(countryD[attackFrom]["armies"],countryD[attackTo]["armies"])
    if countryD[attackTo]["armies"]<=0:
        countryD[attackTo]["armies"]=0
        countryD[attackTo]["owner"]=attackingPlayer
    drawRectangle(dT,countryD[attackFrom]["loc"][0],countryD[attackFrom]["loc"][1],31,15,countryD[attackFrom]["armies"],12,playerD[attackingPlayer]["color"],-3)
    drawRectangle(dT,countryD[attackTo]["loc"][0],countryD[attackTo]["loc"][1],31,15,countryD[attackTo]["armies"],12,playerD[countryD[attackTo]["owner"]]["color"],-3)

def noDefendingPlayerLeft(defendingPlayer):
    noneLeft=True
    for country in countryD:
        if countryD[country]["owner"]==defendingPlayer:
            noneLeft=False
    return noneLeft

def attackNeighboringCountry(t,player):
    dT=cTurtle.Turtle()
    dT.ht()
    countryCaptured=False
    #attackFrom=playerModuleNames[player-1].attackFromCountry(player,countryD,bookArmiesBonusList,{player:playerD[player]})
    attackFrom=eval("P"+str(player)).attackFromCountry(player,countryD,bookArmiesBonusList,{player:playerD[player]})
    print("Attacking from",attackFrom)
    while attackFrom != "NO ATTACK":
        #present list of countries owned with more than one army, 0 element is no attack
        attackTo,defendingPlayer=pickAttackTo(attackFrom,player)
        print("\nAttacking",attackTo)
        continueAttack=""
        while continueAttack != "RETREAT" and countryD[attackTo]["armies"]>0 and countryD[attackFrom]["armies"]>1:
            rollDice(dT, player, attackFrom, defendingPlayer, attackTo)
            if countryD[attackTo]["armies"]>0 and countryD[attackFrom]["armies"]>1:
                #continueAttack=playerModuleNames[player-1].continueAttack(player,countryD,bookArmiesBonusList,{player:playerD[player]})
                continueAttack=eval("P"+str(player)).continueAttack(player,countryD,bookArmiesBonusList,{player:playerD[player]})
            dT.clear()
        if continueAttack != "RETREAT" and countryD[attackTo]["armies"]<=0:  #wiped out the enemy from a country
            print("\nYou took over "+attackTo+"!")
            howManyToMove=eval("P"+str(player)).tookCountryMoveArmiesHowMany(player,countryD,bookArmiesBonusList,{player:playerD[player]},attackFrom)
            #howManyToMove=playerModuleNames[player-1].tookCountryMoveArmiesHowMany(player,countryD,bookArmiesBonusList,{player:playerD[player]},attackFrom)
            print("Moving",howManyToMove,"armies\n")
            countryD[attackFrom]["armies"]-=howManyToMove
            countryD[attackTo]["armies"]=howManyToMove
            countryCaptured=True
            attackFromCountryIndex=countryD[attackFrom]["loc"]
            attackToCountryIndex=countryD[attackTo]["loc"]
            drawRectangle(t,attackFromCountryIndex[0],attackFromCountryIndex[1],31,15,countryD[attackFrom]["armies"],12,playerD[player]["color"],-3)
            drawRectangle(t,attackToCountryIndex[0],attackToCountryIndex[1],31,15,countryD[attackTo]["armies"],12,playerD[countryD[attackTo]["owner"]]["color"],-3)
            if noDefendingPlayerLeft(defendingPlayer):
                print("You destroyed player",defendingPlayer,"- his cards are now yours!")
                #give the defenders cards to the player
                playerD[player]["cards"]+=(playerD[defendingPlayer]["cards"])
                playerD[defendingPlayer]["cards"]=[]
                bookArmies=0
                while hasABook(player):
                    bookArmies+=playBooks(player,t)
                playerD[player]["armies"]=bookArmies
                drawPlayerBoxes(t,bookArmies,[player])
                #Repeat until no armies left in corner
                while stillArmiesToPlace(playerD):
                    #Display list and ask for country choice and number to place, update displays
                    armyPlacement(player,t,"Takeover Book Placement")
        else: #attacker chose to retreat or attacker ran out of armies
            if continueAttack=="RETREAT":
                print("Attacker chose to RETREAT!")
            else:
                print("Attacker ran out of armies!")
        attackFromCountryIndex=countryD[attackFrom]["loc"]
        attackToCountryIndex=countryD[attackTo]["loc"]
        drawRectangle(t,attackFromCountryIndex[0],attackFromCountryIndex[1],31,15,countryD[attackFrom]["armies"],12,playerD[player]["color"],-3)
        drawRectangle(t,attackToCountryIndex[0],attackToCountryIndex[1],31,15,countryD[attackTo]["armies"],12,playerD[countryD[attackTo]["owner"]]["color"],-3)
        #attackFrom=playerModuleNames[player-1].attackFromCountry(player,countryD,bookArmiesBonusList,{player:playerD[player]})
        attackFrom=eval("P"+str(player)).attackFromCountry(player,countryD,bookArmiesBonusList,{player:playerD[player]})
        print("Attacking from",attackFrom)
    return countryCaptured

def troopMovement(player,t):
    fromCountry,toCountry,howManyToMove=eval("P"+str(player)).troopMove(player,countryD,bookArmiesBonusList,{player:playerD[player]})
    #fromCountry,toCountry,howManyToMove=playerModuleNames[player-1].troopMove(player,countryD,bookArmiesBonusList,{player:playerD[player]})
    if fromCountry!="":
        countryD[fromCountry]["armies"]-=howManyToMove
        countryD[toCountry]["armies"]+=howManyToMove
        drawRectangle(t,countryD[fromCountry]["loc"][0],countryD[fromCountry]["loc"][1],31,15,countryD[fromCountry]["armies"],12,playerD[player]["color"],-3)
        drawRectangle(t,countryD[toCountry]["loc"][0],countryD[toCountry]["loc"][1],31,15,countryD[toCountry]["armies"],12,playerD[countryD[toCountry]["owner"]]["color"],-3)

def playerHasNoCountries(player):
    count=0
    for countryKey in countryD:
        if countryD[countryKey]["owner"]==player:
            count+=1
    #print("COUNT",count)
    if count==0:
        return True
    else:
        return False

def hasABook(player):
    artCount=0
    infCount=0
    cavCount=0
    wildCount=0
    if len(playerD[player]["cards"])< 3:
        return False
    for card in playerD[player]["cards"]:
        if card[1]=="artillery":
            artCount+=1
        elif card[1]=="infantry":
            infCount+=1
        elif card[1]=="cavalry":
            cavCount+=1
        else:
            wildCount+=1
    #Check for three of a kind
    if artCount>=3 or infCount>=3 or cavCount>=3:
        return True
    if artCount>=1 and infCount>=1 and cavCount>=1:
        return True
    if wildCount>=1:
        return True

    return False

def playBooks(player,t):
    bookArmies=0
    #Display the players cards with and index number beside them, also display a menu item to exit
    #bookCardIndices=playerModuleNames[player-1].getBookCardIndices(player,countryD,bookArmiesBonusList,{player:playerD[player]})
    bookCardIndices=eval("P"+str(player)).getBookCardIndices(player,countryD,bookArmiesBonusList,{player:playerD[player]})
    print("INDICES",bookCardIndices)
    print("CARDS",playerD[player]["cards"])
    if len(bookCardIndices)!=0:
        bookCardIndices.sort(reverse=True)
        bookArmies+=bookArmiesBonusList.pop(0)
    countryList=getPlayerCountryList(player)
    for index in bookCardIndices:
        #Allocate 2 armies to any country in my book and Get rid of the played cards
        print("Popping",index)
        print(playerD[player]["cards"])
        card=playerD[player]["cards"].pop(index)
        if card[0] in countryList:
            print("Country OWNED IN BOOK BONUS")
            #Put two armies on that country
            countryD[card[0]]["armies"]=countryD[card[0]]["armies"]+2
            drawRectangle(t,countryD[card[0]]["loc"][0],countryD[card[0]]["loc"][1],31,15,countryD[card[0]]["armies"],12,playerD[countryD[card[0]]["owner"]]["color"],-3)
    return bookArmies

def drawcountryarmies(t):
    for country in countryD:
        drawRectangle(t,countryD[country]["loc"][0],countryD[country]["loc"][1],31,15,countryD[country]["armies"],12,playerD[countryD[country]["owner"]]["color"],-3)

def riskMain():
    bob=cTurtle.Turtle()
    bob.tracer(False)
    bob.ht()
    bob.setup(width=836,height=625,startx=0,starty=0)
    bob.bgpic("Risk01.gif")
    drawPlayerBoxes(bob,"30",[1,2,3,4])
    player=random.randrange(1,5)
    firstPlayer=player
    player=autoAssignCountries(bob,player)
    while stillArmiesToPlace(playerD):
        armyPlacement(player,bob,"Placement of Remaining Starting Armies")
        player=nextPlayer(player)
    riskCards = createCards(countryD)
    print("\n\n"+"*"*30+"\nBEGINNING OF GAME PLAY\n"+"*"*30)
    bob.setup(width=836,height=625,startx=0,starty=0)
    ##### MAIN GAME LOOP #####
    while not gameOver(): #Entire rest of game played in this loop
        print("PLAYER",player,"CARDS:")
        for card in playerD[player]["cards"]:
            print(card)
        print("NEXT BOOK:",bookArmiesBonusList[0])
        bookArmies=0
        if hasABook(player):
            bookArmies=playBooks(player,bob)
        #calculate base armies from num of countries
        armiesToPlace=calcBaseArmiesBeginningOfTurn(player)
        #calculate continent(s) bonus
        continentsBonus=findContinentsBonusBeginningOfTurn(player)
        #Post total armies to place in corner
        totalArmies=armiesToPlace+continentsBonus+bookArmies
        playerD[player]["armies"]=totalArmies
        drawPlayerBoxes(bob,totalArmies,[player])
        #Repeat until no armies left in corner
        while stillArmiesToPlace(playerD):
            #Display list and ask for country choice and number to place, update displays
            armyPlacement(player,bob,"START OF TURN Placement")
        countryCaptured=attackNeighboringCountry(bob,player)
        if countryCaptured and len(riskCards)>0:
            playerD[player]["cards"].append(riskCards.pop())
        troopMovement(player,bob)
        player=nextPlayer(player)
        while playerHasNoCountries(player):
            player=nextPlayer(player)
    print("Congratulations player "+str(countryD["Western United States"]["owner"])+", you are the winner!!!")

# Run the game
if __name__ == "__main__":
    riskmain()
