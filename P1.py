from riskStructs import countryD, adjacentCountriesD
import random

# Get list of countries that the player owns
def get_player_country_list(player):
    country_list = []
    for country_key in countryD:
        if countryD[country_key]["owner"] == player:
            country_list.append(country_key)

    return country_list

# Determine if there is an enemy adjacent to a player's country
def at_least_one_adjacent_enemy(country_key, player):
    at_least_one = False
    for each in adjacentCountriesD[country_key]:
        if countryD[each]["owner"] != player:
            at_least_one = True

    return at_least_one

# Determine if a player has a book
def has_picked_a_book(player_d, player, index_list):
    if len(index_list) < 3:
        return False

    # Convert indexes to cards
    cards = []
    for idx in index_list:
        cards.append(player_d[player]["cards"][idx])

    art_count = 0
    inf_count = 0
    cav_count = 0
    wild_count = 0
    for card in cards:
        if card[1] == "artillery":
            art_count += 1
        elif card[1] == "infantry":
            inf_count += 1
        elif card[1] == "cavalry":
            cav_count += 1
        else:
            wild_count += 1

    # Check for three of a kind
    if art_count >= 3 or inf_count >= 3 or cav_count >= 3:
        return True
    if art_count >= 1 and inf_count >= 1 and cav_count >= 1:
        return True
    if wild_count >= 1:
        return True

    return False

def attack_from_country(player, manual):
    # Build list of countries to attack from
    country_list = []
    for country_key in countryD:
        if countryD[country_key]["owner"] == player and countryD[country_key]["armies"] >= 2 and at_least_one_adjacent_enemy(country_key, player):
            country_list.append(country_key)

    if country_list == []:
        return "NO ATTACK"

    if manual:
        # List choices
        print("0. NO ATTACK")
        for i in range(1, len(country_list) + 1):
            print(str(i) + ". " + country_list[i - 1])

        # Get player choice
        choice = -1
        while choice < 0 or choice > len(country_list):
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
            return country_list[choice - 1]

    # AUTOMATIC
    else:
        if len(country_list) == 1:
            return country_list[0]
        else:
            # Determine country with largest number of armies
            max_armies = ""
            for country in range(1, len(country_list)):
                if countryD[country_list[country]]["armies"] > countryD[country_list[country - 1]]["armies"]:
                    max_armies = country_list[country]
                else:
                    max_armies = country_list[country - 1]

            return max_armies

# Determine which country to attack
def attack_to_country(player, attack_from_country, manual):
    # Get list of possible targets
    possibles_list = []
    for each_country in adjacentCountriesD[attack_from_country]:
        if countryD[each_country]["owner"] != player:
            possibles_list.append(each_country)

    if manual:
        # List possible targets
        for index in range(len(possibles_list)):
            print(str(index) + ". ", possibles_list[index])

        # Get player choice
        choice = -1
        while choice < 0 or choice >= len(possibles_list):
            choice = input("Which country would you like to attack? => ")
            if choice.isnumeric():
                choice = int(choice)
            else:
                choice = 0

        return possibles_list[choice], countryD[possibles_list[choice]]["owner"]

    # AUTOMATIC
    else:
        if len(possibles_list) == 1:
            return possibles_list[0], countryD[possibles_list[0]]["owner"]
        else:
            min_armies = ""
            for country in range(1, len(possibles_list)):
                if countryD[possibles_list[country]]["armies"] < countryD[possibles_list[country - 1]]["armies"]:
                    min_armies = possibles_list[country]
                else:
                    min_armies = possibles_list[country - 1]

            return min_armies, countryD[min_armies]["owner"]

# Determine if a player wants to attack again
def continue_attack(attack_to_armies, attack_from_armies, manual):
    if manual:
        ret = (input("Attack again? (Enter to attack, RETREAT and enter to end attack) => "))

    # AUTOMATIC
    else:
        # Only attack if player has more than 2 armies above the other player
        if attack_to_armies != 0 and attack_from_armies - attack_to_armies <= 3:
            ret = "RETREAT"
        else:
            ret = ""

    return ret

