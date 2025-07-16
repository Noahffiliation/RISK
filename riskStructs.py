# Define country names as constants
ALASKA = "Alaska"
NORTHWEST_TERRITORY = "Northwest Territory"
GREENLAND = "Greenland"
ALBERTA = "Alberta"
ONTARIO = "Ontario"
EASTERN_CANADA = "Eastern Canada"
WESTERN_UNITED_STATES = "Western United States"
EASTERN_UNITED_STATES = "Eastern United States"
CENTRAL_AMERICA = "Central America"
VENEZUELA = "Venezuela"
PERU = "Peru"
BRAZIL = "Brazil"
ARGENTINA = "Argentina"
NORTH_AFRICA = "North Africa"
EGYPT = "Egypt"
EAST_AFRICA = "East Africa"
CENTRAL_AFRICA = "Central Africa"
SOUTH_AFRICA = "South Africa"
MADAGASCAR = "Madagascar"
WESTERN_EUROPE = "Western Europe"
SOUTHERN_EUROPE = "Southern Europe"
NORTHERN_EUROPE = "Northern Europe"
RUSSIA = "Russia"
GREAT_BRITAIN = "Great Britain"
ICELAND = "Iceland"
SCANDINAVIA = "Scandinavia"
URAL = "Ural"
SIBERIA = "Siberia"
YAKUTSK = "Yakutsk"
KAMCHATKA = "Kamchatka"
IRKUTSK = "Irkutsk"
JAPAN = "Japan"
MONGOLIA = "Mongolia"
CHINA = "China"
AFGHANISTAN = "Afghanistan"
MIDDLE_EAST = "Middle East"
INDIA = "India"
SOUTHEAST_ASIA = "Southeast Asia"
INDONESIA = "Indonesia"
NEW_GUINEA = "New Guinea"
WESTERN_AUSTRALIA = "Western Australia"
EASTERN_AUSTRALIA = "Eastern Australia"

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
adjacentCountriesD = {
    ALASKA: [KAMCHATKA, NORTHWEST_TERRITORY, ALBERTA],
    NORTHWEST_TERRITORY: [ALASKA, ALBERTA, ONTARIO, GREENLAND],
    GREENLAND: [NORTHWEST_TERRITORY, ONTARIO, EASTERN_CANADA, ICELAND],
    ALBERTA: [ALASKA, NORTHWEST_TERRITORY, ONTARIO, WESTERN_UNITED_STATES],
    ONTARIO: [GREENLAND, ALBERTA, WESTERN_UNITED_STATES, EASTERN_UNITED_STATES, EASTERN_CANADA, NORTHWEST_TERRITORY],
    EASTERN_CANADA: [EASTERN_UNITED_STATES, ONTARIO, GREENLAND],
    WESTERN_UNITED_STATES: [ALBERTA, ONTARIO, EASTERN_UNITED_STATES, CENTRAL_AMERICA],
    EASTERN_UNITED_STATES: [ONTARIO, EASTERN_CANADA, WESTERN_UNITED_STATES, CENTRAL_AMERICA],
    CENTRAL_AMERICA: [WESTERN_UNITED_STATES, EASTERN_UNITED_STATES, VENEZUELA],

    VENEZUELA: [CENTRAL_AMERICA, PERU, BRAZIL],
    PERU: [ARGENTINA, BRAZIL, VENEZUELA],
    BRAZIL: [ARGENTINA, PERU, VENEZUELA, NORTH_AFRICA],
    ARGENTINA: [PERU, BRAZIL],

    NORTH_AFRICA: [BRAZIL, WESTERN_EUROPE, SOUTHERN_EUROPE, EGYPT, EAST_AFRICA, CENTRAL_AFRICA],
    EGYPT: [SOUTHERN_EUROPE, MIDDLE_EAST, EAST_AFRICA, NORTH_AFRICA],
    EAST_AFRICA: [MIDDLE_EAST, CENTRAL_AFRICA, MADAGASCAR, EGYPT, SOUTH_AFRICA, NORTH_AFRICA],
    CENTRAL_AFRICA: [NORTH_AFRICA, EAST_AFRICA, SOUTH_AFRICA],
    SOUTH_AFRICA: [CENTRAL_AFRICA, EAST_AFRICA, MADAGASCAR],
    MADAGASCAR: [SOUTH_AFRICA, EAST_AFRICA],

    WESTERN_EUROPE: [GREAT_BRITAIN, NORTHERN_EUROPE, SOUTHERN_EUROPE, NORTH_AFRICA],
    SOUTHERN_EUROPE: [WESTERN_EUROPE, NORTHERN_EUROPE, RUSSIA, MIDDLE_EAST, EGYPT, NORTH_AFRICA],
    NORTHERN_EUROPE: [GREAT_BRITAIN, SCANDINAVIA, RUSSIA, SOUTHERN_EUROPE, WESTERN_EUROPE],
    RUSSIA: [SOUTHERN_EUROPE, NORTHERN_EUROPE, SCANDINAVIA, URAL, AFGHANISTAN, MIDDLE_EAST],
    GREAT_BRITAIN: [ICELAND, SCANDINAVIA, NORTHERN_EUROPE, WESTERN_EUROPE],
    ICELAND: [GREENLAND, SCANDINAVIA, GREAT_BRITAIN],
    SCANDINAVIA: [ICELAND, RUSSIA, NORTHERN_EUROPE, GREAT_BRITAIN],

    URAL: [RUSSIA, SIBERIA, CHINA, AFGHANISTAN],
    SIBERIA: [URAL, YAKUTSK, IRKUTSK, MONGOLIA, CHINA],
    YAKUTSK: [SIBERIA, IRKUTSK, KAMCHATKA],
    KAMCHATKA: [ALASKA, JAPAN, YAKUTSK, IRKUTSK, MONGOLIA],
    IRKUTSK: [SIBERIA, YAKUTSK, KAMCHATKA, MONGOLIA],
    JAPAN: [KAMCHATKA, MONGOLIA],
    MONGOLIA: [JAPAN, KAMCHATKA, CHINA, SIBERIA, IRKUTSK],
    CHINA: [MONGOLIA, SOUTHEAST_ASIA, INDIA, AFGHANISTAN, URAL, SIBERIA],
    AFGHANISTAN: [RUSSIA, URAL, CHINA, INDIA, MIDDLE_EAST],
    MIDDLE_EAST: [SOUTHERN_EUROPE, RUSSIA, AFGHANISTAN, INDIA, EAST_AFRICA, EGYPT],
    INDIA: [MIDDLE_EAST, AFGHANISTAN, CHINA, SOUTHEAST_ASIA],
    SOUTHEAST_ASIA: [INDONESIA, INDIA, CHINA],

    INDONESIA: [SOUTHEAST_ASIA, WESTERN_AUSTRALIA, NEW_GUINEA],
    NEW_GUINEA: [EASTERN_AUSTRALIA, WESTERN_AUSTRALIA, INDONESIA],
    WESTERN_AUSTRALIA: [INDONESIA, EASTERN_AUSTRALIA, NEW_GUINEA],
    EASTERN_AUSTRALIA: [NEW_GUINEA, WESTERN_AUSTRALIA]
}

