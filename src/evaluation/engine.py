from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, asdict
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time
import json
from enum import Enum

try:
    from ..models.inference import ModelManager, EvaluationResult
    from ..data.processor import ConversationTurn, DataProcessor
except ImportError:
    # Fallback classes for when ML dependencies aren't installed
    class MockModelManager:
        def __init__(self, config):
            self.config = config
            
        def get_model(self, model_name=None):
            return MockModel()
    
    class MockModel:
        def evaluate_conversation(self, conversation, facets):
            return [MockEvaluationResult(facet) for facet in facets]
    
    class MockEvaluationResult:
        def __init__(self, facet):
            self.facet = facet
            self.score = 3
            self.confidence = 0.8
            self.reasoning = "Mock evaluation result"
    
    class MockConversationTurn:
        def __init__(self, text, speaker=None):
            self.text = text
            self.speaker = speaker
    
    class MockDataProcessor:
        def process_conversation(self, data):
            return data
    
    ModelManager = MockModelManager
    EvaluationResult = MockEvaluationResult
    ConversationTurn = MockConversationTurn  
    DataProcessor = MockDataProcessor

logger = logging.getLogger(__name__)


class ScoreScale(Enum):
    """Enumeration for score scale."""
    VERY_POOR = 1
    POOR = 2
    AVERAGE = 3
    GOOD = 4
    EXCELLENT = 5


@dataclass
class ConfidenceMetrics:
    """Confidence metrics for evaluation results."""
    overall_confidence: float
    model_confidence: float
    consistency_score: float
    uncertainty_estimate: float


@dataclass
class ConversationEvaluation:
    """Complete evaluation result for a conversation."""
    conversation_id: str
    conversation_text: str
    facet_scores: Dict[str, EvaluationResult]
    confidence_metrics: ConfidenceMetrics
    processing_time: float
    model_used: str
    timestamp: float


@dataclass
class BatchEvaluationResult:
    """Result of batch evaluation."""
    evaluations: List[ConversationEvaluation]
    total_processing_time: float
    average_confidence: float
    facet_statistics: Dict[str, Dict[str, float]]


