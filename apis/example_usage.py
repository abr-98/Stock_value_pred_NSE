"""
Example usage script for the Stock Predictor API
This script demonstrates how to call the different API endpoints
"""
import requests
import json


# Base URL for the API
BASE_URL = "http://localhost:8000"


def health_check():
    """Check if API is running"""
    print("=" * 60)
    print("Health Check")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def analyze_stock(symbol):
    """Analyze a stock"""
    print("=" * 60)
    print(f"Stock Analysis - {symbol}")
    print("=" * 60)
    
    # Using POST method
    response = requests.post(
        f"{BASE_URL}/api/v1/stock/analyze",
        json={"symbol": symbol}
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Error: {response.text}")
    print()


def analyze_stock_get(symbol):
    """Analyze a stock using GET method"""
    print("=" * 60)
    print(f"Stock Analysis (GET) - {symbol}")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/api/v1/stock/analyze/{symbol}")
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Error: {response.text}")
    print()


def analyze_portfolio():
    """Analyze a portfolio"""
    print("=" * 60)
    print("Portfolio Analysis")
    print("=" * 60)
    
    portfolio_data = {
        "portfolio": {
            "AAPL": 10,
            "GOOGL": 5,
            "MSFT": 8
        },
        "value": 100000.0
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/portfolio/analyze",
        json=portfolio_data
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Error: {response.text}")
    print()


def get_allocation():
    """Get allocation recommendations"""
    print("=" * 60)
    print("Allocation Recommendations")
    print("=" * 60)
    
    allocation_data = {
        "portfolio": {
            "AAPL": 10,
            "GOOGL": 5
        },
        "value": 50000.0
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/allocation/analyze",
        json=allocation_data
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Error: {response.text}")
    print()


def analyze_correlation(symbol):
    """Analyze correlation for a stock"""
    print("=" * 60)
    print(f"Correlation Analysis - {symbol}")
    print("=" * 60)
    
    response = requests.post(
        f"{BASE_URL}/api/v1/correlation/analyze",
        json={"symbol": symbol}
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Error: {response.text}")
    print()


def get_fundamental_report(symbol):
    """Get fundamental report for a stock"""
    print("=" * 60)
    print(f"Fundamental Report - {symbol}")
    print("=" * 60)
    
    response = requests.post(
        f"{BASE_URL}/api/v1/fundamental/report",
        json={"symbol": symbol}
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Error: {response.text}")
    print()


if __name__ == "__main__":
    print("\n")
    print("╔═══════════════════════════════════════════════════════╗")
    print("║   Stock Predictor API - Example Usage                ║")
    print("╚═══════════════════════════════════════════════════════╝")
    print("\nMake sure the API server is running before executing this script!")
    print("Start the server with: python apis/start_server.py\n")
    
    try:
        # Check API health
        health_check()
        
        # Example stock symbol
        test_symbol = "AAPL"
        
        # Test different endpoints
        # Note: Uncomment the endpoints you want to test
        
        # analyze_stock(test_symbol)
        # analyze_stock_get(test_symbol)
        # analyze_portfolio()
        # get_allocation()
        # analyze_correlation(test_symbol)
        # get_fundamental_report(test_symbol)
        
        print("✓ All example tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("✗ Error: Could not connect to the API server.")
        print("  Please make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
