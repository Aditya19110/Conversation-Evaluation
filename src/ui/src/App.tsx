import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  Grid,
  Card,
  CardContent,
  LinearProgress,
  Chip,
  Alert,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  OutlinedInput,
  CircularProgress
} from '@mui/material';
import { 
  Send as SendIcon,
  Analytics as AnalyticsIcon,
  Psychology as PsychologyIcon 
} from '@mui/icons-material';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import { Bar } from 'react-chartjs-2';
import axios from 'axios';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

interface FacetResult {
  score: number;
  confidence: number;
  reasoning: string;
}

interface EvaluationResult {
  conversation_id: string;
  conversation_text: string;
  facet_scores: { [key: string]: FacetResult };
  confidence_metrics: {
    overall_confidence: number;
    model_confidence: number;
    consistency_score: number;
    uncertainty_estimate: number;
  };
  processing_time: number;
  model_used: string;
  timestamp: number;
}

const FACET_CATEGORIES = {
  'Linguistic Quality': ['grammar', 'coherence', 'fluency', 'vocabulary_richness', 'clarity'],
  'Pragmatics': ['appropriateness', 'relevance', 'politeness', 'context_understanding'],
  'Safety': ['toxicity', 'bias', 'harmful_content', 'hate_speech'],
  'Emotion': ['empathy', 'sentiment', 'emotional_appropriateness']
};

const ALL_FACETS = Object.values(FACET_CATEGORIES).flat();

