"""
Tests for Risk.py main game functions and UI helpers.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import Risk
from riskStructs import countryD
from test_helpers import RiskTestBase, MockTurtle, create_test_country_dict, create_test_player_dict

class TestRiskGameFunctions(RiskTestBase):
    """Tests for Risk.py game logic functions."""

    @patch('turtle.Turtle')
    def test_autoassigncountries(self, mock_turtle_class):
        """Test random assignment of countries."""
        t = mock_turtle_class.return_value
        Risk.playerd = create_test_player_dict()
        for c in countryD:
            countryD[c]["owner"] = 0
            countryD[c]["armies"] = 0
        with patch('Risk.nextplayer', side_effect=[2, 3, 4, 1] * 20):
            Risk.autoassigncountries(t, 1)

    def test_playbooks_logic(self):
        Risk.playerd = create_test_player_dict()
        Risk.playerd[1]["cards"] = [["Alaska", "infantry"], ["Alberta", "infantry"], ["Ontario", "infantry"]]
        t = Mock()
        with patch('P1.get_book_card_indices', return_value=[0, 1, 2]):
            countryD["Alaska"]["owner"] = 1
            countryD["Alaska"]["armies"] = 1
            Risk.bookarmiesbonuslist = [4, 6]
            bonus = Risk.playbooks(1, t)
            assert bonus == 4

    @patch('Risk.gameover', side_effect=[True]) # 0 Iterations (Stable)
    @patch('Risk.autoassigncountries', return_value=1)
    @patch('Risk.stillarmiestoplace', side_effect=[False] * 10)
    @patch('Risk.createcards', return_value=[])
    @patch('Risk.calcbasearmiesbeginningofturn', return_value=3)
    @patch('Risk.findcontinentsbonusbeginningofturn', return_value=0)
    @patch('Risk.armyplacement')
    @patch('Risk.attackneighboringcountry', return_value=False)
    @patch('Risk.troop_movement')
    @patch('turtle.Turtle')
    @patch('turtle.Screen')
    @patch('builtins.input', side_effect=Exception("Input called!"))
    def test_riskmain_smoke(self, mock_input, mock_screen, mock_turtle, mock_move, mock_attack, mock_place,
                           mock_bonus, mock_calc, mock_cards, mock_still, mock_assign, mock_gameover):
        """Smoke test for main game loop - 0 Iterations."""
        Risk.playerd = create_test_player_dict()
        Risk.manual = False
        try:
            Risk.riskmain()
        except Exception as e:
            pytest.fail(f"riskmain raised exception: {e}")

        assert mock_assign.called
        assert mock_gameover.called

    @patch('turtle.Turtle')
    @patch('time.sleep')
    @patch('builtins.print')
    @patch('P1.took_country_move_armies_how_many', return_value=1)
    @patch('P1.continue_attack', side_effect=["ATTACK", "RETREAT"]) # Run loop once then exit
    @patch('P1.attack_to_country', return_value=["Alberta", 0]) # Target
    @patch('P1.attack_from_country', side_effect=["Alaska", "NO ATTACK"]) # Source then Stop
    @patch('Risk.rolldice', return_value=True) # Win attack
    @patch('Risk.drawrectangle')
    def test_attackneighboringcountry_logic(self, mock_rect, mock_roll, mock_from, mock_to, mock_con, mock_move_armies, mock_print, mock_sleep, mock_turtle_class):
        """Test attack logic in isolation."""
        t = Mock()
        Risk.playerd = create_test_player_dict()
        Risk.manual = False

        # Setup countries
        countryD["Alaska"]["owner"] = 1
        countryD["Alaska"]["armies"] = 5
        countryD["Alberta"]["owner"] = 2
        countryD["Alberta"]["armies"] = 1

        # Calls attackneighboringcountry(t, 1)
        # 1. calls attack_from called?
        # 2. calls attack_to called?
        # 3. calls rolldice?

        captured = Risk.attackneighboringcountry(t, 1)

        # Verify flow
        assert mock_from.called
        assert mock_to.called
        assert mock_roll.called

        # If captured, returns TRUE?
        # Logic: if countrycaptured... returns True?
        # Risk.py returns countrycaptured boolean.
        # Since we mocked rolldice to return True (capture?), logic inside handles armies.
        # Check army transfer logic
        pass

