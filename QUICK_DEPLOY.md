# Render Deployment - Step by Step

Render is an excellent platform for deploying your API with free tier and automatic SSL. Follow these exact steps:

## Prerequisites
- GitHub account
- Your project pushed to GitHub

## Step 1: Push to GitHub
```bash
# In your project directory
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/conversation-evaluation.git
git push -u origin main
```

## Step 2: Deploy on Render

1. **Go to Render**
   - Visit https://render.com
   - Click "Get Started" → "GitHub" to login

2. **Create Web Service**
   - Click "New +" → "Web Service"
   - Click "Connect" next to your repository
   - Choose your repository `conversation-evaluation`

3. **Configure Service**
   - **Name**: `conversation-evaluation-api`
   - **Environment**: `Docker`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Docker Command**: Leave empty (uses Dockerfile)

4. **Set Environment Variables**
   - Click "Advanced" 
   - Add: `PORT = 8000`
   - Add: `ENVIRONMENT = production`

5. **Deploy**
   - Click "Create Web Service"
   - Wait 3-5 minutes for build to complete

6. **Get Your URL**
   - You'll get a URL like: `https://conversation-evaluation-api.onrender.com`

## Step 3: Test Your Deployment

Visit your URLs:
- **API Health**: `https://your-app.onrender.com/health`
- **API Docs**: `https://your-app.onrender.com/docs`
- **Test Endpoint**: `https://your-app.onrender.com/`

## Step 4: Add Database (Optional)

1. **Create PostgreSQL Database**
   - In Render dashboard, click "New +" → "PostgreSQL"
   - Choose a name: `conversation-eval-db`
   - Select free tier
   - Click "Create Database"

2. **Connect to your API**
   - Go to your web service settings
   - Add environment variable `DATABASE_URL`
   - Copy the "Internal Database URL" from your PostgreSQL service

## Step 5: Add Redis (Optional)

1. **Create Redis Instance**
   - Click "New +" → "Redis"
   - Name: `conversation-eval-redis`
   - Click "Create Redis"

2. **Connect to API**
   - Add environment variable `REDIS_URL`
   - Use the Redis connection URL

## That's it! Your website is live!

Your API is now accessible worldwide at your Render URL.

## Custom Domain (Optional)

1. **Buy a domain** (from Namecheap, GoDaddy, etc.)
2. **In Render**:
   - Go to Settings → Custom Domains
   - Click "Add Custom Domain"
   - Enter your domain
3. **Update DNS**:
   - Add CNAME record pointing to your Render URL

## Frontend Deployment (Optional)

If you want to deploy the React frontend as well:

### Deploy Frontend on Netlify
1. **Go to Netlify**: https://netlify.com → Login with GitHub
2. **New Site**: "Add new site" → "Import from Git"
3. **Build Settings**:
   - Build command: `cd src/ui && npm ci && npm run build`
   - Publish directory: `src/ui/build`
4. **Environment Variables**:
   - `REACT_APP_API_URL=https://your-api.onrender.com`

### Complete Setup
- **Frontend**: `https://your-app.netlify.app`
- **API**: `https://your-api.onrender.com`

## Environment Variables

Add these in Render dashboard → Environment:
- `ENVIRONMENT=production`
- `PORT=8000`
- `DEBUG=false`
- `CORS_ORIGINS=["https://your-app.netlify.app"]` (if using frontend)

## Monitoring

Render provides:
- Automatic HTTPS/SSL certificates
- Health checks and monitoring
- Real-time logs viewer
- Usage metrics and analytics
- Automatic deployments on git push
- 99.9% uptime SLA

## Free Tier Limits

Render Free Tier includes:
- 512MB RAM
- 0.1 CPU
- Sleeps after 15 minutes of inactivity
- 750 hours/month (enough for personal projects)

Your conversation evaluation system is now live on the web!