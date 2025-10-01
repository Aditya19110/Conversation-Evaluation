# Web Deployment Guide

This guide covers multiple options to deploy your Conversation Evaluation Benchmark to the web.

## Option 1: Railway (Recommended - Easy & Free)

Railway is perfect for this project as it supports Docker and provides free hosting.

### Step-by-Step Railway Deployment:

1. **Prepare your project**
   - Push your code to GitHub
   - Make sure all files are committed

2. **Sign up for Railway**
   - Go to https://railway.app
   - Sign up with your GitHub account

3. **Deploy**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will automatically detect docker-compose.yml

4. **Configure services**
   - Railway will create services for each container
   - Set environment variables if needed

5. **Access your app**
   - Railway provides a public URL
   - Your API will be available at the provided URL

### Railway Configuration Files:

**railway.toml** (create this file):
```toml
[build]
builder = "dockerfile"
buildCommand = "docker-compose build"

[deploy]
startCommand = "docker-compose up"
restartPolicyType = "on-failure"
restartPolicyMaxRetries = 10

[env]
PORT = "8000"
```

## Option 2: Render (Free Tier Available)

Render provides excellent Docker support and free SSL certificates.

### Step-by-Step Render Deployment:

1. **Create Render account**
   - Go to https://render.com
   - Sign up with GitHub

2. **Create Web Service**
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Choose your branch (main)

3. **Configure service**
   - Name: `conversation-evaluation-api`
   - Environment: `Docker`
   - Build Command: `docker build -f docker/api/Dockerfile -t api .`
   - Start Command: `python -m uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`

4. **Add database**
   - Create PostgreSQL database on Render
   - Copy connection URL to environment variables

5. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy automatically

## Option 3: Heroku (Paid but Reliable)

### Step-by-Step Heroku Deployment:

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # Windows
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login and create app**
   ```bash
   heroku login
   heroku create your-conversation-eval-app
   ```

3. **Add PostgreSQL addon**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

4. **Configure for Heroku**
   - Create `Procfile`
   - Set environment variables

5. **Deploy**
   ```bash
   git push heroku main
   ```

## Option 4: AWS (Advanced - Most Scalable)

For production-grade deployment with full control.

### AWS Deployment Steps:

1. **Setup AWS ECS with Fargate**
2. **Create RDS PostgreSQL instance**
3. **Setup Application Load Balancer**
4. **Configure Auto Scaling**
5. **Setup CloudWatch monitoring**

## Option 5: DigitalOcean App Platform

Simple and cost-effective for medium-scale applications.

### DigitalOcean Steps:

1. **Create DigitalOcean account**
2. **Use App Platform**
3. **Connect GitHub repository**
4. **Configure build settings**
5. **Add managed database**

---

## Quick Start Recommendation

**For beginners**: Use Railway - it's the easiest and provides a good free tier.

**For production**: Use Render or AWS depending on your scale needs.

## Next Steps After Deployment

1. **Custom Domain**: Point your domain to the deployed URL
2. **SSL Certificate**: Most platforms provide this automatically
3. **Monitoring**: Set up health checks and monitoring
4. **Scaling**: Configure auto-scaling based on traffic