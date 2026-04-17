"""
Level progression configuration for all unit classes.
Easily modify stats for each class and level.
"""

# Maximum level cap for all units
MAX_LEVEL = 20

# Class-specific level sets
# Each class has specific stats for each level
CLASS_LEVELS = {
    "Tristan": {
        1: {"hp": 10, "atk": 3, "move": 4, "range": 1},
        2: {"hp": 11, "atk": 4, "move": 4, "range": 1},
        3: {"hp": 13, "atk": 5, "move": 5, "range": 1},
        4: {"hp": 14, "atk": 6, "move": 5, "range": 1},
        5: {"hp": 15, "atk": 7, "move": 5, "range": 1},
        6: {"hp": 17, "atk": 8, "move": 5, "range": 1},
        7: {"hp": 18, "atk": 10, "move": 6, "range": 1},
        8: {"hp": 19, "atk": 11, "move": 6, "range": 1},
        9: {"hp": 21, "atk": 12, "move": 6, "range": 1},
        10: {"hp": 22, "atk": 13, "move": 6, "range": 1},
        11: {"hp": 23, "atk": 14, "move": 7, "range": 1},
        12: {"hp": 25, "atk": 15, "move": 7, "range": 1},
        13: {"hp": 26, "atk": 16, "move": 7, "range": 1},
        14: {"hp": 27, "atk": 17, "move": 7, "range": 1},
        15: {"hp": 29, "atk": 18, "move": 7, "range": 1},
        16: {"hp": 30, "atk": 20, "move": 8, "range": 1},
        17: {"hp": 32, "atk": 21, "move": 8, "range": 1},
        18: {"hp": 35, "atk": 21, "move": 8, "range": 1},
        19: {"hp": 39, "atk": 23, "move": 8, "range": 1},
        20: {"hp": 42, "atk": 27, "move": 9, "range": 1}
    },
    
    "Archer": {
        1: {"hp": 8, "atk": 2, "move": 3, "range": 3},
        2: {"hp": 9, "atk": 3, "move": 3, "range": 3},
        3: {"hp": 10, "atk": 4, "move": 4, "range": 3},
        4: {"hp": 12, "atk": 5, "move": 4, "range": 3},
        5: {"hp": 14, "atk": 6, "move": 4, "range": 4},
        6: {"hp": 15, "atk": 7, "move": 5, "range": 4},
        7: {"hp": 16, "atk": 8, "move": 5, "range": 4},
        8: {"hp": 16, "atk": 10, "move": 5, "range": 4},
        9: {"hp": 17, "atk": 11, "move": 5, "range": 4},
        10: {"hp": 18, "atk": 12, "move": 6, "range": 5},
        11: {"hp": 20, "atk": 13, "move": 6, "range": 5},
        12: {"hp": 21, "atk": 15, "move": 6, "range": 5},
        13: {"hp": 22, "atk": 16, "move": 6, "range": 5},
        14: {"hp": 24, "atk": 17, "move": 6, "range": 5},
        15: {"hp": 25, "atk": 18, "move": 7, "range": 6},
        16: {"hp": 26, "atk": 19, "move": 7, "range": 6},
        17: {"hp": 29, "atk": 21, "move": 7, "range": 6},
        18: {"hp": 30, "atk": 22, "move": 7, "range": 6},
        19: {"hp": 31, "atk": 23, "move": 7, "range": 6},
        20: {"hp": 32, "atk": 25, "move": 8, "range": 7}
    },
    
    "Mage": {
        1: {"hp": 7, "atk": 4, "move": 2, "range": 3},
        2: {"hp": 8, "atk": 5, "move": 2, "range": 3},
        3: {"hp": 9, "atk": 6, "move": 3, "range": 3},
        4: {"hp": 10, "atk": 7, "move": 3, "range": 3},
        5: {"hp": 12, "atk": 8, "move": 3, "range": 4},
        6: {"hp": 13, "atk": 10, "move": 4, "range": 4},
        7: {"hp": 14, "atk": 11, "move": 4, "range": 4},
        8: {"hp": 15, "atk": 12, "move": 4, "range": 4},
        9: {"hp": 16, "atk": 13, "move": 4, "range": 4},
        10: {"hp": 18, "atk": 14, "move": 5, "range": 5},
        11: {"hp": 19, "atk": 16, "move": 5, "range": 5},
        12: {"hp": 20, "atk": 17, "move": 5, "range": 5},
        13: {"hp": 21, "atk": 18, "move": 5, "range": 5},
        14: {"hp": 22, "atk": 19, "move": 5, "range": 5},
        15: {"hp": 24, "atk": 20, "move": 6, "range": 6},
        16: {"hp": 25, "atk": 22, "move": 6, "range": 6},
        17: {"hp": 27, "atk": 24, "move": 6, "range": 6},
        18: {"hp": 29, "atk": 26, "move": 6, "range": 6},
        19: {"hp": 32, "atk": 29, "move": 6, "range": 6},
        20: {"hp": 36, "atk": 33, "move": 7, "range": 7}
    },
    
    "Horse": {
        1: {"hp": 9, "atk": 1, "move": 6, "range": 1},
        2: {"hp": 11, "atk": 2, "move": 6, "range": 1},
        3: {"hp": 11, "atk": 3, "move": 7, "range": 1},
        4: {"hp": 13, "atk": 4, "move": 7, "range": 1},
        5: {"hp": 14, "atk": 5, "move": 7, "range": 1},
        6: {"hp": 14, "atk": 6, "move": 8, "range": 1},
        7: {"hp": 16, "atk": 7, "move": 8, "range": 1},
        8: {"hp": 16, "atk": 8, "move": 8, "range": 1},
        9: {"hp": 18, "atk": 9, "move": 8, "range": 1},
        10: {"hp": 19, "atk": 11, "move": 9, "range": 1},
        11: {"hp": 19, "atk": 12, "move": 9, "range": 2},
        12: {"hp": 21, "atk": 13, "move": 9, "range": 2},
        13: {"hp": 21, "atk": 14, "move": 9, "range": 2},
        14: {"hp": 23, "atk": 15, "move": 9, "range": 2},
        15: {"hp": 24, "atk": 16, "move": 10, "range": 2},
        16: {"hp": 24, "atk": 17, "move": 10, "range": 2},
        17: {"hp": 26, "atk": 18, "move": 10, "range": 2},
        18: {"hp": 26, "atk": 19, "move": 10, "range": 2},
        19: {"hp": 30, "atk": 20, "move": 10, "range": 2},
        20: {"hp": 36, "atk": 22, "move": 11, "range": 3}
    },
    
    "Knig": {
        1: {"hp": 18, "atk": 6, "move": 4, "range": 1},
        2: {"hp": 19, "atk": 7, "move": 4, "range": 1},
        3: {"hp": 21, "atk": 8, "move": 5, "range": 1},
        4: {"hp": 22, "atk": 9, "move": 5, "range": 1},
        5: {"hp": 24, "atk": 11, "move": 5, "range": 1},
        6: {"hp": 25, "atk": 12, "move": 6, "range": 1},
        7: {"hp": 27, "atk": 13, "move": 6, "range": 1},
        8: {"hp": 28, "atk": 14, "move": 6, "range": 1},
        9: {"hp": 30, "atk": 15, "move": 6, "range": 1},
        10: {"hp": 31, "atk": 17, "move": 7, "range": 1},
        11: {"hp": 33, "atk": 19, "move": 7, "range": 1},
        12: {"hp": 34, "atk": 20, "move": 7, "range": 1},
        13: {"hp": 36, "atk": 21, "move": 7, "range": 1},
        14: {"hp": 37, "atk": 22, "move": 7, "range": 1},
        15: {"hp": 39, "atk": 24, "move": 8, "range": 1},
        16: {"hp": 40, "atk": 25, "move": 8, "range": 1},
        17: {"hp": 42, "atk": 26, "move": 8, "range": 1},
        18: {"hp": 43, "atk": 27, "move": 8, "range": 1},
        19: {"hp": 45, "atk": 28, "move": 8, "range": 1},
        20: {"hp": 46, "atk": 30, "move": 9, "range": 1}
    },
    
    "Knight": {
        1: {"hp": 12, "atk": 4, "move": 2, "range": 1},
        2: {"hp": 14, "atk": 5, "move": 2, "range": 1},
        3: {"hp": 15, "atk": 6, "move": 3, "range": 1},
        4: {"hp": 17, "atk": 7, "move": 3, "range": 1},
        5: {"hp": 18, "atk": 9, "move": 3, "range": 1},
        6: {"hp": 19, "atk": 10, "move": 4, "range": 1},
        7: {"hp": 21, "atk": 11, "move": 4, "range": 1},
        8: {"hp": 22, "atk": 13, "move": 4, "range": 2},
        9: {"hp": 24, "atk": 14, "move": 4, "range": 2},
        10: {"hp": 25, "atk": 16, "move": 5, "range": 2},
        11: {"hp": 26, "atk": 17, "move": 5, "range": 2},
        12: {"hp": 28, "atk": 18, "move": 5, "range": 2},
        13: {"hp": 29, "atk": 19, "move": 5, "range": 2},
        14: {"hp": 30, "atk": 20, "move": 5, "range": 2},
        15: {"hp": 32, "atk": 21, "move": 6, "range": 2},
        16: {"hp": 33, "atk": 23, "move": 6, "range": 2},
        17: {"hp": 34, "atk": 24, "move": 6, "range": 2},
        18: {"hp": 36, "atk": 25, "move": 6, "range": 2},
        19: {"hp": 38, "atk": 26, "move": 6, "range": 2},
        20: {"hp": 44, "atk": 27, "move": 7, "range": 3}
    },
    
    "Srodman": {
        1: {"hp": 11, "atk": 2, "move": 4, "range": 1},
        2: {"hp": 12, "atk": 5, "move": 4, "range": 1},
        3: {"hp": 14, "atk": 6, "move": 5, "range": 1},
        4: {"hp": 16, "atk": 7, "move": 5, "range": 1},
        5: {"hp": 17, "atk": 8, "move": 5, "range": 1},
        6: {"hp": 19, "atk": 9, "move": 5, "range": 1},
        7: {"hp": 20, "atk": 10, "move": 6, "range": 1},
        8: {"hp": 21, "atk": 12, "move": 6, "range": 1},
        9: {"hp": 22, "atk": 14, "move": 6, "range": 1},
        10: {"hp": 24, "atk": 14, "move": 7, "range": 1},
        11: {"hp": 26, "atk": 15, "move": 7, "range": 1},
        12: {"hp": 28, "atk": 16, "move": 7, "range": 1},
        13: {"hp": 30, "atk": 17, "move": 6, "range": 1},
        14: {"hp": 32, "atk": 18, "move": 6, "range": 1},
        15: {"hp": 51, "atk": 21, "move": 7, "range": 1},
        16: {"hp": 53, "atk": 22, "move": 7, "range": 1},
        17: {"hp": 55, "atk": 23, "move": 7, "range": 1},
        18: {"hp": 57, "atk": 24, "move": 7, "range": 1},
        19: {"hp": 59, "atk": 25, "move": 7, "range": 1},
        20: {"hp": 71, "atk": 30, "move": 8, "range": 1}
    },
    
    "Soldier": {
        1: {"hp": 7, "atk": 1, "move": 4, "range": 2},
        2: {"hp": 8, "atk": 2, "move": 4, "range": 2},
        3: {"hp": 9, "atk": 3, "move": 5, "range": 2},
        4: {"hp": 10, "atk": 4, "move": 5, "range": 2},
        5: {"hp": 11, "atk": 5, "move": 5, "range": 2},
        6: {"hp": 12, "atk": 6, "move": 6, "range": 2},
        7: {"hp": 13, "atk": 7, "move": 6, "range": 2},
        8: {"hp": 14, "atk": 8, "move": 6, "range": 2},
        9: {"hp": 15, "atk": 9, "move": 6, "range": 3},
        10: {"hp": 16, "atk": 10, "move": 7, "range": 3},
        11: {"hp": 17, "atk": 11, "move": 7, "range": 3},
        12: {"hp": 18, "atk": 12, "move": 7, "range": 3},
        13: {"hp": 19, "atk": 13, "move": 7, "range": 3},
        14: {"hp": 20, "atk": 14, "move": 7, "range": 3},
        15: {"hp": 21, "atk": 15, "move": 8, "range": 3},
        16: {"hp": 22, "atk": 16, "move": 8, "range": 3},
        17: {"hp": 23, "atk": 17, "move": 8, "range": 3},
        18: {"hp": 24, "atk": 18, "move": 8, "range": 3},
        19: {"hp": 25, "atk": 19, "move": 8, "range": 3},
        20: {"hp": 27, "atk": 20, "move": 9, "range": 3}
    },
    
    "Healer": {
        1: {"hp": 6, "atk": 0, "move": 3, "range": 1},
        2: {"hp": 7, "atk": 0, "move": 3, "range": 1},
        3: {"hp": 8, "atk": 0, "move": 4, "range": 1},
        4: {"hp": 9, "atk": 0, "move": 4, "range": 1},
        5: {"hp": 10, "atk": 0, "move": 4, "range": 2},
        6: {"hp": 11, "atk": 0, "move": 5, "range": 2},
        7: {"hp": 12, "atk": 0, "move": 5, "range": 2},
        8: {"hp": 13, "atk": 0, "move": 5, "range": 2},
        9: {"hp": 14, "atk": 0, "move": 5, "range": 2},
        10: {"hp": 15, "atk": 0, "move": 6, "range": 3},
        11: {"hp": 16, "atk": 0, "move": 6, "range": 3},
        12: {"hp": 17, "atk": 0, "move": 6, "range": 3},
        13: {"hp": 18, "atk": 0, "move": 6, "range": 3},
        14: {"hp": 19, "atk": 0, "move": 6, "range": 3},
        15: {"hp": 20, "atk": 0, "move": 7, "range": 4},
        16: {"hp": 21, "atk": 0, "move": 7, "range": 4},
        17: {"hp": 22, "atk": 0, "move": 7, "range": 4},
        18: {"hp": 23, "atk": 0, "move": 7, "range": 4},
        19: {"hp": 24, "atk": 0, "move": 7, "range": 4},
        20: {"hp": 26, "atk": 0, "move": 8, "range": 5}
    },
    
    "Horsearcher": {
        1: {"hp": 7, "atk": 1, "move": 6, "range": 3},
        2: {"hp": 8, "atk": 2, "move": 6, "range": 3},
        3: {"hp": 9, "atk": 3, "move": 6, "range": 3},
        4: {"hp": 11, "atk": 4, "move": 7, "range": 3},
        5: {"hp": 12, "atk": 5, "move": 7, "range": 3},
        6: {"hp": 13, "atk": 6, "move": 7, "range": 3},
        7: {"hp": 14, "atk": 7, "move": 8, "range": 4},
        8: {"hp": 16, "atk": 8, "move": 8, "range": 4},
        9: {"hp": 17, "atk": 9, "move": 8, "range": 4},
        10: {"hp": 18, "atk": 10, "move": 8, "range": 4},
        11: {"hp": 19, "atk": 11, "move": 9, "range": 4},
        12: {"hp": 21, "atk": 12, "move": 9, "range": 4},
        13: {"hp": 22, "atk": 16, "move": 9, "range": 4},
        14: {"hp": 23, "atk": 17, "move": 9, "range": 4},
        15: {"hp": 24, "atk": 19, "move": 9, "range": 5},
        16: {"hp": 25, "atk": 20, "move": 10, "range": 5},
        17: {"hp": 26, "atk": 22, "move": 10, "range": 5},
        18: {"hp": 27, "atk": 23, "move": 10, "range": 5},
        19: {"hp": 28, "atk": 24, "move": 10, "range": 5},
        20: {"hp": 30, "atk": 25, "move": 11, "range": 6}
    },
    
    "Ballistician": {
        1: {"hp": 6, "atk": 2, "move": 1, "range": 10},
        2: {"hp": 7, "atk": 3, "move": 1, "range": 10},
        3: {"hp": 8, "atk": 4, "move": 2, "range": 10},
        4: {"hp": 9, "atk": 5, "move": 2, "range": 10},
        5: {"hp": 10, "atk": 6, "move": 2, "range": 11},
        6: {"hp": 11, "atk": 7, "move": 3, "range": 11},
        7: {"hp": 12, "atk": 8, "move": 3, "range": 11},
        8: {"hp": 13, "atk": 9, "move": 3, "range": 11},
        9: {"hp": 14, "atk": 10, "move": 3, "range": 11},
        10: {"hp": 16, "atk": 11, "move": 4, "range": 12},
        11: {"hp": 17, "atk": 12, "move": 4, "range": 12},
        12: {"hp": 18, "atk": 13, "move": 4, "range": 12},
        13: {"hp": 19, "atk": 14, "move": 4, "range": 12},
        14: {"hp": 20, "atk": 15, "move": 4, "range": 12},
        15: {"hp": 21, "atk": 16, "move": 5, "range": 13},
        16: {"hp": 22, "atk": 17, "move": 5, "range": 13},
        17: {"hp": 23, "atk": 18, "move": 5, "range": 13},
        18: {"hp": 24, "atk": 19, "move": 5, "range": 13},
        19: {"hp": 25, "atk": 20, "move": 5, "range": 13},
        20: {"hp": 26, "atk": 21, "move": 5, "range": 14}
    },
    
    "Bandit": {
        1: {"hp": 8, "atk": 2, "move": 3, "range": 1},
        2: {"hp": 9, "atk": 3, "move": 3, "range": 1},
        3: {"hp": 10, "atk": 4, "move": 3, "range": 1},
        4: {"hp": 11, "atk": 5, "move": 3, "range": 1},
        5: {"hp": 13, "atk": 6, "move": 4, "range": 1},
        6: {"hp": 14, "atk": 7, "move": 4, "range": 1},
        7: {"hp": 15, "atk": 9, "move": 4, "range": 1},
        8: {"hp": 16, "atk": 10, "move": 4, "range": 1},
        9: {"hp": 17, "atk": 11, "move": 4, "range": 1},
        10: {"hp": 21, "atk": 13, "move": 5, "range": 1},
        11: {"hp": 22, "atk": 14, "move": 5, "range": 1},
        12: {"hp": 23, "atk": 15, "move": 5, "range": 1},
        13: {"hp": 24, "atk": 16, "move": 5, "range": 1},
        14: {"hp": 25, "atk": 17, "move": 5, "range": 1},
        15: {"hp": 31, "atk": 20, "move": 6, "range": 1},
        16: {"hp": 32, "atk": 21, "move": 6, "range": 1},
        17: {"hp": 33, "atk": 22, "move": 6, "range": 1},
        18: {"hp": 34, "atk": 23, "move": 6, "range": 1},
        19: {"hp": 35, "atk": 24, "move": 6, "range": 1},
        20: {"hp": 43, "atk": 29, "move": 7, "range": 2}
    },
    
    "Darkmage": {
        1: {"hp": 10, "atk": 3, "move": 2, "range": 3},
        2: {"hp": 11, "atk": 4, "move": 2, "range": 3},
        3: {"hp": 12, "atk": 5, "move": 3, "range": 3},
        4: {"hp": 13, "atk": 6, "move": 3, "range": 3},
        5: {"hp": 15, "atk": 8, "move": 3, "range": 4},
        6: {"hp": 16, "atk": 9, "move": 4, "range": 4},
        7: {"hp": 17, "atk": 10, "move": 4, "range": 4},
        8: {"hp": 18, "atk": 11, "move": 4, "range": 4},
        9: {"hp": 19, "atk": 12, "move": 4, "range": 4},
        10: {"hp": 21, "atk": 14, "move": 5, "range": 5},
        11: {"hp": 22, "atk": 15, "move": 5, "range": 5},
        12: {"hp": 23, "atk": 16, "move": 5, "range": 5},
        13: {"hp": 24, "atk": 17, "move": 5, "range": 5},
        14: {"hp": 25, "atk": 18, "move": 5, "range": 5},
        15: {"hp": 27, "atk": 20, "move": 6, "range": 6},
        16: {"hp": 28, "atk": 21, "move": 6, "range": 6},
        17: {"hp": 29, "atk": 22, "move": 6, "range": 6},
        18: {"hp": 30, "atk": 23, "move": 6, "range": 6},
        19: {"hp": 31, "atk": 24, "move": 6, "range": 6},
        20: {"hp": 33, "atk": 26, "move": 7, "range": 7}
    },
    
    "Great_sage": {
        1: {"hp": 16, "atk": 5, "move": 4, "range": 5},
        2: {"hp": 17, "atk": 6, "move": 4, "range": 5},
        3: {"hp": 19, "atk": 7, "move": 5, "range": 5},
        4: {"hp": 20, "atk": 9, "move": 5, "range": 5},
        5: {"hp": 22, "atk": 10, "move": 5, "range": 6},
        6: {"hp": 23, "atk": 12, "move": 6, "range": 6},
        7: {"hp": 24, "atk": 13, "move": 6, "range": 6},
        8: {"hp": 26, "atk": 14, "move": 6, "range": 6},
        9: {"hp": 27, "atk": 16, "move": 6, "range": 6},
        10: {"hp": 29, "atk": 17, "move": 7, "range": 7},
        11: {"hp": 30, "atk": 19, "move": 7, "range": 7},
        12: {"hp": 32, "atk": 20, "move": 7, "range": 7},
        13: {"hp": 33, "atk": 22, "move": 7, "range": 7},
        14: {"hp": 35, "atk": 23, "move": 7, "range": 7},
        15: {"hp": 36, "atk": 25, "move": 8, "range": 8},
        16: {"hp": 38, "atk": 26, "move": 8, "range": 8},
        17: {"hp": 39, "atk": 28, "move": 8, "range": 8},
        18: {"hp": 41, "atk": 29, "move": 8, "range": 8},
        19: {"hp": 42, "atk": 31, "move": 8, "range": 8},
        20: {"hp": 45, "atk": 33, "move": 9, "range": 9}
    }
}

def get_class_stats(class_name: str, level: int) -> dict:
    """Get stats for a class at a specific level"""
    if class_name not in CLASS_LEVELS:
        return {"hp": 10, "atk": 3, "move": 3, "range": 1}
    
    # Cap level at MAX_LEVEL
    if level > MAX_LEVEL:
        level = MAX_LEVEL
    
    # Get the exact stats for this level
    if level in CLASS_LEVELS[class_name]:
        return CLASS_LEVELS[class_name][level].copy()
    else:
        # If level not found, use the highest available level
        highest_level = max(CLASS_LEVELS[class_name].keys())
        return CLASS_LEVELS[class_name][highest_level].copy()

def get_exp_required(level: int) -> int:
    """Calculate experience required for a specific level"""
    if level <= 1:
        return 0
    # Exponential growth: 10, 20, 35, 55, 80, 110, 145, 185, 230, 280...
    return int(10 * (1.2 ** (level - 1)))