# Get book indices to play
def get_book_card_indices(player, player_d_me, manual):
    print("IN PLAYER", player)
    list_of_card_indices_to_play = []
    if manual:
        while not has_picked_a_book(player_d_me, player, list_of_card_indices_to_play):
            # List choices
            idx = 0
            for card in player_d_me[player]["cards"]:
                print(str(idx) + ". ", card)
                idx += 1
            print(str(idx) + ". ", "DO NOT play a book")

            for _ in range(3):
                answer = "-1"
                while int(answer) < 0 or int(answer)>idx or int(answer) in list_of_card_indices_to_play:
                    answer = input("Play card => ")
                if int(answer) == idx:
                    return []
                else:
                    list_of_card_indices_to_play.append(int(answer))
            if not has_picked_a_book(player_d_me, player, list_of_card_indices_to_play):
                list_of_card_indices_to_play = []
    else:
        list_of_card_indices_to_play = []
        while not has_picked_a_book(player_d_me, player, list_of_card_indices_to_play):
            list_of_card_indices_to_play = []
            list_of_indices = list(range(len(player_d_me[player]["cards"])))
            for _ in range(3):
                list_of_card_indices_to_play.append(list_of_indices.pop(random.randrange(0, len(list_of_indices))))

    return list_of_card_indices_to_play

# Determine how many armies to move into the captured country
def took_country_move_armies_how_many(attack_from, manual):
    if manual:
        how_many_to_move = input("\nHow many of the " + str(countryD[attack_from]["armies"] - 1) + " armies would you like to move? => ")
        # Move all armies by default
        if how_many_to_move == "":
            how_many_to_move = countryD[attack_from]["armies"] - 1
        else:
            how_many_to_move = int(how_many_to_move)

    # AUTOMATIC
    else:
        # Always move half the armies
        if countryD[attack_from]["armies"] == 0:
            how_many_to_move = 1
        else:
            how_many_to_move = (countryD[attack_from]["armies"] - 1) // 2
            if how_many_to_move == 0:
                how_many_to_move = 1

    return how_many_to_move

