BASE_PAGE = 'https://euclidea.fandom.com'
START_PAGE = 'https://euclidea.fandom.com/wiki/Euclidea_Wiki'
SAVE_PATH_OF_SOLVABLE_LEVELS = './solvable_levels.json'
SAVE_PATH_OF_IMAGES = '../images'

TOOL2IDX = {
    'Perpendicular Tool': 0,
    'Line Tool': 1,
    'Circle Tool': 2,
    'Perpendicular Bisector Tool': 3,
    'Angle Bisector Tool': 4,
    'Parallel Tool': 5,
    'Compass Tool': 6,
    'Intersect Tool': 7,
    'Point Tool': 8,
}

IDX2TOOL = {
    v: k for k, v in TOOL2IDX.items()
}
