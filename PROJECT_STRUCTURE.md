# Conversation Evaluation Benchmark

A production-ready system for evaluating conversation quality using open-weights models. Features comprehensive evaluation across 300+ facets with 5-point scoring and scalable architecture supporting up to 5000 facets.

## Architecture

### Backend (API)
- **Framework**: FastAPI with Python 3.9
- **Models**: Llama 3-8B, Qwen2-8B, Mixtral 8×7B MoE (≤16B constraint)
- **Features**: Async processing, batch evaluation, confidence metrics
- **Deployment**: Render platform with Docker containerization

### Frontend (UI)
- **Framework**: React 18 with TypeScript
- **UI Library**: Material-UI components
- **Visualization**: Chart.js for metrics display
- **Deployment**: Netlify static hosting

## Key Components

- `src/data/processor.py` - Data processing and feature extraction
- `src/models/inference.py` - Model integration and quantization
- `src/evaluation/engine.py` - Core evaluation system
- `src/api/main.py` - FastAPI application
- `src/ui/` - React frontend application

## Deployment

Use the streamlined `DEPLOY.md` guide for complete deployment instructions to Render (API) and Netlify (frontend).

## Development

```bash
# Backend
pip install -r requirements.txt
python src/api/main.py

# Frontend
cd src/ui
npm install
npm start
```

## Testing

```bash
python test_project.py
```