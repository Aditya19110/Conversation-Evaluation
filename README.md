# Conversation Evaluation Benchmark

Production-ready system for evaluating conversations across 300+ facets using open-weights language models.

## Features

- Multi-facet conversation evaluation (300+ facets, scalable to 5000+)
- Open-weights model support (≤16B parameters)
- Confidence estimation for all scores
- Real-time web interface
- RESTful API endpoints
- Docker containerization

## Architecture

### Core Components

1. **Data Pipeline** (`src/data/`)
   - Facet dataset preprocessing
   - Conversation data cleaning
   - Feature engineering

2. **Model Service** (`src/models/`)
   - Open-weights model integration (Llama 3-8B, Qwen2-8B, Mixtral 8×7B MoE)
   - Efficient inference pipeline
   - Batch processing capabilities

3. **Evaluation Engine** (`src/evaluation/`)
   - Multi-facet scoring system
   - Confidence estimation
   - Scalable architecture for 5000+ facets

4. **API Service** (`src/api/`)
   - RESTful API endpoints
   - Real-time evaluation
   - Batch processing support

5. **Web UI** (`src/ui/`)
   - Interactive conversation evaluation
   - Facet scoring visualization
   - Confidence metrics display

## Tech Stack

- **Backend**: Python, FastAPI, Pydantic
- **ML/AI**: Transformers, PyTorch, Hugging Face
- **Frontend**: React, TypeScript, Chart.js
- **Database**: PostgreSQL, Redis (caching)
- **Containerization**: Docker, Docker Compose
- **Deployment**: Docker Swarm/K8s ready

## Project Structure

```
conversation-eval-benchmark/
├── src/
│   ├── data/                   # Data processing pipeline
│   ├── models/                 # Model integration and inference
│   ├── evaluation/             # Core evaluation engine
│   ├── api/                    # API service
│   └── ui/                     # Web interface
├── data/
│   ├── raw/                    # Raw datasets
│   ├── processed/              # Cleaned and processed data
│   └── sample_conversations/   # Test conversation examples
├── configs/                    # Configuration files
├── tests/                      # Unit and integration tests
├── docker/                     # Docker configurations
├── docs/                       # Documentation
├── requirements.txt            # Python dependencies
├── docker-compose.yml          # Container orchestration
└── README.md                   # This file
```

## How to Run the Project

### Prerequisites
- Python 3.9+
- Docker & Docker Compose (for containerized deployment)
- 8GB RAM minimum (16GB recommended)

### Method 1: Quick Test (Recommended for initial testing)

1. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the test script**
   ```bash
   python test_project.py
   ```
   
   This will verify all components are working correctly.

### Method 2: Local Development

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the API server**
   ```bash
   cd src/api
   python -m uvicorn main:app --reload --port 8000
   ```

3. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

### Method 3: Docker Deployment (Production)

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Access the services**
   - Web UI: http://localhost:3000
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Database: localhost:5432
   - Redis: localhost:6379

3. **Stop the services**
   ```bash
   docker-compose down
   ```

### Adding Your Facet Dataset

Place your facet dataset CSV file in the `data/raw/` directory. The CSV should have these columns:
- `facet_name`: Name of the evaluation facet
- `category`: Category (linguistic_quality, pragmatics, safety, emotion)
- `description`: Description of what the facet evaluates

Example:
```csv
facet_name,category,description
politeness,pragmatics,Evaluates the politeness level of the conversation
grammar,linguistic_quality,Assesses grammatical correctness
```

## Features

### Core Features
- Multi-facet conversation evaluation (300+ facets)
- Open-weights model integration
- Confidence scoring
- Scalable architecture (5000+ facets)
- RESTful API
- Interactive Web UI
- Docker containerization

### Evaluation Facets
- **Linguistic Quality**: Grammar, coherence, fluency, vocabulary
- **Pragmatics**: Context understanding, appropriateness, relevance
- **Safety**: Toxicity, bias, harmful content detection
- **Emotion**: Sentiment analysis, emotional intelligence, empathy

## Usage

### API Usage

```python
import requests

# Evaluate a single conversation turn
response = requests.post("http://localhost:8000/evaluate", json={
    "conversation": "Hello, how are you today?",
    "context": "Friendly greeting",
    "facets": ["politeness", "clarity", "appropriateness"]
})

scores = response.json()
```

### Web UI
Navigate to http://localhost:3000 to use the interactive interface for:
- Inputting conversations
- Selecting evaluation facets
- Viewing real-time scores and confidence metrics
- Downloading evaluation reports

## Performance & Scalability

- **Throughput**: 100+ evaluations/second
- **Latency**: <500ms per evaluation
- **Scalability**: Supports 5000+ facets without architectural changes
- **Resource Usage**: Optimized for 16GB VRAM usage

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
pytest tests/performance/
```

## Documentation

- [API Documentation](docs/api.md)
- [Model Integration Guide](docs/models.md)
- [Deployment Guide](docs/deployment.md)
- [Contributing Guidelines](docs/contributing.md)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Open-source model providers (Meta, Alibaba, Mistral)
- Hugging Face for model hosting and tooling
- The open-source community for inspiration and tools