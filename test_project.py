#!/usr/bin/env python3

import json
import asyncio
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_data_processor():
    """Test the data processor functionality."""
    try:
        from src.data.processor import DataProcessor, ConversationTurn
        import yaml
        
        # Load config
        config_path = Path(__file__).parent / "configs" / "config.yaml"
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Initialize processor
        processor = DataProcessor(config)
        
        # Test conversation cleaning
        test_text = "Hello,   how are  you???   "
        clean_text = processor.clean_conversation_text(test_text)
        print(f"[PASS] Text cleaning works: '{test_text}' -> '{clean_text}'")
        
        # Test feature extraction
        conv = ConversationTurn(text="Hello, how are you today?")
        features = processor.extract_features(conv)
        print(f"[PASS] Feature extraction works: {len(features)} features extracted")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] Data processor test failed: {e}")
        return False

def test_config_loading():
    """Test configuration loading."""
    try:
        import yaml
        
        config_path = Path(__file__).parent / "configs" / "config.yaml"
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        print(f"[PASS] Config loaded: {config['app']['name']}")
        print(f"[PASS] Facets available: {len(config.get('facets', {}))}")
        
        return True
        
    except Exception as e:
        print(f"✗ Config loading failed: {e}")
        return False

def test_sample_data():
    """Test sample conversation data."""
    try:
        sample_path = Path(__file__).parent / "data" / "sample_conversations" / "sample_conversations.json"
        
        with open(sample_path, 'r') as f:
            conversations = json.load(f)
        
        print(f"[PASS] Sample conversations loaded: {len(conversations)} conversations")
        
        # Test first conversation
        first_conv = conversations[0]
        required_fields = ['id', 'text', 'context', 'category']
        
        for field in required_fields:
            if field not in first_conv:
                raise ValueError(f"Missing field: {field}")
        
        print(f"[PASS] Sample conversation structure valid")
        
        return True
        
    except Exception as e:
        print(f"✗ Sample data test failed: {e}")
        return False

def test_api_structure():
    """Test API module structure."""
    try:
        # Test imports without actually running the server
        spec = "src.api.main"
        module = __import__(spec, fromlist=[''])
        
        print("[PASS] API module imports successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ API structure test failed: {e}")
        return False

def test_docker_files():
    """Test Docker configuration files."""
    try:
        docker_compose_path = Path(__file__).parent / "docker-compose.yml"
        dockerfile_api_path = Path(__file__).parent / "docker" / "api" / "Dockerfile"
        
        if not docker_compose_path.exists():
            raise FileNotFoundError("docker-compose.yml not found")
        
        if not dockerfile_api_path.exists():
            raise FileNotFoundError("API Dockerfile not found")
        
        print("[PASS] Docker files exist")
        
        return True
        
    except Exception as e:
        print(f"✗ Docker files test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Testing Conversation Evaluation Benchmark System")
    print("=" * 50)
    
    tests = [
        ("Configuration Loading", test_config_loading),
        ("Sample Data", test_sample_data),
        ("Data Processor", test_data_processor),
        ("API Structure", test_api_structure),
        ("Docker Files", test_docker_files),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nTesting {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"   {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! The project structure is working correctly.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Place your facet dataset in data/raw/")
        print("3. Run with Docker: docker-compose up --build")
        print("4. Access the UI at http://localhost:3000")
        print("5. Access the API docs at http://localhost:8000/docs")
    else:
        print("Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)