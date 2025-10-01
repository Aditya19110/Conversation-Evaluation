-- Initialize the conversation evaluation database
CREATE DATABASE IF NOT EXISTS conversation_eval;

-- Create tables for storing evaluation results
CREATE TABLE IF NOT EXISTS evaluations (
    id SERIAL PRIMARY KEY,
    conversation_id VARCHAR(255) UNIQUE NOT NULL,
    conversation_text TEXT NOT NULL,
    model_used VARCHAR(255) NOT NULL,
    processing_time FLOAT NOT NULL,
    overall_confidence FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS facet_scores (
    id SERIAL PRIMARY KEY,
    evaluation_id INTEGER REFERENCES evaluations(id) ON DELETE CASCADE,
    facet_name VARCHAR(100) NOT NULL,
    score INTEGER NOT NULL CHECK (score >= 1 AND score <= 5),
    confidence FLOAT NOT NULL CHECK (confidence >= 0 AND confidence <= 1),
    reasoning TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS batch_evaluations (
    id SERIAL PRIMARY KEY,
    batch_id VARCHAR(255) UNIQUE NOT NULL,
    total_conversations INTEGER NOT NULL,
    total_processing_time FLOAT NOT NULL,
    average_confidence FLOAT NOT NULL,
    facets_evaluated TEXT[], -- Array of facet names
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_evaluations_conversation_id ON evaluations(conversation_id);
CREATE INDEX IF NOT EXISTS idx_evaluations_model_used ON evaluations(model_used);
CREATE INDEX IF NOT EXISTS idx_evaluations_created_at ON evaluations(created_at);

CREATE INDEX IF NOT EXISTS idx_facet_scores_evaluation_id ON facet_scores(evaluation_id);
CREATE INDEX IF NOT EXISTS idx_facet_scores_facet_name ON facet_scores(facet_name);
CREATE INDEX IF NOT EXISTS idx_facet_scores_score ON facet_scores(score);

CREATE INDEX IF NOT EXISTS idx_batch_evaluations_batch_id ON batch_evaluations(batch_id);
CREATE INDEX IF NOT EXISTS idx_batch_evaluations_created_at ON batch_evaluations(created_at);

-- Insert sample data for testing
INSERT INTO evaluations (conversation_id, conversation_text, model_used, processing_time, overall_confidence) 
VALUES 
    ('sample_001', 'Hello, how are you today?', 'meta-llama/Llama-2-7b-chat-hf', 1.23, 0.85),
    ('sample_002', 'Thank you for your help!', 'meta-llama/Llama-2-7b-chat-hf', 0.98, 0.92)
ON CONFLICT (conversation_id) DO NOTHING;

INSERT INTO facet_scores (evaluation_id, facet_name, score, confidence, reasoning)
SELECT 
    e.id,
    unnest(ARRAY['grammar', 'politeness', 'clarity']) as facet_name,
    unnest(ARRAY[4, 5, 4]) as score,
    unnest(ARRAY[0.88, 0.95, 0.82]) as confidence,
    unnest(ARRAY[
        'Good grammatical structure with proper sentence formation',
        'Very polite greeting with appropriate tone',
        'Clear and easily understandable message'
    ]) as reasoning
FROM evaluations e 
WHERE e.conversation_id = 'sample_001'
AND NOT EXISTS (SELECT 1 FROM facet_scores fs WHERE fs.evaluation_id = e.id);

INSERT INTO facet_scores (evaluation_id, facet_name, score, confidence, reasoning)
SELECT 
    e.id,
    unnest(ARRAY['grammar', 'politeness', 'clarity']) as facet_name,
    unnest(ARRAY[5, 5, 5]) as score,
    unnest(ARRAY[0.92, 0.98, 0.89]) as confidence,
    unnest(ARRAY[
        'Perfect grammatical structure',
        'Excellent expression of gratitude and politeness',
        'Very clear and direct communication'
    ]) as reasoning
FROM evaluations e 
WHERE e.conversation_id = 'sample_002'
AND NOT EXISTS (SELECT 1 FROM facet_scores fs WHERE fs.evaluation_id = e.id);