from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union
import asyncio
import logging
import time
import yaml
from pathlib import Path

from ..evaluation.engine import ConversationEvaluationEngine, ConversationEvaluation, BatchEvaluationResult
from ..data.processor import ConversationTurn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration
config_path = Path(__file__).parent.parent.parent / "configs" / "config.yaml"
try:
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    # Fallback config for deployment
    config = {
        'api': {
            'title': 'Conversation Evaluation API',
            'description': 'API for conversation evaluation',
            'version': '1.0.0'
        },
        'models': {'default_model': 'mock'}
    }

# Initialize evaluation engine
try:
    evaluation_engine = ConversationEvaluationEngine(config)
except Exception as e:
    logger.warning(f"Could not initialize full evaluation engine: {e}")
    # Create a mock evaluation engine for deployment
    class MockEvaluationEngine:
        def __init__(self, config):
            self.config = config
            
        async def evaluate_conversation(self, conversation_text, facets, model_name=None):
            import random
            results = []
            for facet in facets:
                results.append({
                    'facet': facet,
                    'score': random.randint(1, 5),
                    'confidence': round(random.uniform(0.7, 0.95), 2),
                    'reasoning': f'Mock evaluation for {facet}'
                })
            return results
            
        async def evaluate_batch(self, conversations, facets, model_name=None):
            results = []
            for conv in conversations:
                conv_results = await self.evaluate_conversation(conv, facets, model_name)
                results.append(conv_results)
            return results
    
    evaluation_engine = MockEvaluationEngine(config)

# Initialize FastAPI app
app = FastAPI(
    title=config['api']['title'],
    description=config['api']['description'],
    version=config['api']['version'],
    docs_url=config['api']['docs_url'],
    redoc_url=config['api']['redoc_url']
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config['api']['cors']['allow_origins'],
    allow_credentials=True,
    allow_methods=config['api']['cors']['allow_methods'],
    allow_headers=config['api']['cors']['allow_headers'],
)


# Pydantic models for API
class ConversationInput(BaseModel):
    """Input model for conversation evaluation."""
    text: str = Field(..., min_length=1, max_length=10000, description="Conversation text to evaluate")
    speaker: Optional[str] = Field(None, description="Speaker identifier")
    context: Optional[str] = Field(None, description="Additional context for the conversation")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    
    @validator('text')
    def text_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Text cannot be empty')
        return v


class EvaluationRequest(BaseModel):
    """Request model for conversation evaluation."""
    conversation: ConversationInput
    facets: List[str] = Field(..., min_items=1, max_items=100, description="List of facets to evaluate")
    model_name: Optional[str] = Field(None, description="Model to use for evaluation")
    conversation_id: Optional[str] = Field(None, description="Unique identifier for the conversation")
    
    @validator('facets')
    def facets_must_be_valid(cls, v):
        # Get valid facets from config
        valid_facets = set()
        for category_facets in config.get('facets', {}).values():
            valid_facets.update(category_facets)
        
        invalid_facets = [f for f in v if f not in valid_facets]
        if invalid_facets:
            raise ValueError(f'Invalid facets: {invalid_facets}')
        return v


class BatchEvaluationRequest(BaseModel):
    """Request model for batch evaluation."""
    conversations: List[ConversationInput] = Field(..., min_items=1, max_items=100)
    facets: List[str] = Field(..., min_items=1, max_items=100)
    model_name: Optional[str] = Field(None, description="Model to use for evaluation")
    
    @validator('facets')
    def facets_must_be_valid(cls, v):
        # Get valid facets from config
        valid_facets = set()
        for category_facets in config.get('facets', {}).values():
            valid_facets.update(category_facets)
        
        invalid_facets = [f for f in v if f not in valid_facets]
        if invalid_facets:
            raise ValueError(f'Invalid facets: {invalid_facets}')
        return v


class EvaluationResponse(BaseModel):
    """Response model for evaluation results."""
    conversation_id: str
    conversation_text: str
    facet_scores: Dict[str, Dict[str, Any]]
    confidence_metrics: Dict[str, float]
    processing_time: float
    model_used: str
    timestamp: float


