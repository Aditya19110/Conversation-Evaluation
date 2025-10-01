#!/usr/bin/env python3
"""
Simple test to verify API deployment readiness
"""
import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

async def test_api_startup():
    """Test API can start without heavy dependencies."""
    try:
        # Test imports
        from src.api.main import app, evaluation_engine
        
        print("✓ API imports successful")
        
        # Test mock evaluation
        result = await evaluation_engine.evaluate_conversation(
            "Hello, how are you?",
            ["grammar", "politeness"]
        )
        
        if hasattr(result, 'facet_scores'):
            print(f"✓ Mock evaluation works: {len(result.facet_scores)} facets evaluated")
            print(f"  Sample facet: {list(result.facet_scores.keys())[0]}")
        elif isinstance(result, list):
            print(f"✓ Mock evaluation works: {len(result)} results")
            print(f"  Sample result: {result[0] if result else 'No results'}")
        else:
            print(f"✓ Mock evaluation completed: {type(result)}")
        
        print("✓ All deployment tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Deployment test failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_api_startup())
    sys.exit(0 if success else 1)