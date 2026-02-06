"""
Shared test helpers and fixtures to minimize code duplication across test files.
"""
import copy
from unittest.mock import Mock, MagicMock
from riskStructs import countryD


class MockTurtle:
    """Mock turtle object for testing graphics-dependent functions."""

    def __init__(self):
        self.position = (0, 0)
        self.heading_angle = 0
        self.pen_down = True
        self.fill_color = "black"
        self.pen_color = "black"
        self.hidden = False
        self.drawings = []
        self.writes = []

    def up(self):
        self.pen_down = False

    def down(self):
        self.pen_down = True

    def goto(self, x, y):
        self.position = (x, y)
        if self.pen_down:
            self.drawings.append(("goto", x, y))

    def forward(self, distance):
        self.drawings.append(("forward", distance))

    def right(self, angle):
        self.heading_angle = (self.heading_angle - angle) % 360

    def left(self, angle):
        self.heading_angle = (self.heading_angle + angle) % 360

    def fillcolor(self, color):
        self.fill_color = color

    def color(self, color):
        self.pen_color = color

    def begin_fill(self):
        self.drawings.append(("begin_fill",))

    def end_fill(self):
        self.drawings.append(("end_fill",))

    def write(self, text, font=None):
        self.writes.append((text, font))

    def ht(self):
        """Hide turtle."""
        self.hidden = True

    def clear(self):
        """Clear drawings."""
        self.drawings = []
        self.writes = []


def create_mock_turtle():
    """Factory function to create a fresh MockTurtle instance."""
    return MockTurtle()


class RiskTestBase:
    """Base class for Risk tests handling common setup/teardown."""

    def setup_method(self):
        """Save original state of countryD."""
        self.original_countryD_state = {}
        for country in countryD:
            self.original_countryD_state[country] = {
                "owner": countryD[country]["owner"],
                "armies": countryD[country].get("armies", 0),
                "loc": countryD[country].get("loc", [0, 0])
            }
        # We might need to save playerd state too if tests modify it extensively
        # But usually tests modify playerd directly imported or mocked.
        # If tests import playerd from Risk, we should save it.
        # Here we assume countryD is the main persistent state riskStructs.

    def teardown_method(self):
        """Restore original state."""
        for country, state in self.original_countryD_state.items():
            countryD[country]["owner"] = state["owner"]
            countryD[country]["armies"] = state["armies"]


def create_test_country_dict():
    """Create a minimal country dictionary for testing."""
    return {
        "Alaska": {"loc": [-372, 161], "owner": 1, "armies": 3},
        "Alberta": {"loc": [-301, 118], "owner": 1, "armies": 5},
        "Ontario": {"loc": [-243, 110], "owner": 2, "armies": 2},
        "Greenland": {"loc": [-149, 196], "owner": 2, "armies": 4},
        "Iceland": {"loc": [-71, 140], "owner": 3, "armies": 1},
        "Scandinavia": {"loc": [-6, 130], "owner": 3, "armies": 6},
    }


def create_test_player_dict():
    """Create a minimal player dictionary for testing."""
    return {
        1: {"armies": 10, "color": "green", "loc": (-350, 257), "cards": []},
        2: {"armies": 8, "color": "blue", "loc": (220, 257), "cards": []},
        3: {"armies": 5, "color": "purple", "loc": (220, -289), "cards": []},
        4: {"armies": 0, "color": "red", "loc": (-350, -289), "cards": []},
    }


def create_test_cards():
    """Create a minimal card list for testing."""
    return [
        ["Alaska", "infantry"],
        ["Alberta", "cavalry"],
        ["Ontario", "artillery"],
        ["wild", "wild"],
        ["Greenland", "infantry"],
        ["Iceland", "cavalry"],
    ]


def setup_player_with_cards(player_dict, player_num, cards):
    """Helper to set up a player with specific cards."""
    player_dict[player_num]["cards"] = copy.deepcopy(cards)
    return player_dict


def setup_country_ownership(country_dict, country_name, owner, armies=1):
    """Helper to set up country ownership and army count."""
    if country_name in country_dict:
        country_dict[country_name]["owner"] = owner
        country_dict[country_name]["armies"] = armies
    return country_dict


