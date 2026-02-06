"""
Tests for Risk.py - Main game engine and logic.
"""
import pytest
from unittest.mock import patch, MagicMock, call
import Risk
from riskStructs import countryD, adjacentCountriesD, continentD, armiesPerContinentD
from test_helpers import (
    create_test_country_dict,
    create_test_player_dict,
    create_book_cards,
    MockTurtle,
    RiskTestBase
)

# Constants for testing
ALASKA = "Alaska"
ALBERTA = "Alberta"

class TestNextPlayer:
    """Tests for nextplayer function."""

    def test_next_player_cycles_correctly(self):
        """Test that player numbers cycle 1 -> 2 -> 3 -> 4 -> 1."""
        assert Risk.nextplayer(1) == 2
        assert Risk.nextplayer(2) == 3
        assert Risk.nextplayer(3) == 4
        assert Risk.nextplayer(4) == 1

class TestStillArmiesToPlace:
    """Tests for stillarmiestoplace function."""

    def test_returns_true_when_armies_remain(self):
        """Test true when player has > 0 armies."""
        Risk.playerd[1]["armies"] = 5
        assert Risk.stillarmiestoplace(1) is True

    def test_returns_false_when_no_armies(self):
        """Test false when player has 0 armies."""
        Risk.playerd[1]["armies"] = 0
        assert Risk.stillarmiestoplace(1) is False

class TestGameOver(RiskTestBase):
    """Tests for gameover function."""

    def test_returns_true_when_one_player_owns_all(self):
        """Test game over when single owner for all countries."""
        for k in countryD:
            countryD[k]["owner"] = 1
        assert Risk.gameover() is True

    def test_returns_false_when_multiple_owners(self):
        """Test game continues when mixed ownership."""
        for k in countryD:
            countryD[k]["owner"] = 1
        countryD[ALASKA]["owner"] = 2
        assert Risk.gameover() is False

class TestCalcBaseArmies(RiskTestBase):
    """Tests for calcbasearmiesbeginningofturn function."""

    def test_minimum_armies_is_three(self):
        """Test always returns at least 3 armies."""
        # Give player 1 country (1 // 3 = 0, so should return 3)
        for k in countryD:
            countryD[k]["owner"] = 0
        countryD[ALASKA]["owner"] = 1

        assert Risk.calcbasearmiesbeginningofturn(1) == 3

    def test_calculates_based_on_country_count(self):
        """Test returns count // 3."""
        # Give player 12 countries (12 // 3 = 4)
        countries = list(countryD.keys())[:12]
        for k in countryD:
            countryD[k]["owner"] = 0
        for k in countries:
            countryD[k]["owner"] = 1

        assert Risk.calcbasearmiesbeginningofturn(1) == 4

class TestFindContinentsBonus(RiskTestBase):
    """Tests for findcontinentsbonusbeginningofturn function."""

    def test_returns_zero_when_no_continents_owned(self):
        """Test 0 bonus when owning scattered countries."""
        for k in countryD:
            countryD[k]["owner"] = 0

        # Give one country from each continent
        for cont in continentD:
            first_country = continentD[cont][0]
            countryD[first_country]["owner"] = 1

        assert Risk.findcontinentsbonusbeginningofturn(1) == 0

    def test_returns_correct_bonus_for_continent(self):
        """Test correct bonus when owning entire continent."""
        for k in countryD:
            countryD[k]["owner"] = 0

        # Give all Australia
        total_bonus = 0
        for cont_name, countries in continentD.items():
             # testing with Australia as it is small
            if cont_name == "Australia":
                for country in countries:
                    countryD[country]["owner"] = 1
                total_bonus = armiesPerContinentD[cont_name]
                break

        assert Risk.findcontinentsbonusbeginningofturn(1) == total_bonus

class TestCreateCards:
    """Tests for createcards function."""

    def test_creates_correct_number_of_cards(self):
        """Test total card count (42 countries + 2 wild)."""
        # Note: createcards pops from the input list, so we pass a copy
        dummy_country_d = {k: {} for k in countryD}
        cards = Risk.createcards(dummy_country_d)

        # 42 countries + 2 wild cards = 44
        assert len(cards) == 44

    def test_contains_all_types(self):
        """Test deck contains infantry, cavalry, artillery, and wild."""
        dummy_country_d = {k: {} for k in countryD}
        cards = Risk.createcards(dummy_country_d)

        types = set(card[1] for card in cards)
        assert "infantry" in types
        assert "cavalry" in types
        assert "artillery" in types
        assert "wild" in types

class TestHasABook:
    """Tests for has_a_book function."""

    def setup_method(self):
        self.original_cards = Risk.playerd[1]["cards"]

    def teardown_method(self):
        Risk.playerd[1]["cards"] = self.original_cards

    def test_returns_false_with_few_cards(self):
        """Test false when < 3 cards."""
        Risk.playerd[1]["cards"] = [["A", "infantry"], ["B", "cavalry"]]
        assert Risk.has_a_book(1) is False

    def test_returns_true_three_same(self):
        """Test true for 3 of same type."""
        Risk.playerd[1]["cards"] = [
            ["A", "infantry"], ["B", "infantry"], ["C", "infantry"]
        ]
        assert Risk.has_a_book(1) is True

    def test_returns_true_one_each(self):
        """Test true for 1 of each type."""
        Risk.playerd[1]["cards"] = [
            ["A", "infantry"], ["B", "cavalry"], ["C", "artillery"]
        ]
        assert Risk.has_a_book(1) is True

    def test_returns_true_with_wild(self):
        """Test true with wild card."""
        Risk.playerd[1]["cards"] = [
            ["A", "infantry"], ["B", "infantry"], ["Wild", "wild"]
        ]
        assert Risk.has_a_book(1) is True

