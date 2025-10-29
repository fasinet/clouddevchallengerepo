import sys
import os
import json
import pytest
import azure.functions as func
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from function_app import VisitCounter
@patch("function_app.TableServiceClient")
def test_visit_counter_returns_200(mock_table_service_client):
    # Mock table client and entity
    mock_table_client = MagicMock()
    mock_entity = {"PartitionKey": "counter", "RowKey": "siteVisits", "Count": 42}

    # Configure mock behavior
    mock_table_client.get_entity.return_value = mock_entity
    mock_table_service_client.from_connection_string.return_value.get_table_client.return_value = mock_table_client

    # Create a mock HTTP request
    req = func.HttpRequest(
        method='GET',
        url='/api/VisitCounter',
        headers={"Content-Type": "application/json"},
        body=None
    )

def test_visit_counter_returns_200():
    req = func.HttpRequest(
        method='GET',
        url='/api/VisitCounter',
        body=None
    )

    resp = VisitCounter(req)
    response_text = resp.get_body().decode()
    print("Response body:", response_text)

    assert resp.status_code == 200

    try:
        response_body = json.loads(response_text)
    except json.JSONDecodeError:
        pytest.fail("Response is not valid JSON")

    assert "count" in response_body
    assert isinstance(response_body["count"], int)