def create_book_cards(book_type="three_of_kind"):
    """
    Create cards that form a valid book.

    Args:
        book_type: "three_of_kind", "one_of_each", or "with_wild"
    """
    if book_type == "three_of_kind":
        return [
            ["Alaska", "infantry"],
            ["Alberta", "infantry"],
            ["Ontario", "infantry"],
        ]
    elif book_type == "one_of_each":
        return [
            ["Alaska", "infantry"],
            ["Alberta", "cavalry"],
            ["Ontario", "artillery"],
        ]
    elif book_type == "with_wild":
        return [
            ["Alaska", "infantry"],
            ["Alberta", "cavalry"],
            ["wild", "wild"],
        ]
    else:
        return []


def assert_valid_country_dict(country_dict):
    """Assert that a country dictionary has valid structure."""
    assert isinstance(country_dict, dict), "Country dict must be a dictionary"
    # Basic size check if testing full game data
    if len(country_dict) == 42:
        pass # Expected for full game

    for country_name, country_data in country_dict.items():
        assert isinstance(country_name, str), f"Country name must be string: {country_name}"
        assert "loc" in country_data, f"Country {country_name} missing 'loc'"
        assert "owner" in country_data, f"Country {country_name} missing 'owner'"
        assert isinstance(country_data["loc"], list), f"Country {country_name} loc must be list"
        assert len(country_data["loc"]) == 2, f"Country {country_name} loc must have 2 elements"
        assert isinstance(country_data["owner"], int), f"Country {country_name} owner must be int"
        assert 0 <= country_data["owner"] <= 4, f"Country {country_name} owner invalid"


def assert_valid_adjacency_dict(adj_dict, country_dict):
    """Assert adjacency dictionary validity."""
    assert isinstance(adj_dict, dict)
    for country, adjacents in adj_dict.items():
        assert country in country_dict
        assert isinstance(adjacents, list)
        assert len(adjacents) > 0
        for adj in adjacents:
            assert adj in country_dict
            # Symmetry check
            assert country in adj_dict[adj], f"Asymmetry: {country}->{adj} but not vice versa"
            # Self-adjacency check
            assert country != adj, f"Self-adjacency: {country}"


def assert_valid_continent_dict(cont_dict, country_dict):
    """Assert continent dictionary validity."""
    assert isinstance(cont_dict, dict)
    assert len(cont_dict) == 6
    all_countries = set()
    for cont, countries in cont_dict.items():
        assert isinstance(countries, list)
        assert len(countries) > 0
        for c in countries:
            assert c in country_dict
            assert c not in all_countries, f"Duplicate country in continents: {c}"
            all_countries.add(c)

    assert len(all_countries) == len(country_dict), "Continent country count mismatch"


def assert_valid_armies_per_continent(armies_dict, cont_dict):
    """Assert army bonus dictionary validity."""
    assert isinstance(armies_dict, dict)
    assert len(armies_dict) == len(cont_dict)
    for cont, bonus in armies_dict.items():
        assert cont in cont_dict
        assert isinstance(bonus, int)
        assert bonus > 0


def assert_valid_player_dict(player_dict):
    """Assert that a player dictionary has valid structure."""
    assert isinstance(player_dict, dict), "Player dict must be a dictionary"
    for player_num, player_data in player_dict.items():
        assert isinstance(player_num, int), f"Player number must be int: {player_num}"
        assert "armies" in player_data, f"Player {player_num} missing 'armies'"
        assert "color" in player_data, f"Player {player_num} missing 'color'"
        assert "loc" in player_data, f"Player {player_num} missing 'loc'"
        assert "cards" in player_data, f"Player {player_num} missing 'cards'"
        assert isinstance(player_data["cards"], list), f"Player {player_num} cards must be list"


def reset_country_dict_state(country_dict):
    """Reset all countries to unowned state with 0 armies."""
    for country in country_dict:
        country_dict[country]["owner"] = 0
        country_dict[country]["armies"] = 0
    return country_dict
