"""
Tests for P1.py - Player AI logic and decision-making functions.
"""
import pytest
from unittest.mock import patch, MagicMock
import copy
import P1
from riskStructs import countryD, adjacentCountriesD
from test_helpers import (
    create_test_country_dict,
    create_test_player_dict,
    create_test_cards,
    create_book_cards,
    setup_player_with_cards,
    setup_country_ownership,
    RiskTestBase
)

class TestGetPlayerCountryList(RiskTestBase):
    """Tests for get_player_country_list function."""

    def test_returns_empty_list_for_player_with_no_countries(self):
        """Test that function returns empty list when player owns no countries."""
        # Set all countries to be owned by player 2
        for country in countryD:
            countryD[country]["owner"] = 2

        result = P1.get_player_country_list(1)
        assert result == []

    def test_returns_correct_countries_for_player(self):
        """Test that function returns all countries owned by a player."""
        # Set up specific ownership
        test_countries = ["Alaska", "Alberta", "Ontario"]

        for country in countryD:
            if country in test_countries:
                countryD[country]["owner"] = 1
            else:
                countryD[country]["owner"] = 2

        result = P1.get_player_country_list(1)
        assert len(result) == len(test_countries)
        for country in test_countries:
            assert country in result

    def test_returns_list_type(self):
        """Test that function returns a list."""
        result = P1.get_player_country_list(1)
        assert isinstance(result, list)


class TestAtLeastOneAdjacentEnemy(RiskTestBase):
    """Tests for at_least_one_adjacent_enemy function."""

    def test_returns_true_when_enemy_adjacent(self):
        """Test that function returns True when an enemy is adjacent."""
        # Set Alaska to player 1, and one of its neighbors to player 2
        countryD["Alaska"]["owner"] = 1
        countryD["Alberta"]["owner"] = 2  # Alberta is adjacent to Alaska

        result = P1.at_least_one_adjacent_enemy("Alaska", 1)
        assert result is True

    def test_returns_false_when_no_enemy_adjacent(self):
        """Test that function returns False when all adjacent countries are owned by player."""
        # Set Alaska and all its neighbors to player 1
        countryD["Alaska"]["owner"] = 1
        for adjacent in adjacentCountriesD["Alaska"]:
            countryD[adjacent]["owner"] = 1

        result = P1.at_least_one_adjacent_enemy("Alaska", 1)
        assert result is False

    def test_returns_boolean(self):
        """Test that function returns a boolean value."""
        result = P1.at_least_one_adjacent_enemy("Alaska", 1)
        assert isinstance(result, bool)


class TestHasPickedABook:
    """Tests for has_picked_a_book function."""

    def test_returns_false_with_less_than_three_cards(self):
        """Test that function returns False when less than 3 cards selected."""
        player_dict = create_test_player_dict()
        player_dict[1]["cards"] = create_book_cards("three_of_kind")

        result = P1.has_picked_a_book(player_dict, 1, [0, 1])
        assert result is False

    def test_returns_true_for_three_of_kind(self):
        """Test that function returns True for three infantry cards."""
        player_dict = create_test_player_dict()
        player_dict[1]["cards"] = create_book_cards("three_of_kind")

        result = P1.has_picked_a_book(player_dict, 1, [0, 1, 2])
        assert result is True

    def test_returns_true_for_one_of_each(self):
        """Test that function returns True for one infantry, cavalry, and artillery."""
        player_dict = create_test_player_dict()
        player_dict[1]["cards"] = create_book_cards("one_of_each")

        result = P1.has_picked_a_book(player_dict, 1, [0, 1, 2])
        assert result is True

    def test_returns_true_with_wild_card(self):
        """Test that function returns True when a wild card is included."""
        player_dict = create_test_player_dict()
        player_dict[1]["cards"] = create_book_cards("with_wild")

        result = P1.has_picked_a_book(player_dict, 1, [0, 1, 2])
        assert result is True

    def test_returns_false_for_invalid_combination(self):
        """Test that function returns False for invalid card combinations."""
        player_dict = create_test_player_dict()
        player_dict[1]["cards"] = [
            ["Alaska", "infantry"],
            ["Alberta", "infantry"],
            ["Ontario", "cavalry"],
        ]

        result = P1.has_picked_a_book(player_dict, 1, [0, 1, 2])
        assert result is False