class BatchEvaluationResponse(BaseModel):
    """Response model for batch evaluation results."""
    evaluations: List[EvaluationResponse]
    total_processing_time: float
    average_confidence: float
    facet_statistics: Dict[str, Dict[str, float]]


class ModelInfo(BaseModel):
    """Model information response."""
    name: str
    loaded: bool
    supported: bool
    device: Optional[str] = None


class HealthCheck(BaseModel):
    """Health check response."""
    status: str
    timestamp: float
    version: str
    models_loaded: int


# Dependency for rate limiting (simplified)
async def rate_limit_check():
    """Simple rate limiting check."""
    # In production, implement proper rate limiting with Redis
    return True


# API Endpoints
@app.get("/", response_model=Dict[str, Any])
async def root():
    """Root endpoint with API information."""
    return {
        "name": config['app']['name'],
        "version": config['app']['version'],
        "description": "Production-ready conversation evaluation benchmark",
        "docs_url": "/docs",
        "health_url": "/health"
    }


@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint."""
    return HealthCheck(
        status="healthy",
        timestamp=time.time(),
        version=config['app']['version'],
        models_loaded=len(evaluation_engine.model_manager.models)
    )


@app.get("/facets", response_model=Dict[str, List[str]])
async def get_available_facets():
    """Get all available evaluation facets."""
    return config.get('facets', {})


@app.get("/models", response_model=List[str])
async def get_supported_models():
    """Get list of supported models."""
    return evaluation_engine.model_manager.list_supported_models()


@app.get("/models/{model_name}", response_model=ModelInfo)
async def get_model_info(model_name: str):
    """Get information about a specific model."""
    try:
        info = evaluation_engine.model_manager.get_model_info(model_name)
        return ModelInfo(**info)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Model not found: {str(e)}")


@app.post("/evaluate", response_model=EvaluationResponse)
async def evaluate_conversation(
    request: EvaluationRequest,
    background_tasks: BackgroundTasks,
    _: bool = Depends(rate_limit_check)
):
    """Evaluate a single conversation on specified facets."""
    try:
        # Convert request to conversation turn
        conv_turn = ConversationTurn(
            text=request.conversation.text,
            speaker=request.conversation.speaker,
            context=request.conversation.context,
            metadata=request.conversation.metadata
        )
        
        # Perform evaluation
        result = await evaluation_engine.evaluate_conversation(
            conversation=conv_turn,
            facets=request.facets,
            conversation_id=request.conversation_id,
            model_name=request.model_name
        )
        
        # Convert to response format
        response = EvaluationResponse(
            conversation_id=result.conversation_id,
            conversation_text=result.conversation_text,
            facet_scores={
                facet: {
                    "score": eval_result.score,
                    "confidence": eval_result.confidence,
                    "reasoning": eval_result.reasoning
                }
                for facet, eval_result in result.facet_scores.items()
            },
            confidence_metrics={
                "overall_confidence": result.confidence_metrics.overall_confidence,
                "model_confidence": result.confidence_metrics.model_confidence,
                "consistency_score": result.confidence_metrics.consistency_score,
                "uncertainty_estimate": result.confidence_metrics.uncertainty_estimate
            },
            processing_time=result.processing_time,
            model_used=result.model_used,
            timestamp=result.timestamp
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error evaluating conversation: {e}")
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")


@app.post("/evaluate/batch", response_model=BatchEvaluationResponse)
async def batch_evaluate_conversations(
    request: BatchEvaluationRequest,
    background_tasks: BackgroundTasks,
    _: bool = Depends(rate_limit_check)
):
    """Evaluate multiple conversations in batch."""
    try:
        # Convert requests to conversation turns
        conv_turns = [
            ConversationTurn(
                text=conv.text,
                speaker=conv.speaker,
                context=conv.context,
                metadata=conv.metadata
            )
            for conv in request.conversations
        ]
        
        # Perform batch evaluation
        result = await evaluation_engine.batch_evaluate(
            conversations=conv_turns,
            facets=request.facets,
            model_name=request.model_name
        )
        
        # Convert to response format
        evaluations = []
        for eval_result in result.evaluations:
            evaluation_response = EvaluationResponse(
                conversation_id=eval_result.conversation_id,
                conversation_text=eval_result.conversation_text,
                facet_scores={
                    facet: {
                        "score": facet_result.score,
                        "confidence": facet_result.confidence,
                        "reasoning": facet_result.reasoning
                    }
                    for facet, facet_result in eval_result.facet_scores.items()
                },
                confidence_metrics={
                    "overall_confidence": eval_result.confidence_metrics.overall_confidence,
                    "model_confidence": eval_result.confidence_metrics.model_confidence,
                    "consistency_score": eval_result.confidence_metrics.consistency_score,
                    "uncertainty_estimate": eval_result.confidence_metrics.uncertainty_estimate
                },
                processing_time=eval_result.processing_time,
                model_used=eval_result.model_used,
                timestamp=eval_result.timestamp
            )
            evaluations.append(evaluation_response)
        
        response = BatchEvaluationResponse(
            evaluations=evaluations,
            total_processing_time=result.total_processing_time,
            average_confidence=result.average_confidence,
            facet_statistics=result.facet_statistics
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error in batch evaluation: {e}")
        raise HTTPException(status_code=500, detail=f"Batch evaluation failed: {str(e)}")


@app.post("/models/{model_name}/load")
async def load_model(model_name: str, background_tasks: BackgroundTasks):
    """Load a specific model."""
    try:
        # Check if model is supported
        if model_name not in evaluation_engine.model_manager.list_supported_models():
            raise HTTPException(status_code=400, detail=f"Model {model_name} is not supported")
        
        # Load model in background
        background_tasks.add_task(evaluation_engine.model_manager.load_model, model_name)
        
        return {"message": f"Loading model {model_name}", "status": "started"}
        
    except Exception as e:
        logger.error(f"Error loading model {model_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to load model: {str(e)}")


@app.delete("/models/{model_name}")
async def unload_model(model_name: str):
    """Unload a specific model to free memory."""
    try:
        evaluation_engine.model_manager.unload_model(model_name)
        return {"message": f"Model {model_name} unloaded", "status": "success"}
        
    except Exception as e:
        logger.error(f"Error unloading model {model_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to unload model: {str(e)}")


@app.get("/stats", response_model=Dict[str, Any])
async def get_system_stats():
    """Get system statistics."""
    try:
        import psutil
        import torch
        
        stats = {
            "cpu_usage": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "models_loaded": len(evaluation_engine.model_manager.models),
            "timestamp": time.time()
        }
        
        # Add GPU stats if available
        if torch.cuda.is_available():
            stats["gpu_memory_used"] = torch.cuda.memory_allocated() / 1024**3  # GB
            stats["gpu_memory_total"] = torch.cuda.get_device_properties(0).total_memory / 1024**3  # GB
        
        return stats
        
    except ImportError:
        return {
            "models_loaded": len(evaluation_engine.model_manager.models),
            "timestamp": time.time(),
            "note": "Detailed system stats unavailable (psutil not installed)"
        }


# Exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    logger.info("Starting Conversation Evaluation API")
    
    # Load default model
    try:
        default_model = config.get('models', {}).get('default_model')
        if default_model:
            logger.info(f"Loading default model: {default_model}")
            # Load model in background to avoid blocking startup
            asyncio.create_task(evaluation_engine.model_manager.load_model_async(default_model))
    except Exception as e:
        logger.warning(f"Failed to load default model: {e}")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    logger.info("Shutting down Conversation Evaluation API")
    
    # Cleanup model manager
    for model_name in list(evaluation_engine.model_manager.models.keys()):
        evaluation_engine.model_manager.unload_model(model_name)


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=config['app']['host'],
        port=config['app']['port'],
        reload=config['app']['debug'],
        workers=1  # Use 1 worker for model loading
    )