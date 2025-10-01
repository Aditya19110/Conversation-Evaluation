import torch
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    pipeline,
    BitsAndBytesConfig
)
from typing import Dict, List, Optional, Tuple, Any, Union
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
import asyncio
from concurrent.futures import ThreadPoolExecutor
import gc

logger = logging.getLogger(__name__)


@dataclass
class ModelOutput:
    """Represents model output with confidence."""
    text: str
    confidence: float
    tokens_used: int
    processing_time: float


@dataclass
class EvaluationResult:
    """Represents evaluation result for a facet."""
    facet: str
    score: int
    confidence: float
    reasoning: str


class BaseModel(ABC):
    """Abstract base class for evaluation models."""
    
    def __init__(self, model_name: str, config: Dict[str, Any]):
        self.model_name = model_name
        self.config = config
        self.device = self._get_device()
        
    def _get_device(self) -> str:
        """Determine the best available device."""
        if torch.cuda.is_available():
            return "cuda"
        elif torch.backends.mps.is_available():
            return "mps"
        else:
            return "cpu"
    
    @abstractmethod
    def load_model(self) -> None:
        """Load the model and tokenizer."""
        pass
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> ModelOutput:
        """Generate text from prompt."""
        pass
    
    @abstractmethod
    def evaluate_conversation(self, 
                            conversation: str, 
                            facets: List[str]) -> List[EvaluationResult]:
        """Evaluate conversation on given facets."""
        pass


class OpenWeightsModel(BaseModel):
    """Implementation for open-weights models."""
    
    def __init__(self, model_name: str, config: Dict[str, Any]):
        super().__init__(model_name, config)
        self.tokenizer = None
        self.model = None
        self.pipeline = None
        
    def load_model(self) -> None:
        """Load the model with optimizations."""
        try:
            logger.info(f"Loading model: {self.model_name}")
            
            # Configure quantization for efficiency
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4"
            )
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                cache_dir=self.config.get('cache_dir', './models'),
                trust_remote_code=True
            )
            
            # Ensure pad token exists
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Load model with quantization
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                quantization_config=quantization_config,
                device_map="auto",
                cache_dir=self.config.get('cache_dir', './models'),
                trust_remote_code=True,
                torch_dtype=torch.float16
            )
            
            # Create pipeline for easier generation
            self.pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device_map="auto",
                torch_dtype=torch.float16
            )
            
            logger.info(f"Model {self.model_name} loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading model {self.model_name}: {e}")
            raise
    
    def generate(self, prompt: str, **kwargs) -> ModelOutput:
        """Generate text from prompt."""
        if not self.pipeline:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        import time
        start_time = time.time()
        
        try:
            # Set generation parameters
            generation_kwargs = {
                'max_length': kwargs.get('max_length', self.config.get('max_length', 2048)),
                'temperature': kwargs.get('temperature', self.config.get('temperature', 0.7)),
                'do_sample': True,
                'pad_token_id': self.tokenizer.pad_token_id,
                'return_full_text': False,
                'num_return_sequences': 1
            }
            
            # Generate response
            outputs = self.pipeline(prompt, **generation_kwargs)
            
            # Extract generated text
            generated_text = outputs[0]['generated_text']
            
            # Calculate confidence (simplified approach)
            confidence = self._calculate_confidence(prompt, generated_text)
            
            # Count tokens
            tokens_used = len(self.tokenizer.encode(prompt + generated_text))
            
            processing_time = time.time() - start_time
            
            return ModelOutput(
                text=generated_text,
                confidence=confidence,
                tokens_used=tokens_used,
                processing_time=processing_time
            )
            
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            raise
    
    def _calculate_confidence(self, prompt: str, generated_text: str) -> float:
        """Calculate confidence score for generated text."""
        # Simplified confidence calculation
        # In production, this could use more sophisticated methods
        
        # Factors that increase confidence:
        # - Appropriate length
        # - Clear structure
        # - Relevant content
        
        confidence = 0.5  # Base confidence
        
        # Length factor
        if 10 <= len(generated_text.split()) <= 100:
            confidence += 0.2
        
        # Structure factor (has clear sentences)
        if any(punct in generated_text for punct in '.!?'):
            confidence += 0.1
        
        # Relevance factor (contains key terms from prompt)
        prompt_words = set(prompt.lower().split())
        generated_words = set(generated_text.lower().split())
        
        if prompt_words.intersection(generated_words):
            confidence += 0.2
        
        return min(confidence, 1.0)
    
    def evaluate_conversation(self, 
                            conversation: str, 
                            facets: List[str]) -> List[EvaluationResult]:
        """Evaluate conversation on given facets."""
        results = []
        
        for facet in facets:
            try:
                # Create evaluation prompt
                prompt = self._create_evaluation_prompt(conversation, facet)
                
                # Generate evaluation
                output = self.generate(prompt)
                
                # Parse evaluation result
                result = self._parse_evaluation_output(facet, output)
                
                results.append(result)
                
            except Exception as e:
                logger.error(f"Error evaluating facet {facet}: {e}")
                # Add error result
                results.append(EvaluationResult(
                    facet=facet,
                    score=3,  # Default neutral score
                    confidence=0.0,
                    reasoning=f"Error during evaluation: {str(e)}"
                ))
        
        return results
    
    def _create_evaluation_prompt(self, conversation: str, facet: str) -> str:
        """Create evaluation prompt for a specific facet."""
        facet_descriptions = {
            'grammar': 'grammatical correctness, including syntax, tense usage, and sentence structure',
            'coherence': 'logical flow and consistency of ideas throughout the conversation',
            'fluency': 'natural and smooth expression of language',
            'vocabulary_richness': 'diversity and sophistication of vocabulary used',
            'clarity': 'how clear and understandable the message is',
            'appropriateness': 'suitability of the response given the context',
            'politeness': 'level of courtesy and respectfulness in the conversation',
            'relevance': 'how relevant the response is to the conversation topic',
            'toxicity': 'presence of harmful, offensive, or toxic content',
            'empathy': 'demonstration of understanding and caring for others',
            'sentiment': 'overall emotional tone of the conversation'
        }
        
        description = facet_descriptions.get(facet, f'quality of {facet.replace("_", " ")}')
        
        prompt = f"""
You are an expert conversation analyst. Evaluate the following conversation turn for {description}.

Conversation: "{conversation}"

Please evaluate this conversation on a scale of 1-5 where:
1 = Very Poor
2 = Poor  
3 = Average
4 = Good
5 = Excellent

Provide your evaluation in the following format:
Score: [1-5]
Reasoning: [Brief explanation for your score]

Evaluation:
"""
        
        return prompt.strip()
    
    def _parse_evaluation_output(self, facet: str, output: ModelOutput) -> EvaluationResult:
        """Parse model output to extract evaluation result."""
        text = output.text.strip()
        
        # Extract score
        score = 3  # default
        reasoning = "Unable to parse evaluation"
        
        try:
            # Look for score pattern
            import re
            score_match = re.search(r'Score:\s*(\d)', text)
            if score_match:
                score = int(score_match.group(1))
                score = max(1, min(5, score))  # Ensure score is in valid range
            
            # Extract reasoning
            reasoning_match = re.search(r'Reasoning:\s*(.+?)(?:\n|$)', text, re.DOTALL)
            if reasoning_match:
                reasoning = reasoning_match.group(1).strip()
            
        except Exception as e:
            logger.warning(f"Error parsing evaluation output for {facet}: {e}")
        
        return EvaluationResult(
            facet=facet,
            score=score,
            confidence=output.confidence,
            reasoning=reasoning
        )
    
    def batch_evaluate(self, 
                      conversations: List[str], 
                      facets: List[str]) -> List[List[EvaluationResult]]:
        """Batch evaluate multiple conversations."""
        results = []
        
        for conversation in conversations:
            conv_results = self.evaluate_conversation(conversation, facets)
            results.append(conv_results)
            
            # Clean up memory after each conversation
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            gc.collect()
        
        return results