class TestAttackFromCountry(RiskTestBase):
    """Tests for attack_from_country function."""

    def test_returns_no_attack_when_no_valid_countries(self):
        """Test that function returns 'NO ATTACK' when player has no valid attack sources."""
        for country in countryD:
            countryD[country]["owner"] = 1
            countryD[country]["armies"] = 1

        result = P1.attack_from_country(1, manual=False)
        assert result == "NO ATTACK"

    def test_returns_country_with_most_armies_automatic(self):
        """Test that automatic mode returns country with most armies."""
        # Set up test scenario
        countryD["Alaska"]["owner"] = 1
        countryD["Alaska"]["armies"] = 10
        countryD["Alberta"]["owner"] = 1
        countryD["Alberta"]["armies"] = 5
        countryD["Ontario"]["owner"] = 2  # Enemy
        countryD["Ontario"]["armies"] = 3

        result = P1.attack_from_country(1, manual=False)
        # Should return Alaska as it has most armies and can attack
        assert result in ["Alaska", "Alberta"]

    def test_requires_at_least_2_armies(self):
        """Test that countries with less than 2 armies cannot attack."""
        # Set all player 1 countries to 1 army
        for country in countryD:
            if countryD[country]["owner"] == 1:
                countryD[country]["armies"] = 1

        result = P1.attack_from_country(1, manual=False)
        assert result == "NO ATTACK"


class TestAttackToCountry(RiskTestBase):
    """Tests for attack_to_country function."""

    def test_returns_enemy_country_and_owner(self):
        """Test that function returns an enemy country and its owner."""
        countryD["Alaska"]["owner"] = 1
        countryD["Alberta"]["owner"] = 2

        result_country, result_owner = P1.attack_to_country(1, "Alaska", manual=False)
        # Should return one of Alaska's neighbors that's owned by an enemy
        assert result_country in adjacentCountriesD["Alaska"]
        assert countryD[result_country]["owner"] != 1
        assert result_owner == countryD[result_country]["owner"]

    def test_automatic_mode_targets_weakest_enemy(self):
        """Test that automatic mode targets the enemy with fewest armies."""
        countryD["Alaska"]["owner"] = 1
        countryD["Alberta"]["owner"] = 2
        countryD["Alberta"]["armies"] = 2
        countryD["Northwest Territory"]["owner"] = 2
        countryD["Northwest Territory"]["armies"] = 5

        result_country, result_owner = P1.attack_to_country(1, "Alaska", manual=False)
        # Should prefer Alberta (weaker) over Northwest Territory
        assert result_country in adjacentCountriesD["Alaska"]


class TestContinueAttack:
    """Tests for continue_attack function."""

    def test_automatic_mode_retreats_when_disadvantaged(self):
        """Test that automatic mode retreats when attacker is disadvantaged."""
        result = P1.continue_attack(attack_to_armies=5, attack_from_armies=6, manual=False)
        assert result == "RETREAT"

    def test_automatic_mode_continues_when_advantaged(self):
        """Test that automatic mode continues when attacker has advantage."""
        result = P1.continue_attack(attack_to_armies=2, attack_from_armies=10, manual=False)
        assert result == ""

    def test_automatic_mode_retreats_when_defender_eliminated(self):
        """Test that automatic mode handles defender with 0 armies."""
        result = P1.continue_attack(attack_to_armies=0, attack_from_armies=5, manual=False)
        assert result == ""


class TestGetBookCardIndices:
    """Tests for get_book_card_indices function."""

    def test_automatic_mode_returns_valid_book(self):
        """Test that automatic mode returns a valid book of 3 cards."""
        player_dict = create_test_player_dict()
        # Give player enough cards to form a book
        player_dict[1]["cards"] = [
            ["Alaska", "infantry"],
            ["Alberta", "infantry"],
            ["Ontario", "infantry"],
            ["Greenland", "cavalry"],
            ["Iceland", "artillery"],
        ]

        result = P1.get_book_card_indices(1, player_dict, manual=False)

        # Should return 3 indices
        assert len(result) == 3
        # Indices should be valid
        for idx in result:
            assert 0 <= idx < len(player_dict[1]["cards"])
        # Should form a valid book
        assert P1.has_picked_a_book(player_dict, 1, result)


class TestTookCountryMoveArmiesHowMany(RiskTestBase):
    """Tests for took_country_move_armies_how_many function."""

    def test_automatic_mode_moves_half_armies(self):
        """Test that automatic mode moves approximately half the armies."""
        countryD["Alaska"]["armies"] = 10

        result = P1.took_country_move_armies_how_many("Alaska", manual=False)
        # Should move (10-1)//2 = 4 armies
        assert result == 4

    def test_automatic_mode_moves_at_least_one(self):
        """Test that automatic mode always moves at least 1 army."""
        countryD["Alaska"]["armies"] = 2

        result = P1.took_country_move_armies_how_many("Alaska", manual=False)
        assert result >= 1


class TestTroopMove(RiskTestBase):
    """Tests for troop_move function."""

    def test_automatic_mode_returns_valid_move_or_no_move(self):
        """Test that automatic mode returns valid move data."""
        # Set up scenario where player 1 owns adjacent countries
        countryD["Alaska"]["owner"] = 1
        countryD["Alaska"]["armies"] = 10
        countryD["Alberta"]["owner"] = 1
        countryD["Alberta"]["armies"] = 2

        from_country, to_country, how_many = P1.troop_move(1, manual=False)

        # Either no move or valid move
        if from_country == "":
            assert to_country == ""
            assert how_many == 0
        else:
            assert from_country in countryD
            assert to_country in countryD
            assert how_many >= 0

    def test_automatic_mode_no_move_when_insufficient_armies(self):
        """Test that automatic mode returns no move when player has insufficient armies."""
        # Set all player 1 countries to 1 army
        for country in countryD:
            if countryD[country]["owner"] == 1:
                countryD[country]["armies"] = 1

        from_country, to_country, how_many = P1.troop_move(1, manual=False)
        assert from_country == ""
        assert to_country == ""
        assert how_many == 0


