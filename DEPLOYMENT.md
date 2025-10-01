# Web Deployment Guide

This guide covers multiple options to deploy your Conversation Evaluation Benchmark to the web.

## Option 1: Render (Recommended - Easy & Free)

Render is perfect for this project with excellent Docker support, free SSL, and managed databases.

### Step-by-Step Render Deployment:

1. **Prepare your project**
   - Push your code to GitHub
   - Make sure all files are committed

2. **Sign up for Render**
   - Go to https://render.com
   - Sign up with your GitHub account

3. **Create Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Choose your repository

4. **Configure service**
   - Environment: Docker
   - Build and start commands are auto-detected
   - Set environment variables

5. **Add Database (Optional)**
   - Create PostgreSQL database
   - Connect via DATABASE_URL environment variable

6. **Deploy**
   - Render builds and deploys automatically
   - Get your live URL

### Render Benefits:
- Free SSL certificates
- Automatic deployments
- Managed PostgreSQL & Redis
- 99.9% uptime SLA
- Global CDN

## Option 2: Netlify (For Frontend/Static Sites)

Perfect for deploying the React UI component as a static site.

### Step-by-Step Netlify Deployment:

1. **Build React App**
   ```bash
   cd src/ui
   npm run build
   ```

2. **Deploy to Netlify**
   - Go to https://netlify.com
   - Drag and drop your `build` folder
   - Or connect GitHub repository

3. **Configure Build Settings**
   - Build command: `cd src/ui && npm run build`
   - Publish directory: `src/ui/build`

4. **Environment Variables**
   - Add `REACT_APP_API_URL` pointing to your Render API

5. **Custom Domain**
   - Add your domain in Site Settings
   - Configure DNS records

### Netlify Benefits:
- Global CDN
- Instant deploys
- Branch previews
- Form handling
- Edge functions

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

**For API Backend**: Use Render - excellent Docker support, free tier, managed databases.

**For Frontend UI**: Use Netlify - global CDN, instant deploys, perfect for React apps.

**For Full Stack**: Deploy API on Render + UI on Netlify for best performance.

**For Production**: Use Render Pro or AWS depending on your scale needs.

## Next Steps After Deployment

1. **Custom Domain**: Point your domain to the deployed URL
2. **SSL Certificate**: Most platforms provide this automatically
3. **Monitoring**: Set up health checks and monitoring
4. **Scaling**: Configure auto-scaling based on traffic