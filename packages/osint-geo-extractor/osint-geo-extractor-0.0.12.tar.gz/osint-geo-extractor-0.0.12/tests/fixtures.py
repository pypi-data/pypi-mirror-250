import json
import os
import pytest

from geo_extractor.constants import RAW_DATA_FILENAMES

TEST_DATA_FOLDER = 'test_data'
TEST_DATA_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    TEST_DATA_FOLDER
)

def load(filename):
    with open(os.path.join(TEST_DATA_PATH, filename), 'r') as f:
        return json.load(f)

@pytest.fixture
def bellingcat_raw():
    return load(RAW_DATA_FILENAMES.BELLINGCAT)

@pytest.fixture
def ceninfores_raw():
    return load(RAW_DATA_FILENAMES.CENINFORES)

@pytest.fixture
def defmon_raw():
    return load(RAW_DATA_FILENAMES.DEFMON)

@pytest.fixture
def defmon_spreadsheet_raw():
    with open(os.path.join(
            TEST_DATA_PATH, RAW_DATA_FILENAMES.DEFMON_CSV
            ), 'r') as f:
        return f.read()

@pytest.fixture
def geoconfirmed_raw():
    # TODO: Workaround for handling kml/xml instead of json
    with open(os.path.join(TEST_DATA_PATH,
                           RAW_DATA_FILENAMES.GEOCONFIRMED), 'r') as f:
        return f.read()

# @pytest.fixture
# def reukraine_raw():
#     return load(RAW_DATA_FILENAMES.REUKRAINE)

@pytest.fixture
def texty_raw():
    return load(RAW_DATA_FILENAMES.TEXTY)
