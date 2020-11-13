"""DATA"""
foods = [
    'Wheat Flour (Enriched)',
    'Macaroni',
    'Wheat Cereal (Enriched)',
    'Corn Flakes',
    'Corn Meal',
    'Hominy Grits',
    'Rice',
    'Rolled Oats',
    'White Bread (Enriched)',
    'Whole Wheat Bread',
    'Rye Bread',
    'Pound Cake',
    'Soda Crackers',
    'Milk',
    'Evaporated Milk (can)',
    'Butter',
    'Oleomargarine',
    'Eggs',
    'Cheese (Cheddar)',
    'Cream',
    'Peanut Butter',
    'Mayonnaise',
    'Crisco',
    'Lard',
    'Sirloin Steak',
    'Round Steak',
    'Rib Roast',
    'Chuck Roast',
    'Plate',
    'Liver (Beef)',
    'Leg of Lamb',
    'Lamb Chops (Rib)',
    'Pork Chops',
    'Pork Loin Roast',
    'Bacon',
    'Ham, smoked',
    'Salt Pork',
    'Roasting Chicken',
    'Veal Cutlets',
    'Salmon, Pink (can)',
    'Apples',
    'Bananas',
    'Lemons',
    'Oranges',
    'Green Beans',
    'Cabbage',
    'Carrots',
    'Celery',
    'Lettuce',
    'Onions',
    'Potatoes',
    'Spinach',
    'Sweet Potatoes',
    'Peaches (can)',
    'Pears (can)',
    'Pineapple (can)',
    'Asparagus (can)',
    'Green Beans (can)',
    'Pork and Beans (can)',
    'Corn (can)',
    'Peas (can)',
    'Tomatoes (can)',
    'Tomato Soup (can)',
    'Peaches, Dried',
    'Prunes, Dried',
    'Raisins, Dried',
    'Peas, Dried',
    'Lima Beans, Dried',
    'Navy Beans, Dried',
    'Coffee',
    'Tea',
    'Cocoa',
    'Chocolate',
    'Sugar',
    'Corn Syrup',
    'Molasses',
    'Strawberry Preserves', ]

units = [
    '10 lb.',
    '1 lb.',
    '28 oz.',
    '8 oz.',
    '1 lb.',
    '24 oz.',
    '1 lb.',
    '1 lb.',
    '1 lb.',
    '1 lb.',
    '1 lb.',
    '1 lb.',
    '1 lb.',
    '1 qt.',
    '14.5 oz.',
    '1 lb.',
    '1 lb.',
    '1 doz.',
    '1 lb.',
    '1/2 pt.',
    '1 lb.',
    '1/2 pt.',
    '1 lb.',
    '1 lb.',
    '1 lb.',
    '1 lb.',
    '1 lb.',
    '1 lb.',
    '1 lb.',
    '1 lb.',
    '1 lb.',
    '1 lb.',
    '1 lb.',
    '1 lb.',
    '1 lb.',
    '1 lb.',
    '1 lb.',
    '1 lb.',
    '1 lb.',
    '16 oz.',
    '1 lb.',
    '1 lb.',
    '1 doz.',
    '1 doz.',
    '1 lb.',
    '1 lb.',
    '1 bunch',
    '1 stalk',
    '1 head',
    '1 lb.',
    '15 lb.',
    '1 lb.',
    '1 lb.',
    'No. 2 1/2',
    'No. 2 1/2',
    'No. 2 1/2',
    'No. 2',
    'No. 2',
    '16 oz.',
    'No. 2',
    'No. 2',
    'No. 2',
    '10 1/2 oz.',
    '1 lb.',
    '1 lb.',
    '15 oz.',
    '1 lb.',
    '1 lb.',
    '1 lb.',
    '1 lb.',
    '1/4 lb.',
    '8 oz.',
    '8 oz.',
    '10 lb.',
    '24 oz.',
    '18 oz.',
    '1 lb.', ]

price = [
    36,
    14.1,
    24.2,
    7.1,
    4.6,
    8.5,
    7.5,
    7.1,
    7.9,
    9.1,
    9.1,
    24.8,
    15.1,
    11,
    6.7,
    30.8,
    16.1,
    32.6,
    24.2,
    14.1,
    17.9,
    16.7,
    20.3,
    9.8,
    39.6,
    36.4,
    29.2,
    22.6,
    14.6,
    26.8,
    27.6,
    36.6,
    30.7,
    24.2,
    25.6,
    27.4,
    16,
    30.3,
    42.3,
    13,
    4.4,
    6.1,
    26,
    30.9,
    7.1,
    3.7,
    4.7,
    7.3,
    8.2,
    3.6,
    34,
    8.1,
    5.1,
    16.8,
    20.4,
    21.3,
    27.7,
    10,
    7.1,
    10.4,
    13.8,
    8.6,
    7.6,
    15.7,
    9,
    9.4,
    7.9,
    8.9,
    5.9,
    22.4,
    17.4,
    8.6,
    16.2,
    51.7,
    13.7,
    13.6,
    20.5, ]

