# Country list with locations and owners
countryD = {
    "Alaska": {"loc": [-372, 161], "owner": 0}, 
    "Northwest Territory": {"loc": [-292, 165], "owner": 0}, 
    "Greenland": {"loc": [-149, 196], "owner": 0}, 
    "Alberta": {"loc": [-301, 118], "owner": 0}, 
    "Ontario": {"loc": [-243, 110], "owner": 0}, 
    "Eastern Canada": {"loc": [-197, 106], "owner": 0}, 
    "Western United States": {"loc": [-294, 54], "owner": 0}, 
    "Eastern United States": {"loc": [-231, 38], "owner": 0}, 
    "Central America": {"loc": [-276, 5], "owner": 0}, 
    
    "Venezuela": {"loc": [-233, -40], "owner": 0}, 
    "Peru": {"loc": [-206, -106], "owner": 0}, 
    "Brazil": {"loc": [-165, -90], "owner": 0}, 
    "Argentina": {"loc": [-183, -143], "owner": 0}, 
    
    "North Africa": {"loc": [-38, -77], "owner": 0}, 
    "Egypt": {"loc": [30, -50], "owner": 0}, 
    "East Africa": {"loc": [55, -99], "owner": 0}, 
    "Central Africa": {"loc": [23, -108], "owner": 0}, 
    "South Africa": {"loc": [25, -195], "owner": 0}, 
    "Madagascar": {"loc": [116, -190], "owner": 0}, 
    
    "Western Europe": {"loc": [-77, 3], "owner": 0}, 
    "Southern Europe": {"loc": [0, 23], "owner": 0}, 
    "Northern Europe": {"loc": [-28, 67], "owner": 0}, 
    "Russia": {"loc": [64, 117], "owner": 0}, 
    "Great Britain": {"loc": [-92, 73], "owner": 0}, 
    "Iceland": {"loc": [-71, 140], "owner": 0}, 
    "Scandinavia": {"loc": [-6, 130], "owner": 0}, 
    
    "Ural": {"loc": [149, 120], "owner": 0}, 
    "Siberia": {"loc": [193, 142], "owner": 0}, 
    "Yakutsk": {"loc": [249, 185], "owner": 0}, 
    "Kamchatka": {"loc": [313, 186], "owner": 0}, 
    "Irkutsk": {"loc": [226, 121], "owner": 0}, 
    "Japan": {"loc": [343, 68], "owner": 0}, 
    "Mongolia": {"loc": [243, 76], "owner": 0}, 
    "China": {"loc": [222, 30], "owner": 0}, 
    "Afghanistan": {"loc": [127, 53], "owner": 0}, 
    "Middle East": {"loc": [72, -5], "owner": 0}, 
    "India": {"loc": [169, -13], "owner": 0}, 
    "Southeast Asia": {"loc": [235, -4], "owner": 0}, 

    "Indonesia": {"loc": [231, -104], "owner": 0}, 
    "New Guinea": {"loc": [304, -87], "owner": 0}, 
    "Western Australia": {"loc": [262, -174], "owner": 0}, 
    "Eastern Australia": {"loc": [338, -156], "owner": 0}}

