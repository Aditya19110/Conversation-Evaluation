#!/usr/bin/env python3
"""
Test script to verify model token configuration
"""
import os
import sys
import asyncio

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

async def test_model_loading():
    """Test model loading with and without token."""
    try:
        from src.models.inference import create_model
        
        # Test configuration
        config = {
            'cache_dir': './models',
            'max_length': 512
        }
        
        # Test without token (should use mock)
        print("Testing without HUGGINGFACE_TOKEN...")
        if 'HUGGINGFACE_TOKEN' in os.environ:
            del os.environ['HUGGINGFACE_TOKEN']
            
        model = create_model("microsoft/DialoGPT-medium", config)
        print(f"Model type: {type(model).__name__}")
        
        await model.load_model()
        
        # Test generation
        result = await model.generate("Hello, how are you?")
        print(f"Mock result: {result.text}")
        
        print("✅ Model loading test passed!")
        
    except Exception as e:
        print(f"❌ Model loading test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_model_loading())
    sys.exit(0 if success else 1)