calories = [
    44.7,
    11.6,
    11.8,
    11.4,
    36.0,
    28.6,
    21.2,
    25.3,
    15.0,
    12.2,
    12.4,
    8.0,
    12.5,
    6.1,
    8.4,
    10.8,
    20.6,
    2.9,
    7.4,
    3.5,
    15.7,
    8.6,
    20.1,
    41.7,
    2.9,
    2.2,
    3.4,
    3.6,
    8.5,
    2.2,
    3.1,
    3.3,
    3.5,
    4.4,
    10.4,
    6.7,
    18.8,
    1.8,
    1.7,
    5.8,
    5.8,
    4.9,
    1.0,
    2.2,
    2.4,
    2.6,
    2.7,
    0.9,
    0.4,
    5.8,
    14.3,
    1.1,
    9.6,
    3.7,
    3.0,
    2.4,
    0.4,
    1.0,
    7.5,
    5.2,
    2.3,
    1.3,
    1.6,
    8.5,
    12.8,
    13.5,
    20.0,
    17.4,
    26.9,
    0,
    0,
    8.7,
    8.0,
    34.9,
    14.7,
    9.0,
    6.4,
]

protein = [
    1411,
    418,
    377,
    252,
    897,
    680,
    460,
    907,
    488,
    484,
    439,
    130,
    288,
    310,
    422,
    9,
    17,
    238,
    448,
    49,
    661,
    18,
    0,
    0,
    166,
    214,
    213,
    309,
    404,
    333,
    245,
    140,
    196,
    249,
    152,
    212,
    164,
    184,
    156,
    705,
    27,
    60,
    21,
    40,
    138,
    125,
    73,
    51,
    27,
    166,
    336,
    106,
    138,
    20,
    8,
    16,
    33,
    54,
    364,
    136,
    136,
    63,
    71,
    87,
    99,
    104,
    1367,
    1055,
    1691,
    0,
    0,
    237,
    77,
    0,
    0,
    0,
    11,
]

calcium = [
    2,
    0.7,
    14.4,
    0.1,
    1.7,
    0.8,
    0.6,
    5.1,
    2.5,
    2.7,
    1.1,
    0.4,
    0.5,
    10.5,
    15.1,
    0.2,
    0.6,
    1.0,
    16.4,
    1.7,
    1.0,
    0.2,
    0,
    0,
    0.1,
    0.1,
    0.1,
    0.2,
    0.2,
    0.2,
    0.1,
    0.1,
    0.2,
    0.3,
    0.2,
    0.2,
    0.1,
    0.1,
    0.1,
    6.8,
    0.5,
    0.4,
    0.5,
    1.1,
    3.7,
    4.0,
    2.8,
    3.0,
    1.1,
    3.8,
    1.8,
    0,
    2.7,
    0.4,
    0.3,
    0.4,
    0.3,
    2,
    4,
    0.2,
    0.6,
    0.7,
    0.6,
    1.7,
    2.5,
    2.5,
    4.2,
    3.7,
    11.4,
    0,
    0,
    3,
    1.3,
    0,
    0.5,
    10.3,
    0.4,
]

iron = [
    365,
    54,
    175,
    56,
    99,
    80,
    41,
    341,
    115,
    125,
    82,
    31,
    50,
    18,
    9,
    3,
    6,
    52,
    19,
    3,
    48,
    8,
    0,
    0,
    34,
    32,
    33,
    46,
    62,
    139,
    20,
    15,
    30,
    37,
    23,
    31,
    26,
    30,
    24,
    45,
    36,
    30,
    14,
    18,
    80,
    36,
    43,
    23,
    22,
    59,
    118,
    138,
    54,
    10,
    8,
    8,
    12,
    65,
    134,
    16,
    45,
    38,
    43,
    173,
    154,
    136,
    345,
    459,
    792,
    0,
    0,
    72,
    39,
    0,
    74,
    244,
    7,
]

