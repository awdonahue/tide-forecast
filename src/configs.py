import os

TIDES_URL = os.getenv('TIDES_URL', 'https://www.tide-forecast.com/locations')
TIDES_LATEST_PATH = os.getenv('TIDES_LATEST_PATH', 'tides/latest')
TIDES_TABLE_NAME = os.getenv('TIDES_TABLE_NAME', 'tide_flex_start')

# Area / State must be hyphenated. Format Example-Area, Example-State
LOCATIONS = [
    ('Half-Moon-Bay', 'California'),
    ('Huntington-Beach', 'California'),
    ('Providence', 'Rhode-Island'),
    ('Wrightsville-Beach', 'North-Carolina'),
]

# Beautiful Soup array index positions for table columns
RISES_COLUMN = {
    'sunrise': 0,
    'sunset': 1,
    'moonrise': 2,
    'moonset': 3
}

TIDE_COLUMN = {
    'type': 0,
    'time': 1,
    'height': 2,
}