# Determine how many armies to move during troop movement phase
def troop_move(player, manual):
    if manual:
        troop_movement_candidate_from_list = []
        for country_key in countryD:
            if countryD[country_key]["owner"] == player and countryD[country_key]["armies"] > 1:
                for each_country in adjacentCountriesD[country_key]:
                    if countryD[each_country]["owner"] == player and country_key not in troop_movement_candidate_from_list:
                        troop_movement_candidate_from_list.append(country_key)

        # List choices to move armies from
        print("0. NO TROOP MOVEMENT")
        for idx in range(0, len(troop_movement_candidate_from_list)):
            print(str(idx + 1) + ". "+ troop_movement_candidate_from_list[idx])

        # Determine player choice
        from_choice = -1
        while from_choice < 0 or from_choice > len(troop_movement_candidate_from_list):
            from_choice = input("Troop Movement From? ")
            if from_choice.isnumeric() and from_choice != "0":
                from_choice = int(from_choice) - 1
            elif from_choice == "":
                return "", "", 0
            # Default is no movement
            else:
                return "", "", 0

        from_country = troop_movement_candidate_from_list[from_choice]

        # List choices to move armies to
        troop_movement_candidate_to_list = []
        for each in adjacentCountriesD[troop_movement_candidate_from_list[from_choice]]:
            if countryD[each]["owner"] == player:
                troop_movement_candidate_to_list.append(each)

        # List choices
        for idx in range(0, len(troop_movement_candidate_to_list)):
            print(str(idx) + ". " + troop_movement_candidate_to_list[idx])

        # Determine player choice
        to_choice = -1
        while to_choice < 0 or to_choice > len(troop_movement_candidate_to_list):
            to_choice = input("Troop Movement TO? ")
            if to_choice.isnumeric():
                to_choice = int(to_choice) - 1
            elif to_choice == "":
                to_choice = 0
            else:
                return "", "", 0

        how_many_to_move = -1
        while how_many_to_move < 0 or how_many_to_move > countryD[troop_movement_candidate_from_list[from_choice]]["armies"] - 1:
            how_many_to_move = input("\nHow many of the " + str(countryD[from_country]["armies"] - 1) + " armies would you like to move? => ")
            if how_many_to_move.isnumeric():
                how_many_to_move = int(how_many_to_move)
            else:
                how_many_to_move = countryD[troop_movement_candidate_from_list[from_choice]]["armies"] - 1

    # AUTOMATIC
    else:
        # Build list to determine where to move armies from
        troop_movement_candidate_from_list = []
        for country_key in countryD:
            if countryD[country_key]["owner"] == player and countryD[country_key]["armies"] > 1:
                for each_country in adjacentCountriesD[country_key]:
                    if countryD[each_country]["owner"] == player and country_key not in troop_movement_candidate_from_list:
                        troop_movement_candidate_from_list.append(country_key)

        # If we can't move any extra armies
        if len(troop_movement_candidate_from_list) == 0 or len(troop_movement_candidate_from_list) == 1:
            return "", "", 0

        # Determine which player's countries have the largest army
        max_armies_from = ""
        for country in range(1, len(troop_movement_candidate_from_list)):
            if countryD[troop_movement_candidate_from_list[country]]["armies"] > countryD[troop_movement_candidate_from_list[country - 1]]["armies"]:
                max_armies_from = troop_movement_candidate_from_list[country]
            else:
                max_armies_from = troop_movement_candidate_from_list[country - 1]

        # Build list to determine where to move armies to
        troop_movement_candidate_to_list = []
        for each in adjacentCountriesD[max_armies_from]:
            if countryD[each]["owner"] == player:
                troop_movement_candidate_to_list.append(each)

        if len(troop_movement_candidate_to_list) == 0:
            return "", "", 0

        # Determine where to move armies to
        min_armies = ""
        for country in range(1, len(troop_movement_candidate_to_list)):
            if countryD[troop_movement_candidate_to_list[country]]["armies"] < countryD[troop_movement_candidate_to_list[country - 1]]["armies"]:
                min_armies = troop_movement_candidate_to_list[country]
            else:
                min_armies = troop_movement_candidate_to_list[country - 1]

        how_many_to_move = (countryD[max_armies_from]["armies"] - 1) // 2
        if how_many_to_move == 1:
            how_many_to_move = 0

    return max_armies_from, min_armies, how_many_to_move

# Determine where and how many armies to place
def place_armies(player, player_d_me, manual):
    country_list = get_player_country_list(player)

    if manual:
        # List choices
        for index in range(len(country_list)):
            print(str(index) + ". " + country_list[index])

        # Determine player country choice
        country_index = -1
        while country_index < 0 or country_index >= len(country_list):
            val_in = input("Player " + str(player) + ", WHERE do you wish to place armies? => ")
            if val_in == "":
                country_index = 0
            elif val_in.isnumeric():
                country_index = int(val_in)
            else:
                country_index = 0

        # Determine player army count choice
        number_of_armies_to_place = -1
        while number_of_armies_to_place < 1 or number_of_armies_to_place > player_d_me[player]["armies"]:
            val_in = input("HOW MANY of the " + str(player_d_me[player]["armies"]) + " armies do you wish to place in " + country_list[country_index] + " => ")
            if val_in == "":
                number_of_armies_to_place = player_d_me[player]["armies"]
            elif val_in.isnumeric():
                number_of_armies_to_place = int(val_in)
            else:
                number_of_armies_to_place = 0

    # AUTOMATIC
    else:
        # Randomly pick a country to place all armies
        number_of_armies_to_place = player_d_me[player]["armies"]
        country_index = random.randint(0, len(country_list) - 1)

    return country_list[country_index], number_of_armies_to_place
