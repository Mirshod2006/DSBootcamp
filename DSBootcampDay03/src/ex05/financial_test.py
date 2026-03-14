import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ex03.financial import fetch_data
import pytest
from unittest.mock import patch

# Test cases
@patch('requests.get')
def test_get_financial_data_valid_ticker_and_field(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = '<html><div class="tableBody"><div class="row"><div class="column"><div class="rowTitle">Total Revenue</div></div><div class="column">2023</div><div class="column">1000000</div></div></div></html>'
    
    ticker = "AAPL"
    field = "Total Revenue"
    
    expected = ('Total Revenue', '2023', '1000000')
    result = fetch_data(ticker, field)
    
    assert result == expected, f"Expected {expected}, but got {result}"

@patch('requests.get')
def test_return_type(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = '<html><div class="tableBody"><div class="row"><div class="column"><div class="rowTitle">Total Revenue</div></div><div class="column">2023</div><div class="column">1000000</div></div></div></html>'
    
    ticker = "AAPL"
    field = "Total Revenue"
    
    result = fetch_data(ticker, field)
    
    assert isinstance(result, tuple), f"Expected result to be of type tuple, but got {type(result)}"

@patch('requests.get')
def test_invalid_ticker(mock_get):
    mock_get.return_value.status_code = 404
    
    ticker = "INVALID"
    field = "Total Revenue"
    
    with pytest.raises(Exception, match="According to given data, web-site could be found!"):
        fetch_data(ticker, field)

@patch('requests.get')
def test_invalid_field(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = '<html><div class="tableBody"><div class="row"><div class="column"><div class="rowTitle">Profit</div></div><div class="column">2023</div><div class="column">1000000</div></div></div></html>'
    
    ticker = "AAPL"
    field = "Total Revenue"
    
    with pytest.raises(Exception, match="Please make sure, entered field exsists!"):
        fetch_data(ticker, field)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: financial.py <ticker> <field>")
        sys.exit(1)

    ticker = sys.argv[1]
    field = sys.argv[2]
    try:
        print(fetch_data(ticker, field))
    except Exception as e:
        print(str(e))