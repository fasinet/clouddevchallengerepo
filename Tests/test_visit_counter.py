import sys
import os
import json
import pytest
from unittest.mock import patch, MagicMock
import azure.functions as func

# Add project root to sys.path
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

    # Call the function
    resp = VisitCounter(req)
    response_text = resp.get_body().decode()
    print("Response body:", response_text)

    # Assert status code and response
    assert resp.status_code == 200
    response_body = json.loads(response_text)
    assert "count" in response_body
    assert isinstance(response_body["count"], int)