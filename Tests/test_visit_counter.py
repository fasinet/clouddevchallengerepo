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

    resp = visit_counter(req)

    assert resp.status_code == 200
    response_body = json.loads(resp.get_body())
    assert "count" in response_body
    assert isinstance(response_body["count"], int)