class FacetEvaluator:
    """Handles evaluation of individual facets."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.facet_weights = self._load_facet_weights()
    
    def _load_facet_weights(self) -> Dict[str, float]:
        """Load facet weights from configuration."""
        weights = {}
        
        # Default weights (can be customized in config)
        default_weights = {
            # Linguistic Quality
            'grammar': 1.0,
            'coherence': 1.2,
            'fluency': 1.0,
            'vocabulary_richness': 0.8,
            'clarity': 1.3,
            
            # Pragmatics
            'appropriateness': 1.5,
            'relevance': 1.4,
            'politeness': 1.1,
            'context_understanding': 1.3,
            
            # Safety (higher weights due to importance)
            'toxicity': 2.0,
            'bias': 1.8,
            'harmful_content': 2.0,
            'hate_speech': 2.0,
            
            # Emotion
            'empathy': 1.2,
            'sentiment': 1.0,
            'emotional_appropriateness': 1.1
        }
        
        # Override with config values if available
        config_weights = self.config.get('facet_weights', {})
        weights.update(default_weights)
        weights.update(config_weights)
        
        return weights
    
    def calculate_weighted_score(self, 
                               facet_results: List[EvaluationResult]) -> float:
        """Calculate weighted average score across facets."""
        if not facet_results:
            return 0.0
        
        total_weighted_score = 0.0
        total_weight = 0.0
        
        for result in facet_results:
            weight = self.facet_weights.get(result.facet, 1.0)
            weighted_score = result.score * weight * result.confidence
            
            total_weighted_score += weighted_score
            total_weight += weight * result.confidence
        
        return total_weighted_score / total_weight if total_weight > 0 else 0.0
    
    def analyze_facet_consistency(self, 
                                facet_results: List[EvaluationResult]) -> float:
        """Analyze consistency across related facets."""
        if len(facet_results) < 2:
            return 1.0
        
        # Group facets by category
        categories = {}
        for result in facet_results:
            category = self._get_facet_category(result.facet)
            if category not in categories:
                categories[category] = []
            categories[category].append(result.score)
        
        # Calculate consistency within categories
        consistency_scores = []
        
        for category, scores in categories.items():
            if len(scores) > 1:
                # Calculate variance (lower variance = higher consistency)
                mean_score = sum(scores) / len(scores)
                variance = sum((s - mean_score) ** 2 for s in scores) / len(scores)
                # Normalize to 0-1 scale (higher = more consistent)
                consistency = max(0, 1 - variance / 4)  # Max variance is 4 for 1-5 scale
                consistency_scores.append(consistency)
        
        return sum(consistency_scores) / len(consistency_scores) if consistency_scores else 1.0
    
    def _get_facet_category(self, facet: str) -> str:
        """Get category for a facet."""
        linguistic_facets = ['grammar', 'coherence', 'fluency', 'vocabulary_richness', 'clarity']
        pragmatic_facets = ['appropriateness', 'relevance', 'politeness', 'context_understanding']
        safety_facets = ['toxicity', 'bias', 'harmful_content', 'hate_speech']
        emotion_facets = ['empathy', 'sentiment', 'emotional_appropriateness']
        
        if facet in linguistic_facets:
            return 'linguistic_quality'
        elif facet in pragmatic_facets:
            return 'pragmatics'  
        elif facet in safety_facets:
            return 'safety'
        elif facet in emotion_facets:
            return 'emotion'
        else:
            return 'other'


class ConversationEvaluationEngine:
    """Main evaluation engine for conversations."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model_manager = ModelManager(config.get('models', {}))
        self.data_processor = DataProcessor(config)
        self.facet_evaluator = FacetEvaluator(config)
        self.executor = ThreadPoolExecutor(max_workers=config.get('max_workers', 4))
    
    async def evaluate_conversation(self,
                                  conversation: Union[str, ConversationTurn],
                                  facets: List[str],
                                  conversation_id: Optional[str] = None,
                                  model_name: Optional[str] = None) -> ConversationEvaluation:
        """Evaluate a single conversation."""
        start_time = time.time()
        
        # Prepare conversation
        if isinstance(conversation, str):
            conv_turn = ConversationTurn(text=conversation)
        else:
            conv_turn = conversation
        
        conversation_id = conversation_id or f"conv_{int(time.time())}"
        
        # Clean conversation text
        clean_text = self.data_processor.clean_conversation_text(conv_turn.text)
        
        # Get model
        model = await self.model_manager.load_model_async(
            model_name or self.config.get('default_model')
        )
        
        # Evaluate on all facets
        facet_results = await self._evaluate_facets_async(clean_text, facets, model)
        
        # Calculate confidence metrics
        confidence_metrics = self._calculate_confidence_metrics(facet_results)
        
        # Create evaluation result
        processing_time = time.time() - start_time
        
        evaluation = ConversationEvaluation(
            conversation_id=conversation_id,
            conversation_text=clean_text,
            facet_scores={result.facet: result for result in facet_results},
            confidence_metrics=confidence_metrics,
            processing_time=processing_time,
            model_used=model.model_name,
            timestamp=time.time()
        )
        
        return evaluation
    
    async def _evaluate_facets_async(self,
                                   conversation: str,
                                   facets: List[str],
                                   model) -> List[EvaluationResult]:
        """Evaluate facets asynchronously."""
        # Split facets into batches for efficiency
        batch_size = self.config.get('facet_batch_size', 10)
        facet_batches = [facets[i:i + batch_size] for i in range(0, len(facets), batch_size)]
        
        all_results = []
        
        for batch in facet_batches:
            # Run batch evaluation in executor to avoid blocking
            loop = asyncio.get_event_loop()
            batch_results = await loop.run_in_executor(
                self.executor,
                model.evaluate_conversation,
                conversation,
                batch
            )
            all_results.extend(batch_results)
        
        return all_results
    
    def _calculate_confidence_metrics(self, 
                                    facet_results: List[EvaluationResult]) -> ConfidenceMetrics:
        """Calculate comprehensive confidence metrics."""
        if not facet_results:
            return ConfidenceMetrics(0.0, 0.0, 0.0, 1.0)
        
        # Overall confidence (average of individual confidences)
        overall_confidence = sum(r.confidence for r in facet_results) / len(facet_results)
        
        # Model confidence (weighted by facet importance)
        weighted_confidences = []
        for result in facet_results:
            weight = self.facet_evaluator.facet_weights.get(result.facet, 1.0)
            weighted_confidences.append(result.confidence * weight)
        
        model_confidence = sum(weighted_confidences) / sum(
            self.facet_evaluator.facet_weights.get(r.facet, 1.0) for r in facet_results
        )
        
        # Consistency score
        consistency_score = self.facet_evaluator.analyze_facet_consistency(facet_results)
        
        # Uncertainty estimate (higher = more uncertain)
        score_variance = self._calculate_score_variance(facet_results)
        uncertainty_estimate = min(1.0, score_variance / 2.0)  # Normalize
        
        return ConfidenceMetrics(
            overall_confidence=overall_confidence,
            model_confidence=model_confidence,
            consistency_score=consistency_score,
            uncertainty_estimate=uncertainty_estimate
        )
    
    def _calculate_score_variance(self, facet_results: List[EvaluationResult]) -> float:
        """Calculate variance in scores across facets."""
        if len(facet_results) < 2:
            return 0.0
        
        scores = [r.score for r in facet_results]
        mean_score = sum(scores) / len(scores)
        variance = sum((s - mean_score) ** 2 for s in scores) / len(scores)
        
        return variance
    
    async def batch_evaluate(self,
                           conversations: List[Union[str, ConversationTurn]],
                           facets: List[str],
                           model_name: Optional[str] = None) -> BatchEvaluationResult:
        """Evaluate multiple conversations in batch."""
        start_time = time.time()
        
        # Create evaluation tasks
        tasks = []
        for i, conversation in enumerate(conversations):
            task = self.evaluate_conversation(
                conversation=conversation,
                facets=facets,
                conversation_id=f"batch_conv_{i}",
                model_name=model_name
            )
            tasks.append(task)
        
        # Execute all evaluations concurrently
        evaluations = await asyncio.gather(*tasks)
        
        # Calculate batch statistics
        total_time = time.time() - start_time
        avg_confidence = sum(e.confidence_metrics.overall_confidence for e in evaluations) / len(evaluations)
        
        # Calculate facet statistics
        facet_stats = self._calculate_facet_statistics(evaluations, facets)
        
        return BatchEvaluationResult(
            evaluations=evaluations,
            total_processing_time=total_time,
            average_confidence=avg_confidence,
            facet_statistics=facet_stats
        )
    
    def _calculate_facet_statistics(self,
                                  evaluations: List[ConversationEvaluation],
                                  facets: List[str]) -> Dict[str, Dict[str, float]]:
        """Calculate statistics for each facet across all evaluations."""
        stats = {}
        
        for facet in facets:
            facet_scores = []
            facet_confidences = []
            
            for evaluation in evaluations:
                if facet in evaluation.facet_scores:
                    result = evaluation.facet_scores[facet]
                    facet_scores.append(result.score)
                    facet_confidences.append(result.confidence)
            
            if facet_scores:
                stats[facet] = {
                    'mean_score': sum(facet_scores) / len(facet_scores),
                    'min_score': min(facet_scores),
                    'max_score': max(facet_scores),
                    'score_std': (sum((s - sum(facet_scores)/len(facet_scores))**2 for s in facet_scores) / len(facet_scores))**0.5,
                    'mean_confidence': sum(facet_confidences) / len(facet_confidences),
                    'evaluation_count': len(facet_scores)
                }
        
        return stats
    
    def export_evaluation_results(self, 
                                results: Union[ConversationEvaluation, BatchEvaluationResult],
                                format: str = 'json') -> str:
        """Export evaluation results in specified format."""
        if isinstance(results, ConversationEvaluation):
            data = asdict(results)
        else:
            data = asdict(results)
        
        if format.lower() == 'json':
            return json.dumps(data, indent=2, default=str)
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    async def evaluate_with_multiple_models(self,
                                          conversation: Union[str, ConversationTurn],
                                          facets: List[str],
                                          model_names: List[str]) -> Dict[str, ConversationEvaluation]:
        """Evaluate with multiple models for comparison."""
        tasks = []
        
        for model_name in model_names:
            task = self.evaluate_conversation(
                conversation=conversation,
                facets=facets,
                model_name=model_name
            )
            tasks.append(task)
        
        evaluations = await asyncio.gather(*tasks)
        
        return {
            model_names[i]: evaluations[i] 
            for i in range(len(model_names))
        }
    
    def compare_evaluations(self,
                          evaluations: Dict[str, ConversationEvaluation]) -> Dict[str, Any]:
        """Compare evaluations from different models."""
        if len(evaluations) < 2:
            return {"error": "Need at least 2 evaluations to compare"}
        
        comparison = {
            "model_agreements": {},
            "score_differences": {},
            "confidence_comparison": {},
            "consensus_scores": {}
        }
        
        # Get all facets
        all_facets = set()
        for evaluation in evaluations.values():
            all_facets.update(evaluation.facet_scores.keys())
        
        # Compare each facet across models
        for facet in all_facets:
            facet_scores = {}
            facet_confidences = {}
            
            for model_name, evaluation in evaluations.items():
                if facet in evaluation.facet_scores:
                    result = evaluation.facet_scores[facet]
                    facet_scores[model_name] = result.score
                    facet_confidences[model_name] = result.confidence
            
            if len(facet_scores) >= 2:
                scores = list(facet_scores.values())
                
                # Calculate agreement (how similar the scores are)
                score_range = max(scores) - min(scores)
                agreement = max(0, 1 - score_range / 4)  # Normalize to 0-1
                
                comparison["model_agreements"][facet] = agreement
                comparison["score_differences"][facet] = facet_scores
                comparison["confidence_comparison"][facet] = facet_confidences
                
                # Consensus score (weighted by confidence)
                weighted_sum = sum(score * facet_confidences[model] 
                                 for model, score in facet_scores.items() 
                                 if model in facet_confidences)
                weight_sum = sum(facet_confidences.values())
                
                consensus = weighted_sum / weight_sum if weight_sum > 0 else sum(scores) / len(scores)
                comparison["consensus_scores"][facet] = consensus
        
        return comparison