class TestDiceFunctions:
    """Tests for dice drawing and rolling logic."""

    @patch('Risk.drawrectangle')
    def test_drawdice_logic(self, mock_draw):
        """Test army increment logic in drawdice."""
        mock_t = MagicMock()

        # Attacker wins [6] vs [5]
        adice = [6]
        ddice = [5]
        a_inc, d_inc = Risk.drawdice(mock_t, adice, ddice)
        assert a_inc == 0
        assert d_inc == -1

        # Defender wins [4] vs [5]
        adice = [4]
        ddice = [5]
        a_inc, d_inc = Risk.drawdice(mock_t, adice, ddice)
        assert a_inc == -1
        assert d_inc == 0

        # Mixed result checks
        # A: [6, 4], D: [5, 3] -> A wins first (6vs5), A wins second (4vs3)
        adice = [6, 4]
        ddice = [5, 3]
        a_inc, d_inc = Risk.drawdice(mock_t, adice, ddice)
        assert a_inc == 0
        assert d_inc == -2

        # Draw goes to defender
        # A: [5], D: [5]
        adice = [5]
        ddice = [5]
        a_inc, d_inc = Risk.drawdice(mock_t, adice, ddice)
        assert a_inc == -1
        assert d_inc == 0

    @patch('Risk.drawrectangle')
    def test_rolldice_integration(self, mock_draw):
        """Test rolldice updates armies correctly."""
        mock_t = MagicMock()

        # Setup specific scenario
        countryD["AttackerLand"] = {"loc": [0,0], "owner": 1, "armies": 10}
        countryD["DefenderLand"] = {"loc": [10,10], "owner": 2, "armies": 5}

        # Mock random to control dice
        with patch('random.randint', side_effect=[6, 6, 6, 1, 1]):
            Risk.rolldice(mock_t, 1, "AttackerLand", "DefenderLand")

            assert countryD["DefenderLand"]["armies"] == 3 # 5 - 2
            assert countryD["AttackerLand"]["armies"] == 10 # Unchanged

        # Clean up
        del countryD["AttackerLand"]
        del countryD["DefenderLand"]

class TestNoDefendingPlayerLeft(RiskTestBase):
    """Tests for nodefendingplayerleft function."""

    def test_true_when_player_eliminated(self):
        """Test true when player owns no countries."""
        # Set all to player 1
        for k in countryD:
            countryD[k]["owner"] = 1

        assert Risk.nodefendingplayerleft(2) is True

    def test_false_when_player_exists(self):
        """Test false when player owns countries."""
        for k in countryD:
            countryD[k]["owner"] = 1
        countryD[ALASKA]["owner"] = 2

        assert Risk.nodefendingplayerleft(2) is False

class TestRiskUIFunctions(RiskTestBase):
    """Tests for Risk.py UI and game loop functions."""

    @patch('turtle.Turtle')
    @patch('turtle.Screen')
    def test_drawplayerboxes(self, mock_screen, mock_turtle):
        """Test drawplayerboxes function."""
        t = mock_turtle.return_value
        Risk.drawplayerboxes(t, 10, [1, 2])
        # Verify turtle calls were made
        assert t.up.called
        assert t.goto.called
        assert t.down.called

    @patch('turtle.Turtle')
    def test_armyplacement_manual(self, mock_turtle):
        """Test armyplacement function (manual)."""
        t = mock_turtle.return_value

        # Ensure manual mode is active
        # Assuming P1 needs manual flag passed or Risk.manual variable used
        # armyplacement calls P1.place_armies(..., manual)
        # It uses global manual in Risk.py.
        # We patch it.
        with patch('Risk.manual', True):
            # Mock inputs: Country "Alaska", Armies "1" (0 selects Alaska, 1 selects 1 army)
            with patch('builtins.input', side_effect=["0", "1"]):
                 # Setup player 1 with armies
                 from Risk import playerd
                 playerd[1]["armies"] = 5

                 # Setup country owner
                 countryD["Alaska"]["owner"] = 1
                 countryD["Alaska"]["armies"] = 1
                 saved_armies = countryD["Alaska"]["armies"]

                 Risk.armyplacement(1, t)

                 # Verify armies placed
                 assert countryD["Alaska"]["armies"] == saved_armies + 1
                 assert playerd[1]["armies"] == 4

    @patch('turtle.Turtle')
    def test_troop_movement_ui(self, mock_turtle):
        """Test troop_movement UI wrapper."""
        t = mock_turtle.return_value

        with patch('P1.troop_move', return_value=("Alaska", "Alberta", 2)):
             # Setup
             countryD["Alaska"]["owner"] = 1
             countryD["Alaska"]["armies"] = 5
             countryD["Alberta"]["owner"] = 1
             countryD["Alberta"]["armies"] = 5

             original_alaska = countryD["Alaska"]["armies"]
             original_alberta = countryD["Alberta"]["armies"]

             Risk.troop_movement(1, t)

             assert countryD["Alaska"]["armies"] == original_alaska - 2
             assert countryD["Alberta"]["armies"] == original_alberta + 2
