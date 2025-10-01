# Deployment Guide

## Prerequisites

1. Get Hugging Face token from https://huggingface.co/settings/tokens
2. Create token with "Read" access

## API Deployment (Render)

1. Go to https://render.com and login with GitHub
2. Create new Web Service and connect repository
3. Configure settings:
   - Environment: Docker
   - Branch: main
4. Add environment variables:
   ```
   PORT=8000
   ENVIRONMENT=production
   CORS_ORIGINS=["https://your-netlify-url.netlify.app"]
   HUGGINGFACE_TOKEN=hf_your_token_here
   ```

## Frontend Deployment (Netlify)

1. Go to https://netlify.com and login with GitHub
2. Create new site from Git repository
3. Build settings are configured in netlify.toml
4. Update REACT_APP_API_URL with your Render API URL

## Configuration

### Render Environment Variables
- Add HUGGINGFACE_TOKEN to Render (API backend only)
- Update CORS_ORIGINS with actual Netlify URL

### Netlify Environment Variables  
- REACT_APP_API_URL is configured in netlify.toml
- Update with your actual Render API URL

## Testing

- API health: https://your-api.onrender.com/health
- Frontend: your-netlify-url.netlify.app
- Test conversation evaluation functionality