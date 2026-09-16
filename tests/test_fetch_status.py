from unittest.mock import Mock
from fetch_status import handle_response

def make_response(status_code, json_data=None, headers=None):
    response = Mock()
    response.status_code = status_code
    response.json.return_value = json_data or {}
    response.headers = headers or {}
    response.text = "error body"
    return response

def test_handle_response_success_returns_data():
    response = make_response(200, json_data={"foo": "bar"})
    result = handle_response(response, "test")
    assert result == {"foo": "bar"}

def test_handle_response_unauthorized_returns_none():
    response = make_response(401)
    result = handle_response(response, "test")
    assert result is None

def test_handle_response_quota_exhausted_returns_none():
    response = make_response(429, headers={"x-ratelimit-reset": "2026-01-01T00:00Z"})
    result = handle_response(response, "test")
    assert result is None

def test_handle_response_bad_request_returns_none():
    response = make_response(400)
    result = handle_response(response, "test")
    assert result is None

def test_handle_response_unexpected_status_returns_none():
    response = make_response(500)
    result = handle_response(response, "test")
    assert result is None