# List of countries and countries adjacent to them
adjacentCountriesD = {"Alaska": ["Kamchatka", "Northwest Territory", "Alberta"], 
    "Northwest Territory": ["Alaska", "Alberta", "Ontario", "Greenland", ], 
    "Greenland": ["Northwest Territory", "Ontario", "Eastern Canada", "Iceland"], 
    "Alberta": ["Alaska", "Northwest Territory", "Ontario", "Western United States"], 
    "Ontario": ["Greenland", "Alberta", "Western United States", "Eastern United States", "Eastern Canada", "Northwest Territory"], 
    "Eastern Canada": ["Eastern United States", "Ontario", "Greenland"], 
    "Western United States": ["Alberta", "Ontario", "Eastern United States", "Central America"], 
    "Eastern United States": ["Ontario", "Eastern Canada", "Western United States", "Central America"], 
    "Central America": ["Western United States", "Eastern United States", "Venezuela"], 
    
    "Venezuela": ["Central America", "Peru", "Brazil"], 
    "Peru": ["Argentina", "Brazil", "Venezuela"], 
    "Brazil": ["Argentina", "Peru", "Venezuela", "North Africa"], 
    "Argentina": ["Peru", "Brazil"], 
    
    "North Africa": ["Brazil", "Western Europe", "Southern Europe", "Egypt", "East Africa", "Central Africa"], 
    "Egypt": ["Southern Europe", "Middle East", "East Africa", "North Africa"], 
    "East Africa": ["Middle East", "Central Africa", "Madagascar", "Egypt", "South Africa", "North Africa"], 
    "Central Africa": ["North Africa", "East Africa", "South Africa"], 
    "South Africa": ["Central Africa", "East Africa", "Madagascar"], 
    "Madagascar": ["South Africa", "East Africa"], 
    
    "Western Europe": ["Great Britain", "Northern Europe", "Southern Europe", "North Africa"], 
    "Southern Europe": ["Western Europe", "Northern Europe", "Russia", "Middle East", "Egypt", "North Africa"], 
    "Northern Europe": ["Great Britain", "Scandinavia", "Russia", "Southern Europe", "Western Europe"], 
    "Russia": ["Southern Europe", "Northern Europe", "Scandinavia", "Ural", "Afghanistan", "Middle East"], 
    "Great Britain": ["Iceland", "Scandinavia", "Northern Europe", "Western Europe"], 
    "Iceland": ["Greenland", "Scandinavia", "Great Britain"], 
    "Scandinavia": ["Iceland", "Russia", "Northern Europe", "Great Britain"], 
    
    "Ural": ["Russia", "Siberia", "China", "Afghanistan"], 
    "Siberia": ["Ural", "Yakutsk", "Irkutsk", "Mongolia", "China"], 
    "Yakutsk": ["Siberia", "Irkutsk", "Kamchatka"], 
    "Kamchatka": ["Alaska", "Japan", "Yakutsk", "Irkutsk", "Mongolia"], 
    "Irkutsk": ["Siberia", "Yakutsk", "Kamchatka", "Mongolia"], 
    "Japan": ["Kamchatka", "Mongolia"], 
    "Mongolia": ["Japan", "Kamchatka", "China", "Siberia", "Irkutsk"], 
    "China": ["Mongolia", "Southeast Asia", "India", "Afghanistan", "Ural", "Siberia"], 
    "Afghanistan": ["Russia", "Ural", "China", "India", "Middle East"], 
    "Middle East": ["Southern Europe", "Russia", "Afghanistan", "India", "East Africa", "Egypt"], 
    "India": ["Middle East", "Afghanistan", "China", "Southeast Asia"], 
    "Southeast Asia": ["Indonesia", "India", "China"], 

    "Indonesia": ["Southeast Asia", "Western Australia", "New Guinea"], 
    "New Guinea": ["Eastern Australia", "Western Australia", "Indonesia"], 
    "Western Australia": ["Indonesia", "Eastern Australia", "New Guinea"], 
    "Eastern Australia": ["New Guinea", "Western Australia"]
}

# List of which countries makeup each continent
continentD = {"Asia": ["Ural", "Siberia", "Yakutsk", "Kamchatka", "Irkutsk", "Japan", "Mongolia", "China", "Afghanistan", "Middle East", "India", "Southeast Asia"], 
            "North America": ["Alaska", "Northwest Territory", "Greenland", "Alberta", "Ontario", "Eastern Canada", "Western United States", "Eastern United States", "Central America"], 
            "Europe": ["Western Europe", "Southern Europe", "Northern Europe", "Russia", "Great Britain", "Iceland", "Scandinavia"], 
            "Africa": ["North Africa", "Egypt", "East Africa", "Central Africa", "South Africa", "Madagascar"], 
            "Australia": ["Indonesia", "New Guinea", "Western Australia", "Eastern Australia"], 
            "South America": ["Venezuela", "Peru", "Brazil", "Argentina"]}

# Bonus armies if a player owns a whole continent
armiesPerContinentD = {"Asia": 7, 
                     "North America": 5, 
                     "Europe": 5, 
                     "Africa": 3, 
                     "Australia": 2, 
                     "South America": 2}
