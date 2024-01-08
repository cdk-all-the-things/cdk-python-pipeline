import json
from http import HTTPStatus

import pytest
import requests

from tests.utils import generate_random_string, get_stack_output


@pytest.fixture(scope='module', autouse=True)
def test():
    return