class ModelManager:
    """Manages multiple models and model loading."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.models: Dict[str, BaseModel] = {}
        self.current_model: Optional[BaseModel] = None
        self.executor = ThreadPoolExecutor(max_workers=1)  # Single worker for model operations
    
    def load_model(self, model_name: str) -> BaseModel:
        """Load a specific model."""
        if model_name in self.models:
            return self.models[model_name]
        
        # Create model instance
        model = OpenWeightsModel(model_name, self.config)
        
        # Load model (this is CPU/GPU intensive)
        model.load_model()
        
        # Cache the model
        self.models[model_name] = model
        self.current_model = model
        
        return model
    
    async def load_model_async(self, model_name: str) -> BaseModel:
        """Load model asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, self.load_model, model_name)
    
    def get_model(self, model_name: Optional[str] = None) -> BaseModel:
        """Get a loaded model."""
        if model_name:
            if model_name not in self.models:
                return self.load_model(model_name)
            return self.models[model_name]
        
        if self.current_model:
            return self.current_model
        
        # Load default model
        default_model = self.config.get('default_model', 'meta-llama/Llama-2-7b-chat-hf')
        return self.load_model(default_model)
    
    def unload_model(self, model_name: str) -> None:
        """Unload a model to free memory."""
        if model_name in self.models:
            del self.models[model_name]
            
            if self.current_model and self.current_model.model_name == model_name:
                self.current_model = None
            
            # Clean up GPU memory
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            gc.collect()
            
            logger.info(f"Unloaded model: {model_name}")
    
    def list_supported_models(self) -> List[str]:
        """List supported models."""
        return self.config.get('supported_models', [])
    
    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """Get information about a model."""
        info = {
            'name': model_name,
            'loaded': model_name in self.models,
            'supported': model_name in self.list_supported_models()
        }
        
        if model_name in self.models:
            model = self.models[model_name]
            info.update({
                'device': model.device,
                'model_name': model.model_name
            })
        
        return info