# Define continent names as constants
ASIA = "Asia"
NORTH_AMERICA = "North America"
EUROPE = "Europe"
AFRICA = "Africa"
AUSTRALIA = "Australia"
SOUTH_AMERICA = "South America"


# List of which countries makeup each continent
continentD = {
    ASIA: [URAL, SIBERIA, YAKUTSK, KAMCHATKA, IRKUTSK, JAPAN, MONGOLIA, CHINA, AFGHANISTAN, MIDDLE_EAST, INDIA, SOUTHEAST_ASIA],
    NORTH_AMERICA: [ALASKA, NORTHWEST_TERRITORY, GREENLAND, ALBERTA, ONTARIO, EASTERN_CANADA, WESTERN_UNITED_STATES, EASTERN_UNITED_STATES, CENTRAL_AMERICA],
    EUROPE: [WESTERN_EUROPE, SOUTHERN_EUROPE, NORTHERN_EUROPE, RUSSIA, GREAT_BRITAIN, ICELAND, SCANDINAVIA],
    AFRICA: [NORTH_AFRICA, EGYPT, EAST_AFRICA, CENTRAL_AFRICA, SOUTH_AFRICA, MADAGASCAR],
    AUSTRALIA: [INDONESIA, NEW_GUINEA, WESTERN_AUSTRALIA, EASTERN_AUSTRALIA],
    SOUTH_AMERICA: [VENEZUELA, PERU, BRAZIL, ARGENTINA]
}

# Bonus armies if a player owns a whole continent
armiesPerContinentD = {
    ASIA: 7,
    NORTH_AMERICA: 5,
    EUROPE: 5,
    AFRICA: 3,
    AUSTRALIA: 2,
    SOUTH_AMERICA: 2
}
