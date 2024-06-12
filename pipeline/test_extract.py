# pylint: ignore-pylint
import pytest
import requests
from extract import get_plant_response, get_range_of_plants, extract_data
from unittest.mock import Mock, patch, mock_open
EXTRACT_DESTINATION = "extracted_plants.json"


@pytest.fixture
def mock_response(
        status=200,
        content="CONTENT"):
    mock_resp = Mock()
    # set status code and content
    mock_resp.status_code = status
    mock_resp.content = content

    return mock_resp


@patch("extract.requests.get")
def test_get_response_is_called(mock_request, mock_response):
    mock_request.return_value = mock_response
    get_plant_response(3)

    assert mock_request.called == True


@patch("extract.requests.get")
def test_get_response_success(mock_request, mock_response):
    mock_request.return_value = mock_response
    response = get_plant_response(3)
    assert response.status_code == 200


@patch("extract.requests.get.json")
@patch("extract.requests.get")
def test_get_response_error(mock_request, mock_json, mock_response):
    mock_request.return_value = mock_response
    with pytest.raises(ValueError):
        get_plant_response("three")


@patch("extract.requests.get")
def test_get_range_of_plants(mock_request, mock_response):
    mock_request.return_value = mock_response
    get_range_of_plants(2)
    assert mock_request.call_count == 2


@patch("extract.requests.get")
def test_get_range_of_plants_invalid_range(mock_request, mock_response):
    mock_request.return_value = mock_response
    with pytest.raises(ValueError):
        get_range_of_plants("three")


@patch("extract.requests.get")
def test_get_range_of_plants_success(mock_request, mock_response):
    mock_request.return_value = mock_response
    res = get_range_of_plants(2)
    assert len(res) == 2


@patch("extract.get_plant_response")
@patch("extract.requests.get")
def test_get_range_of_plants_value_error(mock_request, mock_plant_response, mock_response):
    mock_request.return_value = mock_response
    mock_plant_response.side_effect = ValueError
    with pytest.raises(ValueError):
        get_range_of_plants(2)


@patch("extract.get_plant_response")
@patch("extract.requests.get")
def test_get_range_of_plants_timeout_error(mock_request, mock_plant_response, mock_response):
    mock_request.return_value = mock_response
    mock_plant_response.side_effect = requests.ReadTimeout
    with pytest.raises(requests.ReadTimeout):
        get_range_of_plants(2)


@patch("builtins.open", new_callable=mock_open, read_data="data")
@patch("extract.json.dump")
@patch("extract.get_range_of_plants")
def test_extract_data(mock_plants, mock_dump, mock_file):
    extract_data()
    mock_plants.assert_called_once()
    mock_file.assert_called_once()
    mock_dump.assert_called_once()
