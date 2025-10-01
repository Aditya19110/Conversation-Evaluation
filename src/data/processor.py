import os
import re
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

import pandas as pd

logger = logging.getLogger(__name__)


@dataclass
class ConversationTurn:
    """Represents a single conversation turn."""
    text: str
    speaker: Optional[str] = None
    timestamp: Optional[float] = None
    context: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class FacetDefinition:
    """Represents a facet for evaluation."""
    name: str
    category: str
    description: str
    keywords: List[str]
    weight: float = 1.0


class DataProcessor:
    """Main data processing class for conversation evaluation."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.facets = self._load_facet_definitions()
        
    def _load_facet_definitions(self) -> Dict[str, FacetDefinition]:
        """Load facet definitions from configuration."""
        facets = {}
        
        for category, facet_names in self.config.get('facets', {}).items():
            for facet_name in facet_names:
                facets[facet_name] = FacetDefinition(
                    name=facet_name,
                    category=category,
                    description=f"Evaluates {facet_name.replace('_', ' ')} in conversations",
                    keywords=self._generate_keywords(facet_name)
                )
        
        return facets
    
    def _generate_keywords(self, facet_name: str) -> List[str]:
        """Generate relevant keywords for a facet."""
        keyword_mapping = {
            'grammar': ['syntax', 'tense', 'subject-verb', 'punctuation'],
            'coherence': ['logical', 'consistent', 'connected', 'flow'],
            'fluency': ['smooth', 'natural', 'effortless', 'articulate'],
            'vocabulary_richness': ['diverse', 'varied', 'sophisticated', 'expressive'],
            'clarity': ['clear', 'understandable', 'precise', 'unambiguous'],
            'appropriateness': ['suitable', 'proper', 'fitting', 'relevant'],
            'politeness': ['courteous', 'respectful', 'civil', 'mannerly'],
            'toxicity': ['offensive', 'harmful', 'abusive', 'hostile'],
            'empathy': ['understanding', 'compassionate', 'caring', 'supportive'],
            'sentiment': ['positive', 'negative', 'neutral', 'emotional']
        }
        
        return keyword_mapping.get(facet_name, [facet_name.replace('_', ' ')])
    
    def clean_conversation_text(self, text: str) -> str:
        """Clean and normalize conversation text."""
        if not isinstance(text, str):
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Normalize quotes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        
        # Remove excessive special characters (keeping common punctuation)
        text = re.sub(r'[^\w\s\.,!?;:\'\"-]', '', text)
        
        # Ensure proper sentence ending
        if text and not text[-1] in '.!?':
            text += '.'
        
        return text
    
    def extract_features(self, conversation: ConversationTurn) -> Dict[str, float]:
        """Extract numerical features from conversation turn."""
        text = conversation.text
        features = {}
        
        # Basic text statistics
        features['word_count'] = len(text.split())
        features['char_count'] = len(text)
        features['sentence_count'] = len(re.findall(r'[.!?]+', text))
        word_lengths = [len(word) for word in text.split()]
        features['avg_word_length'] = sum(word_lengths) / len(word_lengths) if word_lengths else 0
        
        # Linguistic features
        features['question_count'] = text.count('?')
        features['exclamation_count'] = text.count('!')
        features['uppercase_ratio'] = sum(1 for c in text if c.isupper()) / len(text) if text else 0
        features['punctuation_ratio'] = sum(1 for c in text if c in '.,!?;:') / len(text) if text else 0
        
        # Complexity measures
        words = text.split()
        features['unique_word_ratio'] = len(set(words)) / len(words) if words else 0
        features['avg_sentence_length'] = features['word_count'] / features['sentence_count'] if features['sentence_count'] > 0 else 0
        
        return features
    
    def preprocess_facet_dataset(self, file_path: str) -> pd.DataFrame:
        """Load and preprocess the facet dataset."""
        try:
            # Try different file formats
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_path}")
            
            logger.info(f"Loaded dataset with {len(df)} rows and {len(df.columns)} columns")
            
            # Clean column names
            df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace(r'[^a-zA-Z0-9_]', '', regex=True)
            
            # Add additional evaluation columns
            df = self._add_evaluation_columns(df)
            
            # Validate and clean data
            df = self._validate_and_clean_data(df)
            
            return df
            
        except Exception as e:
            logger.error(f"Error preprocessing facet dataset: {e}")
            raise
    
    def _add_evaluation_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add additional columns for evaluation."""
        # Add facet category mapping
        facet_categories = {}
        for facet_name in df.columns:
            if facet_name in self.facets:
                facet_categories[facet_name] = self.facets[facet_name].category
        
        # Add metadata columns
        df['total_facets'] = len([col for col in df.columns if col in self.facets])
        df['evaluation_timestamp'] = pd.Timestamp.now()
        df['facet_categories'] = str(facet_categories)
        
        # Add derived features
        if 'conversation_text' in df.columns or 'text' in df.columns:
            text_col = 'conversation_text' if 'conversation_text' in df.columns else 'text'
            
            # Extract text features
            for idx, row in df.iterrows():
                conv_turn = ConversationTurn(text=str(row[text_col]))
                features = self.extract_features(conv_turn)
                
                for feature_name, feature_value in features.items():
                    if f'feature_{feature_name}' not in df.columns:
                        df[f'feature_{feature_name}'] = None
                    df.loc[idx, f'feature_{feature_name}'] = feature_value
        
        return df
    
    def _validate_and_clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate and clean the dataset."""
        initial_rows = len(df)
        
        # Remove rows with all NaN values
        df = df.dropna(how='all')
        
        # Clean text columns
        text_columns = [col for col in df.columns if 'text' in col.lower() or 'conversation' in col.lower()]
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).apply(self.clean_conversation_text)
                # Remove empty text entries
                df = df[df[col].str.len() > 0]
        
        # Validate score columns (should be integers in range 1-5)
        score_columns = [col for col in df.columns if col in self.facets]
        for col in score_columns:
            if col in df.columns:
                # Convert to numeric, coerce errors to NaN
                df[col] = pd.to_numeric(df[col], errors='coerce')
                # Filter valid scores (1-5 range)
                df = df[(df[col].isna()) | ((df[col] >= 1) & (df[col] <= 5))]
        
        logger.info(f"Data validation completed. Removed {initial_rows - len(df)} invalid rows.")
        
        return df
    
    def create_conversation_batches(self, 
                                  conversations: List[ConversationTurn], 
                                  batch_size: int = 32) -> List[List[ConversationTurn]]:
        """Create batches of conversations for efficient processing."""
        batches = []
        for i in range(0, len(conversations), batch_size):
            batch = conversations[i:i + batch_size]
            batches.append(batch)
        return batches
    
    def prepare_evaluation_data(self, 
                              conversations: List[ConversationTurn],
                              facets: List[str]) -> Dict[str, Any]:
        """Prepare data for evaluation."""
        # Validate facets
        valid_facets = [f for f in facets if f in self.facets]
        invalid_facets = [f for f in facets if f not in self.facets]
        
        if invalid_facets:
            logger.warning(f"Invalid facets will be ignored: {invalid_facets}")
        
        # Prepare data structure
        evaluation_data = {
            'conversations': conversations,
            'facets': valid_facets,
            'facet_definitions': {f: self.facets[f] for f in valid_facets},
            'features': []
        }
        
        # Extract features for each conversation
        for conv in conversations:
            features = self.extract_features(conv)
            evaluation_data['features'].append(features)
        
        return evaluation_data
    
    def save_processed_data(self, df: pd.DataFrame, output_path: str) -> None:
        """Save processed data to file."""
        try:
            if output_path.endswith('.csv'):
                df.to_csv(output_path, index=False)
            elif output_path.endswith(('.xlsx', '.xls')):
                df.to_excel(output_path, index=False)
            else:
                # Default to CSV
                output_path = output_path + '.csv'
                df.to_csv(output_path, index=False)
            
            logger.info(f"Processed data saved to {output_path}")
            
        except Exception as e:
            logger.error(f"Error saving processed data: {e}")
            raise