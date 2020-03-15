import logging

import pandas as pd
import requests
import io
_logger = logging.getLogger(__name__)

_WORLD_DATA_URL = 'https://raw.githubusercontent.com/open-covid-19/data/master/output/world.csv'
_WORLD_DATA_DESTINATION = 'data/world_latest.csv'
_OK_STATUS = 200


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
    return pd.read_csv(download_data())