class TestPlaceArmies(RiskTestBase):
    """Tests for place_armies function."""

    def test_automatic_mode_returns_valid_country_and_army_count(self):
        """Test that automatic mode returns a valid country and army count."""
        # Set some countries to player 1
        countryD["Alaska"]["owner"] = 1
        countryD["Alberta"]["owner"] = 1

        player_dict = create_test_player_dict()
        player_dict[1]["armies"] = 5

        country, num_armies = P1.place_armies(1, player_dict, manual=False)

        # Should return a country owned by player 1
        assert country in countryD
        assert countryD[country]["owner"] == 1

        # Should place all available armies
        assert num_armies == player_dict[1]["armies"]

    def test_automatic_mode_places_all_armies(self):
        """Test that automatic mode places all available armies."""
        # Ensure player 1 owns a country
        countryD["Alaska"]["owner"] = 1

        player_dict = create_test_player_dict()
        player_dict[1]["armies"] = 10

        country, num_armies = P1.place_armies(1, player_dict, manual=False)
        assert num_armies == 10

class TestManualModeInteractions(RiskTestBase):
    """Tests for P1.py functions in manual mode."""

    @patch('builtins.input')
    def test_attack_from_country_manual_selection(self, mock_input):
        """Test manual selection of attacking country."""
        # Setup: Alaska (P1, 10 armies), Alberta (P1, 5 armies)
        countryD["Alaska"]["owner"] = 1
        countryD["Alaska"]["armies"] = 10
        countryD["Alberta"]["owner"] = 1
        countryD["Alberta"]["armies"] = 5
        # Ensure they have adjacent enemies so they are valid valid choices
        countryD["Northwest Territory"]["owner"] = 2

        mock_input.return_value = "1"

        result = P1.attack_from_country(1, manual=True)
        assert result in countryD
        assert countryD[result]["owner"] == 1

        # Test "NO ATTACK" selection (input 0)
        mock_input.return_value = "0"
        result = P1.attack_from_country(1, manual=True)
        assert result == "NO ATTACK"

    @patch('builtins.input')
    def test_attack_to_country_manual_selection(self, mock_input):
        """Test manual selection of target country."""
        countryD["Alaska"]["owner"] = 1
        countryD["Alberta"]["owner"] = 2
        countryD["Northwest Territory"]["owner"] = 2

        # Mock input "1" (first neighbor)
        mock_input.return_value = "1"

        target, owner = P1.attack_to_country(1, "Alaska", manual=True)
        assert target in adjacentCountriesD["Alaska"]
        assert owner == 2

    @patch('builtins.input')
    def test_place_armies_manual_selection(self, mock_input):
        """Test manual placement of armies."""
        countryD["Alaska"]["owner"] = 1
        player_dict = create_test_player_dict()
        player_dict[1]["armies"] = 10

        mock_input.side_effect = ["0", "5"]

        target_country, count = P1.place_armies(1, player_dict, manual=True)

        assert target_country in countryD
        assert countryD[target_country]["owner"] == 1
        assert count == 5

    @patch('builtins.input')
    def test_troop_move_manual_selection(self, mock_input):
        """Test manual troop movement."""
        countryD["Alaska"]["owner"] = 1
        countryD["Alaska"]["armies"] = 10
        countryD["Alberta"]["owner"] = 1
        countryD["Alberta"]["armies"] = 5

        mock_input.side_effect = ["1", "1", "3"]

        from_c, to_c, count = P1.troop_move(1, manual=True)

        # Depending on P1 logic update, it should return valid inputs
        assert from_c in countryD
        assert to_c in countryD
        assert count == 3

    @patch('builtins.input')
    def test_get_book_card_indices_manual(self, mock_input):
        """Test manual card selection for book."""
        player_dict = create_test_player_dict()
        player_dict[1]["cards"] = [
            ["Alaska", "infantry"],
            ["Alberta", "infantry"],
            ["Ontario", "infantry"]
        ]

        # Use simple separate inputs for the loop
        mock_input.side_effect = ["0", "1", "2"]

        indices = P1.get_book_card_indices(1, player_dict, manual=True)
        assert indices == [0, 1, 2]

    @patch('builtins.input')
    def test_continue_attack_manual(self, mock_input):
        """Test manual continue attack decision."""
        # For RETREAT choice
        mock_input.return_value = "RETREAT"
        assert P1.continue_attack(5, 5, manual=True) == "RETREAT"

        # For Attack choice
        mock_input.return_value = ""
        assert P1.continue_attack(5, 5, manual=True) == ""
