"""
Tests for riskStructs.py - Country, continent, and adjacency data structures.
"""
import pytest
from riskStructs import (
    countryD, adjacentCountriesD, continentD, armiesPerContinentD,
    ALASKA, ALBERTA, ONTARIO, GREENLAND, ICELAND, SCANDINAVIA,
    NORTH_AMERICA, EUROPE, ASIA, AFRICA, AUSTRALIA, SOUTH_AMERICA
)
from test_helpers import (
    assert_valid_country_dict,
    assert_valid_adjacency_dict,
    assert_valid_continent_dict,
    assert_valid_armies_per_continent
)

class TestCountryDictionary:
    """Tests for the country dictionary structure."""

    def test_country_dict_structure_and_validity(self):
        """Verify comprehensive validity of countryD using helper."""
        assert_valid_country_dict(countryD)
        assert len(countryD) == 42

    def test_specific_countries_exist(self):
        """Test that specific well-known countries exist."""
        expected_countries = [
            "Alaska", "Alberta", "Ontario", "Greenland",
            "Brazil", "Argentina", "Egypt", "Madagascar",
            "Iceland", "Great Britain", "Russia",
            "China", "India", "Japan"
        ]
        for country in expected_countries:
            assert country in countryD, f"{country} not found in countryD"


class TestAdjacentCountriesDictionary:
    """Tests for the adjacency relationships between countries."""

    def test_adjacency_dict_structure_and_validity(self):
        """Verify comprehensive validity of adjacentCountriesD using helper."""
        assert_valid_adjacency_dict(adjacentCountriesD, countryD)

    def test_alaska_kamchatka_adjacency(self):
        """Test the special cross-map adjacency between Alaska and Kamchatka."""
        assert "Kamchatka" in adjacentCountriesD["Alaska"]
        assert "Alaska" in adjacentCountriesD["Kamchatka"]

    def test_specific_adjacencies(self):
        """Test some specific known adjacencies."""
        # North America
        assert "Alberta" in adjacentCountriesD["Alaska"]
        assert "Ontario" in adjacentCountriesD["Alberta"]

        # Europe
        assert "Great Britain" in adjacentCountriesD["Iceland"]
        assert "Scandinavia" in adjacentCountriesD["Iceland"]

        # South America to Africa
        assert "North Africa" in adjacentCountriesD["Brazil"]


class TestContinentDictionary:
    """Tests for continent definitions."""

    def test_continent_dict_structure_and_validity(self):
        """Verify comprehensive validity of continentD using helper."""
        assert_valid_continent_dict(continentD, countryD)

    def test_all_continents_exist(self):
        """Test that all 6 continents are defined."""
        expected_continents = [NORTH_AMERICA, SOUTH_AMERICA, EUROPE, AFRICA, ASIA, AUSTRALIA]
        for continent in expected_continents:
            assert continent in continentD, f"{continent} not in continentD"

    def test_continent_sizes(self):
        """Test that continents have expected number of countries."""
        assert len(continentD[NORTH_AMERICA]) == 9
        assert len(continentD[SOUTH_AMERICA]) == 4
        assert len(continentD[EUROPE]) == 7
        assert len(continentD[AFRICA]) == 6
        assert len(continentD[ASIA]) == 12
        assert len(continentD[AUSTRALIA]) == 4


class TestArmiesPerContinent:
    """Tests for continent bonus armies."""

    def test_armies_per_continent_structure_and_validity(self):
        """Verify comprehensive validity of armiesPerContinentD using helper."""
        assert_valid_armies_per_continent(armiesPerContinentD, continentD)

    def test_specific_bonus_values(self):
        """Test specific known bonus values."""
        assert armiesPerContinentD[ASIA] == 7
        assert armiesPerContinentD[NORTH_AMERICA] == 5
        assert armiesPerContinentD[EUROPE] == 5
        assert armiesPerContinentD[AFRICA] == 3
        assert armiesPerContinentD[AUSTRALIA] == 2
        assert armiesPerContinentD[SOUTH_AMERICA] == 2

    def test_bonus_values_correlate_with_size(self):
        """Test that larger continents generally have higher bonuses."""
        # Asia is largest and should have highest bonus
        assert armiesPerContinentD[ASIA] == max(armiesPerContinentD.values())

        # Australia and South America are smallest and should have lowest bonuses
        small_continents = [AUSTRALIA, SOUTH_AMERICA]
        for continent in small_continents:
            assert armiesPerContinentD[continent] == 2


class TestCountryConstants:
    """Tests for country name constants."""

    def test_country_constants_match_dict_keys(self):
        """Test that country constants match actual dictionary keys."""
        test_constants = [
            (ALASKA, "Alaska"),
            (ALBERTA, "Alberta"),
            (ONTARIO, "Ontario"),
            (GREENLAND, "Greenland"),
            (ICELAND, "Iceland"),
            (SCANDINAVIA, "Scandinavia"),
        ]

        for constant, expected_value in test_constants:
            assert constant == expected_value
            assert constant in countryD


class TestDataIntegrity:
    """Integration tests for data consistency across all structures."""

    def test_no_isolated_countries(self):
        """Test that no country is completely isolated (has no adjacencies)."""
        # Partially covered by assert_valid_adjacency_dict, but double check explicit isolation
        for country in countryD.keys():
            adjacents = adjacentCountriesD.get(country, [])
            assert len(adjacents) > 0, f"{country} has no adjacent countries"

    def test_continent_internal_connectivity(self):
        """Test that countries within continents are generally connected."""
        # This is a basic check - at least some countries in each continent should be adjacent
        for continent, countries in continentD.items():
            if len(countries) > 1:
                # Check that at least one pair of countries in the continent are adjacent
                found_adjacency = False
                for country in countries:
                    for adjacent in adjacentCountriesD[country]:
                        if adjacent in countries:
                            found_adjacency = True
                            break
                    if found_adjacency:
                        break
                assert found_adjacency, f"No internal adjacencies found in {continent}"
