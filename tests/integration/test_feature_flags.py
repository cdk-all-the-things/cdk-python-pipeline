import json
from http import HTTPStatus
from typing import Any

from tests.utils import generate_api_gw_event, generate_context, generate_random_string

MOCKED_SCHEMA_CAMPAIGN_ON = {
    'features': {
        'premium_features': {
            'default': False,
            'rules': {
                'enable premium features for this specific customer name"': {
                    'when_match': True,
                    'conditions': [{
                        'action': 'EQUALS',
                        'key': 'customer_name',
                        'value': 'wilford'
                    }]
                }
            }
        },
        'ten_percent_off_campaign': {
            'default': True
        }
    },
    'countries': ['ISRAEL', 'USA'],
}

MOCKED_SCHEMA_CAMPAIGN_OFF = {
    'features': {
        'premium_features': {
            'default': False,
            'rules': {
                'enable premium features for this specific customer name"': {
                    'when_match': True,
                    'conditions': [{
                        'action': 'EQUALS',
                        'key': 'customer_name',
                        'value': 'wilford'
                    }]
                }
            }
        },
        'ten_percent_off_campaign': {
            'default': False
        }
    },
    'countries': ['ISRAEL', 'USA'],
}


def mock_dynamic_configuration(mocker, mock_schema: dict[str, Any]) -> None:
    """Mock AppConfig Store get_configuration method to use mock schema instead"""
    mocked_get_conf = mocker.patch('aws_lambda_powertools.utilities.parameters.AppConfigProvider.get')
    mocked_get_conf.return_value = mock_schema


def assert_response(response: dict[str, Any], expected_response_code: HTTPStatus, expected_customer_name: str, expected_order_item_count: int):
    # assert response
    assert response['statusCode'] == expected_response_code
    body_dict = json.loads(response['body'])
    assert body_dict['id']
    assert body_dict['name'] == expected_customer_name
    assert body_dict['item_count'] == expected_order_item_count


def spy_on_campaign_logic(mocker):
    import cdk_python_pipeline.logic.create_order as cr
    return mocker.spy(cr, 'handle_campaign')


def spy_on_premium_logic(mocker):
    import cdk_python_pipeline.logic.create_order as cr
    return mocker.spy(cr, 'apply_premium_user_discount')

