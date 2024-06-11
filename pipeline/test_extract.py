# pylint: ignore-pylint
import pytest
import json
import requests
from extract import get_plant_response
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_response():
    return {"body": "", "status_code": 200}


@patch("extract.requests.get")
def test_get_response_is_called(mock_request, mock_response):
    mock_request.return_value = mock_response
    response = get_plant_response(3)

    assert mock_request.called == True
