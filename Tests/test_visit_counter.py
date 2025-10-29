import sys
import os
import json
import pytest
import azure.functions as func
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from function_app import VisitCounter

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
