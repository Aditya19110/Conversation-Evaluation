# Quick Deployment Guide

## Deploy to Netlify (Frontend) + Render (API)

### 1. Deploy API to Render
1. Go to https://render.com → Login with GitHub
2. "New +" → "Web Service" → Connect your repository
3. **Settings**:
   - Name: `conversation-evaluation-api`
   - Environment: `Docker`
   - Branch: `main`
4. **Environment Variables**:
   - `PORT=8000`
   - `ENVIRONMENT=production`
   - `CORS_ORIGINS=["https://your-netlify-url.netlify.app"]`

### 2. Deploy Frontend to Netlify
1. Go to https://netlify.com → Login with GitHub
2. "Add new site" → "Import from Git" → Select repository
3. **Build Settings**: Auto-detected from `netlify.toml`
   - Build command: `cd src/ui && npm ci && npm run build`
   - Publish directory: `src/ui/build`
4. **Deploy**: Click "Deploy Site"

### 3. Connect Services
1. Copy your Netlify URL (e.g., `https://amazing-app-123.netlify.app`)
2. Update Render API environment variable:
   - `CORS_ORIGINS=["https://amazing-app-123.netlify.app"]`
3. Update `netlify.toml` with your actual API URL if needed

## Test Deployment
- **API**: `https://your-api.onrender.com/health`
- **Frontend**: Your Netlify URL
- **Integration**: Test conversation evaluation in the UI

Your full-stack system is now live! 🚀