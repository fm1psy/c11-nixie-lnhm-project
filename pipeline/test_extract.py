# pylint: ignore-pylint
import pytest
import json
import requests
from extract import get_plant_response, get_range_of_plants
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_response():
    return {"body": "", "status_code": 200}


@patch("extract.requests.get")
def test_get_response_is_called(mock_request, mock_response):
    mock_request.return_value = mock_response
    response = get_plant_response(3)

    assert mock_request.called == True


@patch("extract.requests.get")
def test_get_response_success(mock_request, mock_response):
    mock_request.return_value = mock_response
    response = get_plant_response(3)
    assert response.status_code == 200


@patch("extract.requests.get")
def test_get_response_failure(mock_request, mock_response):
    mock_request.return_value = mock_response
    with pytest.raises(ValueError):
        response = get_plant_response("three")


@patch("extract.requests.get")
@patch("extract.requests.Response.json")
def test_get_range_of_plants(mock_request, mock_json, mock_response):
    mock_request.return_value = mock_response
    mock_json.return_value = mock_response

    get_range_of_plants(2)
    assert mock_json.called.count == 2
