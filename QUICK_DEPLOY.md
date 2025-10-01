# Railway Deployment - Step by Step

Railway is the easiest way to deploy your project. Follow these exact steps:

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

## Step 2: Deploy on Railway

1. **Go to Railway**
   - Visit https://railway.app
   - Click "Login" → "Login with GitHub"

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository `conversation-evaluation`

3. **Configure Deployment**
   - Railway will detect your `Dockerfile` automatically
   - Click "Deploy Now"
   - Wait 2-3 minutes for build to complete

4. **Get Your URL**
   - Go to "Settings" → "Domains"
   - Click "Generate Domain"
   - You'll get a URL like: `https://conversation-evaluation-production.up.railway.app`

## Step 3: Test Your Deployment

Visit your URLs:
- **API Health**: `https://your-url.railway.app/health`
- **API Docs**: `https://your-url.railway.app/docs`
- **Test Endpoint**: `https://your-url.railway.app/`

## Step 4: Add Database (Optional)

1. **Add PostgreSQL**
   - In Railway dashboard, click "New"
   - Select "PostgreSQL"
   - Railway will provide connection details

2. **Connect to your app**
   - Go to your web service
   - Add environment variable `DATABASE_URL`
   - Use the PostgreSQL connection string

## That's it! Your website is live!

Your API is now accessible worldwide at your Railway URL.

## Custom Domain (Optional)

1. **Buy a domain** (from Namecheap, GoDaddy, etc.)
2. **In Railway**:
   - Go to Settings → Domains
   - Click "Custom Domain"
   - Enter your domain
3. **Update DNS**:
   - Add CNAME record pointing to Railway

## Environment Variables

Add these in Railway dashboard → Variables:
- `ENVIRONMENT=production`
- `PORT=8000`
- `DEBUG=false`

## Monitoring

Railway provides:
- Automatic HTTPS
- Health checks
- Logs viewer
- Usage metrics
- Automatic deployments on git push

Your conversation evaluation system is now live on the web!