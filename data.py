import io
import logging

import pandas as pd
import requests

_logger = logging.getLogger(__name__)

_WORLD_DATA_URL = 'https://raw.githubusercontent.com/open-covid-19/data/master/output/data.csv'
_WORLD_DATA_DESTINATION = 'data/world_latest.csv'
_OK_STATUS = 200
_DATA_FILE = 'data.csv'


def download_data() -> io.BytesIO:
    _logger.info('Downloading data...')
    r = requests.get(_WORLD_DATA_URL)

    if r.status_code == _OK_STATUS:
        _logger.info('Download succeeded')
        return io.BytesIO(r.content)
    else:
        _logger.error('Download failed')
        raise Exception(f'Unable to download data. Response: {r.content}')


def get_data() -> pd.DataFrame:
    try:
        content = download_data()
        df = pd.read_csv(content)
    except Exception as e:
        df = load_cache()
    # compute_diff(df)

    return df


def store_data(content):
    with open(_DATA_FILE, 'w') as f:
        f.writelines(content)


def load_cache() -> pd.DataFrame:
    logger.info('Loading data from cache')
    return pd.read_csv(_DATA_FILE)