vitamin_A = [
    0,
    0,
    0,
    0,
    30.9,
    0,
    0,
    0,
    0,
    0,
    0,
    18.9,
    0,
    16.8,
    26,
    44.2,
    55.8,
    18.6,
    28.1,
    16.9,
    0,
    2.7,
    0,
    0.2,
    0.2,
    0.4,
    0,
    0.4,
    0,
    169.2,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0.1,
    0,
    3.5,
    7.3,
    17.4,
    0,
    11.1,
    69,
    7.2,
    188.5,
    0.9,
    112.4,
    16.6,
    6.7,
    918.4,
    290.7,
    21.5,
    0.8,
    2,
    16.3,
    53.9,
    3.5,
    12,
    34.9,
    53.2,
    57.9,
    86.8,
    85.7,
    4.5,
    2.9,
    5.1,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0.2,
]

thiamine = [
    55.4,
    3.2,
    14.4,
    13.5,
    17.4,
    10.6,
    2,
    37.1,
    13.8,
    13.9,
    9.9,
    2.8,
    0,
    4,
    3,
    0,
    0.2,
    2.8,
    0.8,
    0.6,
    9.6,
    0.4,
    0,
    0,
    2.1,
    2.5,
    0,
    1,
    0.9,
    6.4,
    2.8,
    1.7,
    17.4,
    18.2,
    1.8,
    9.9,
    1.4,
    0.9,
    1.4,
    1,
    3.6,
    2.5,
    0.5,
    3.6,
    4.3,
    9,
    6.1,
    1.4,
    1.8,
    4.7,
    29.4,
    5.7,
    8.4,
    0.5,
    0.8,
    2.8,
    1.4,
    1.6,
    8.3,
    1.6,
    4.9,
    3.4,
    3.5,
    1.2,
    3.9,
    6.3,
    28.7,
    26.9,
    38.4,
    4,
    0,
    2,
    0.9,
    0,
    0,
    1.9,
    0.2,
]

riboflavin = [
    33.3,
    1.9,
    8.8,
    2.3,
    7.9,
    1.6,
    4.8,
    8.9,
    8.5,
    6.4,
    3,
    3,
    0,
    16,
    23.5,
    0.2,
    0,
    6.5,
    10.3,
    2.5,
    8.1,
    0.5,
    0,
    0.5,
    2.9,
    2.4,
    2,
    4,
    0,
    50.8,
    3.9,
    2.7,
    2.7,
    3.6,
    1.8,
    3.3,
    1.8,
    1.8,
    2.4,
    4.9,
    2.7,
    3.5,
    0,
    1.3,
    5.8,
    4.5,
    4.3,
    1.4,
    3.4,
    5.9,
    7.1,
    13.8,
    5.4,
    1,
    0.8,
    0.8,
    2.1,
    4.3,
    7.7,
    2.7,
    2.5,
    2.5,
    2.4,
    4.3,
    4.3,
    1.4,
    18.4,
    38.2,
    24.6,
    5.1,
    2.3,
    11.9,
    3.4,
    0,
    0,
    7.5,
    0.4,
]

niacin = [
    441,
    68,
    114,
    68,
    106,
    110,
    60,
    64,
    126,
    160,
    66,
    17,
    0,
    7,
    11,
    2,
    0,
    1,
    4,
    0,
    471,
    0,
    0,
    5,
    69,
    87,
    0,
    120,
    0,
    316,
    86,
    54,
    60,
    79,
    71,
    50,
    0,
    68,
    57,
    209,
    5,
    28,
    4,
    10,
    37,
    26,
    89,
    9,
    11,
    21,
    198,
    33,
    83,
    31,
    5,
    7,
    17,
    32,
    56,
    42,
    37,
    36,
    67,
    55,
    65,
    24,
    162,
    93,
    217,
    50,
    42,
    40,
    14,
    0,
    5,
    146,
    3,
]

ascorbic_acid = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    177,
    60,
    0,
    0,
    0,
    0,
    17,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    525,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    46,
    0,
    0,
    544,
    498,
    952,
    1998,
    862,
    5369,
    608,
    313,
    449,
    1184,
    2522,
    2755,
    1912,
    196,
    81,
    399,
    272,
    431,
    0,
    218,
    370,
    1253,
    862,
    57,
    257,
    136,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
]

"""NURIENTS"""
nutrients = [
    'Calories (1000s)',
    'Protein (grams)',
    'Calcium (grams)',
    'Iron (mg)',
    'Vitamin A (1000 IU)',
    'Vitamin B1 (mg)',
    'Vitamin B2 (mg)',
    'Niacin (mg)',
    'Vitamin C (mg)',
]

nutrient_requirements = [
    3,
    70,
    0.8,
    12,
    5,
    1.8,
    2.7,
    18,
    75,
]
