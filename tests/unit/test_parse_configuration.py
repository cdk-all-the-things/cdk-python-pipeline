import os
from typing import Any

import pytest
from pydantic import BaseModel

from cdk.cdk_python_pipeline.constants import CONFIGURATION_NAME, ENVIRONMENT, SERVICE_NAME

MOCKED_SCHEMA = {'region': 'us-east-1'}


class MockedSchemaModel(BaseModel):
    region: str


def mock_dynamic_configuration(mocker, mock_schema: dict[str, Any]) -> None:
    """Mock AppConfig Store get_configuration method to use mock schema instead"""
    mocked_get_conf = mocker.patch('aws_lambda_powertools.utilities.parameters.AppConfigProvider.get')
    mocked_get_conf.return_value = mock_schema


@pytest.fixture(scope='module', autouse=True)
def init():
    os.environ['CONFIGURATION_APP'] = SERVICE_NAME
    os.environ['CONFIGURATION_ENV'] = ENVIRONMENT
    os.environ['CONFIGURATION_NAME'] = CONFIGURATION_NAME
    os.environ['CONFIGURATION_MAX_AGE_MINUTES'] = '5'

