"""
Test script to verify the API system initialization
This script tests that the environment and initializers are working correctly
"""
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def test_environment_loading():
    """Test that environment.py can load the API key"""
    print("=" * 70)
    print("TEST 1: Loading OpenAI API Key")
    print("=" * 70)
    
    try:
        from environment import load_api_key
        load_api_key()
        
        # Check if the key was loaded
        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key:
            print("✓ OpenAI API key loaded successfully")
            print(f"  Key starts with: {api_key[:10]}...")
            return True
        else:
            print("✗ API key not found in environment")
            return False
    except FileNotFoundError:
        print("✗ OpenAI-Key.txt file not found")
        return False
    except Exception as e:
        print(f"✗ Error loading API key: {str(e)}")
        return False


def test_system_initialization():
    """Test that SystemInitializer works"""
    print("\n" + "=" * 70)
    print("TEST 2: System Initialization")
    print("=" * 70)
    
    try:
        from application.helpers.initializers import SystemInitializer
        
        print("Creating SystemInitializer...")
        initializer = SystemInitializer()
        
        print("Calling initialize_system()...")
        initializer.initialize_system()
        
        print("Getting agents...")
        agents = initializer.get_agents()
        
        print("\nInitialized agents:")
        for agent_name in agents.keys():
            agent = agents[agent_name]
            print(f"  ✓ {agent_name}: {type(agent).__name__}")
        
        print(f"\n✓ System initialized successfully with {len(agents)} agents")
        return True
        
    except Exception as e:
        print(f"✗ Error initializing system: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_engine_initialization():
    """Test that engines can be initialized with pre-loaded agents"""
    print("\n" + "=" * 70)
    print("TEST 3: Engine Initialization with Agents")
    print("=" * 70)
    
    try:
        from application.helpers.initializers import SystemInitializer
        from application.engines.correlation_data_engine import CorrelationDataEngine
        from application.engines.fundamental_report_engine import FundamentalReportEngine
        from application.engines.portfolio_data_engine import PortfolioDataEngine
        from application.engines.allocation_data_engine import StockDataEngine as AllocationEngine
        
        # Initialize system
        initializer = SystemInitializer()
        initializer.initialize_system()
        agents = initializer.get_agents()
        
        # Test each engine
        engines = {
            "CorrelationDataEngine": CorrelationDataEngine(agents=agents),
            "FundamentalReportEngine": FundamentalReportEngine(agents=agents),
            "PortfolioDataEngine": PortfolioDataEngine(agents=agents),
            "AllocationEngine": AllocationEngine(agents=agents),
        }
        
        print("Engines initialized with pre-loaded agents:")
        for engine_name, engine in engines.items():
            print(f"  ✓ {engine_name}: {type(engine).__name__}")
            if hasattr(engine, 'agents'):
                print(f"    - Has agents: {engine.agents is not None}")
        
        print(f"\n✓ All {len(engines)} engines initialized successfully")
        return True
        
    except Exception as e:
        print(f"✗ Error initializing engines: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n")
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║   Stock Predictor API - System Initialization Test               ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")
    print()
    
    results = []
    
    # Run tests
    results.append(("Environment Loading", test_environment_loading()))
    results.append(("System Initialization", test_system_initialization()))
    results.append(("Engine Initialization", test_engine_initialization()))
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{status}: {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✓ ALL TESTS PASSED - System is ready!")
        print("\nYou can now start the API server with:")
        print("  python apis/start_server.py")
    else:
        print("✗ SOME TESTS FAILED - Please check the errors above")
    print("=" * 70)
