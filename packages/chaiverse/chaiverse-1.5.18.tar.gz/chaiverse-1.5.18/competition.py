import requests
import time

import pandas as pd

from chaiverse.login_cli import auto_authenticate
from chaiverse.submit import get_model_info, redeploy_model
from chaiverse.utils import get_all_historical_submissions, get_url


COMPETITIONS_ENDPOINT = '/competitions'
PENDING_COMPETITION_ENDPOINT = '/pending_competition'
ACTIVE_COMPETITION_ENDPOINT = '/active_competition'


def get_competitions():
    url = get_url(COMPETITIONS_ENDPOINT)
    response = requests.get(url)
    assert response.ok, response.json()
    return response.json()