function App() {
  const [conversationText, setConversationText] = useState('');
  const [selectedFacets, setSelectedFacets] = useState<string[]>(['grammar', 'clarity', 'politeness']);
  const [evaluationResult, setEvaluationResult] = useState<EvaluationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [availableModels, setAvailableModels] = useState<string[]>([]);
  const [selectedModel, setSelectedModel] = useState<string>('');

  useEffect(() => {
    fetchAvailableModels();
  }, []);

  const fetchAvailableModels = async () => {
    try {
      const response = await axios.get('/models');
      setAvailableModels(response.data);
      if (response.data.length > 0) {
        setSelectedModel(response.data[0]);
      }
    } catch (err) {
      console.error('Error fetching models:', err);
    }
  };

  const handleEvaluate = async () => {
    if (!conversationText.trim()) {
      setError('Please enter conversation text');
      return;
    }

    if (selectedFacets.length === 0) {
      setError('Please select at least one facet');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const requestData = {
        conversation: {
          text: conversationText,
          context: 'User evaluation request'
        },
        facets: selectedFacets,
        model_name: selectedModel || undefined
      };

      const response = await axios.post('/evaluate', requestData);
      setEvaluationResult(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error evaluating conversation');
      console.error('Evaluation error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 4) return '#4caf50'; // Green
    if (score >= 3) return '#ff9800'; // Orange
    return '#f44336'; // Red
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return '#4caf50';
    if (confidence >= 0.6) return '#ff9800';
    return '#f44336';
  };

  const chartData = evaluationResult ? {
    labels: Object.keys(evaluationResult.facet_scores).map(facet => 
      facet.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())
    ),
    datasets: [
      {
        label: 'Scores',
        data: Object.values(evaluationResult.facet_scores).map(result => result.score),
        backgroundColor: Object.values(evaluationResult.facet_scores).map(result => getScoreColor(result.score)),
        borderColor: Object.values(evaluationResult.facet_scores).map(result => getScoreColor(result.score)),
        borderWidth: 1,
      },
    ],
  } : null;

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Facet Evaluation Scores',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 5,
        ticks: {
          stepSize: 1,
        },
      },
    },
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h3" component="h1" gutterBottom align="center" color="primary">
        <PsychologyIcon sx={{ fontSize: 40, mr: 2, verticalAlign: 'middle' }} />
        Conversation Evaluation Benchmark
      </Typography>
      
      <Typography variant="subtitle1" align="center" color="text.secondary" sx={{ mb: 4 }}>
        Evaluate conversations across 300+ facets using open-weights language models
      </Typography>

      <Grid container spacing={3}>
        {/* Input Section */}
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
              <SendIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
              Input Conversation
            </Typography>
            
            <TextField
              fullWidth
              multiline
              rows={6}
              variant="outlined"
              label="Enter conversation text..."
              value={conversationText}
              onChange={(e) => setConversationText(e.target.value)}
              sx={{ mb: 3 }}
              placeholder="Example: Hello, how are you today? I hope you're having a wonderful day!"
            />

            <FormControl fullWidth sx={{ mb: 3 }}>
              <InputLabel>Evaluation Facets</InputLabel>
              <Select
                multiple
                value={selectedFacets}
                onChange={(e) => setSelectedFacets(e.target.value as string[])}
                input={<OutlinedInput label="Evaluation Facets" />}
                renderValue={(selected) => (
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    {selected.map((value) => (
                      <Chip key={value} label={value.replace('_', ' ')} size="small" />
                    ))}
                  </Box>
                )}
              >
                {Object.entries(FACET_CATEGORIES).map(([category, facets]) => [
                  <MenuItem key={category} disabled sx={{ fontWeight: 'bold' }}>
                    {category}
                  </MenuItem>,
                  ...facets.map((facet) => (
                    <MenuItem key={facet} value={facet} sx={{ pl: 4 }}>
                      {facet.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    </MenuItem>
                  ))
                ])}
              </Select>
            </FormControl>

            {availableModels.length > 0 && (
              <FormControl fullWidth sx={{ mb: 3 }}>
                <InputLabel>Model</InputLabel>
                <Select
                  value={selectedModel}
                  onChange={(e) => setSelectedModel(e.target.value)}
                  input={<OutlinedInput label="Model" />}
                >
                  {availableModels.map((model) => (
                    <MenuItem key={model} value={model}>
                      {model}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            )}

            <Button
              variant="contained"
              size="large"
              fullWidth
              onClick={handleEvaluate}
              disabled={loading}
              startIcon={loading ? <CircularProgress size={20} /> : <AnalyticsIcon />}
              sx={{ py: 1.5 }}
            >
              {loading ? 'Evaluating...' : 'Evaluate Conversation'}
            </Button>

            {error && (
              <Alert severity="error" sx={{ mt: 2 }}>
                {error}
              </Alert>
            )}
          </Paper>
        </Grid>

        {/* Results Section */}
        <Grid item xs={12} md={6}>
          {evaluationResult ? (
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h5" gutterBottom>
                <AnalyticsIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                Evaluation Results
              </Typography>

              {/* Overall Metrics */}
              <Grid container spacing={2} sx={{ mb: 3 }}>
                <Grid item xs={6}>
                  <Card variant="outlined">
                    <CardContent sx={{ textAlign: 'center' }}>
                      <Typography variant="h6" color="primary">
                        {(evaluationResult.confidence_metrics.overall_confidence * 100).toFixed(1)}%
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Overall Confidence
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={6}>
                  <Card variant="outlined">
                    <CardContent sx={{ textAlign: 'center' }}>
                      <Typography variant="h6" color="primary">
                        {evaluationResult.processing_time.toFixed(2)}s
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Processing Time
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>

              {/* Confidence Metrics */}
              <Box sx={{ mb: 3 }}>
                <Typography variant="h6" gutterBottom>Confidence Metrics</Typography>
                
                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" gutterBottom>
                    Model Confidence: {(evaluationResult.confidence_metrics.model_confidence * 100).toFixed(1)}%
                  </Typography>
                  <LinearProgress 
                    variant="determinate" 
                    value={evaluationResult.confidence_metrics.model_confidence * 100}
                    sx={{ 
                      height: 8, 
                      borderRadius: 4,
                      backgroundColor: '#e0e0e0',
                      '& .MuiLinearProgress-bar': {
                        backgroundColor: getConfidenceColor(evaluationResult.confidence_metrics.model_confidence)
                      }
                    }}
                  />
                </Box>

                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" gutterBottom>
                    Consistency Score: {(evaluationResult.confidence_metrics.consistency_score * 100).toFixed(1)}%
                  </Typography>
                  <LinearProgress 
                    variant="determinate" 
                    value={evaluationResult.confidence_metrics.consistency_score * 100}
                    sx={{ 
                      height: 8, 
                      borderRadius: 4,
                      backgroundColor: '#e0e0e0',
                      '& .MuiLinearProgress-bar': {
                        backgroundColor: getConfidenceColor(evaluationResult.confidence_metrics.consistency_score)
                      }
                    }}
                  />
                </Box>
              </Box>

              {/* Chart */}
              {chartData && (
                <Box sx={{ mb: 3 }}>
                  <Bar data={chartData} options={chartOptions} />
                </Box>
              )}

              {/* Detailed Facet Results */}
              <Typography variant="h6" gutterBottom>Detailed Results</Typography>
              <Box sx={{ maxHeight: 400, overflowY: 'auto' }}>
                {Object.entries(evaluationResult.facet_scores).map(([facet, result]) => (
                  <Card key={facet} variant="outlined" sx={{ mb: 2 }}>
                    <CardContent>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                        <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }}>
                          {facet.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                        </Typography>
                        <Box sx={{ display: 'flex', gap: 1 }}>
                          <Chip 
                            label={`Score: ${result.score}/5`} 
                            color={result.score >= 4 ? 'success' : result.score >= 3 ? 'warning' : 'error'}
                            size="small"
                          />
                          <Chip 
                            label={`${(result.confidence * 100).toFixed(0)}%`} 
                            variant="outlined"
                            size="small"
                          />
                        </Box>
                      </Box>
                      
                      <LinearProgress 
                        variant="determinate" 
                        value={(result.score / 5) * 100}
                        sx={{ 
                          mb: 1,
                          height: 6, 
                          borderRadius: 3,
                          backgroundColor: '#e0e0e0',
                          '& .MuiLinearProgress-bar': {
                            backgroundColor: getScoreColor(result.score)
                          }
                        }}
                      />
                      
                      <Typography variant="body2" color="text.secondary">
                        {result.reasoning}
                      </Typography>
                    </CardContent>
                  </Card>
                ))}
              </Box>

              <Typography variant="caption" color="text.secondary" sx={{ mt: 2, display: 'block' }}>
                Model: {evaluationResult.model_used} | 
                Evaluation ID: {evaluationResult.conversation_id}
              </Typography>
            </Paper>
          ) : (
            <Paper elevation={3} sx={{ p: 3, textAlign: 'center', minHeight: 400, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Box>
                <AnalyticsIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
                <Typography variant="h6" color="text.secondary">
                  Enter a conversation and select facets to see evaluation results
                </Typography>
              </Box>
            </Paper>
          )}
        </Grid>
      </Grid>
    </Container>
  );
}

export default App;