# pylint: ignore-pylint
import pytest
import json
import requests
from extract import get_plant_response, get_range_of_plants
from unittest.mock import MagicMock, patch


def mock_response(
        status=200,
        content="CONTENT",
        json_data=None):
    mock_resp = MagicMock()
    # set status code and content
    mock_resp.status_code = status
    mock_resp.content = content
    # add json data if provided
    if json_data:
        mock_resp.json = MagicMock(
            return_value=json_data
        )
    return mock_resp


@patch("extract.requests.get")
def test_get_response_is_called(mock_request):
    mock_request.return_value = mock_response()
    get_plant_response(3)

    assert mock_request.called == True


@patch("extract.requests.get")
def test_get_response_success(mock_request):
    mock_request.return_value = mock_response()
    response = get_plant_response(3)
    assert response.status_code == 200


@patch("extract.requests.get")
def test_get_response_failure(mock_request):
    mock_request.return_value = mock_response(status=404)
    response = get_plant_response(3)
    assert response.status_code == 404


@patch("extract.requests.get")
def test_get_response_error(mock_request):
    mock_request.return_value = mock_response()
    with pytest.raises(ValueError):
        get_plant_response("three")


@patch("extract.requests.get")
def test_get_range_of_plants(mock_request):
    mock_request.return_value = mock_response()
    get_range_of_plants(2)
    assert mock_request.call_count == 2
