# Deployment Guide

Deploy your Conversation Evaluation system with API on Render and Frontend on Netlify.

## Architecture
```
React Frontend (Netlify) ← → Python API (Render) ← → Database (Render)
```

## Part 1: Deploy API Backend (Render)

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/conversation-evaluation.git
git push -u origin main
```

### Step 2: Deploy API
1. **Go to Render**: https://render.com → Login with GitHub
2. **Create Web Service**: "New +" → "Web Service" → Connect repository
3. **Configure**:
   - Name: `conversation-evaluation-api`
   - Environment: `Docker`
   - Branch: `main`
4. **Environment Variables**:
   - `PORT=8000`
   - `ENVIRONMENT=production`
   - `CORS_ORIGINS=["https://your-app.netlify.app"]`
5. **Deploy**: Wait 3-5 minutes

**Your API**: `https://conversation-evaluation-api.onrender.com`

## Part 2: Deploy Frontend (Netlify)

### Step 1: Update API URL
Update your API URL in `netlify.toml` environment section and `src/ui/.env.production`:
```bash
REACT_APP_API_URL=https://your-actual-api.onrender.com
```

### Step 2: Deploy Frontend
1. **Go to Netlify**: https://netlify.com → Login with GitHub
2. **New Site**: "Add new site" → "Import from Git"
3. **Build Settings**:
   - Build command: `npm run build` (Netlify will auto-detect from netlify.toml)
   - Publish directory: `build` (relative to base: src/ui)
   - Base directory: `src/ui`
4. **Environment Variables**: Already configured in netlify.toml

**Your Frontend**: `https://conversation-eval.netlify.app`

## Part 3: Connect Services

### Update API CORS
In `src/api/main.py`, update CORS:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://conversation-eval.netlify.app",  # Your Netlify URL
        "http://localhost:3000"  # Local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
Redeploy API after this change.

## Testing Your Deployment

### API Tests
- Health: `https://your-api.onrender.com/health`
- Docs: `https://your-api.onrender.com/docs`

### Frontend Tests  
- Visit your Netlify URL
- Test conversation evaluation
- Check API connection status

## Optional: Database Setup

1. **Create PostgreSQL**: Render → "New +" → "PostgreSQL"
2. **Connect**: Add `DATABASE_URL` environment variable to API

## Environment Variables Summary

### API (Render)
- `PORT=8000`
- `ENVIRONMENT=production`
- `CORS_ORIGINS=["https://your-netlify-url.netlify.app"]`
- `DATABASE_URL=...` (optional)

### Frontend (Netlify)
- `REACT_APP_API_URL=https://your-api.onrender.com`

## Cost
- **Free Tier**: API + Frontend + Database all free
- **Paid**: $7/month for always-on API (optional)

Your full-stack conversation evaluation system is now live!