# Complete Deployment: Render + Netlify

Deploy your full-stack conversation evaluation system using Render for the API and Netlify for the frontend.

## Architecture Overview

```
Frontend (Netlify) ← → API Backend (Render) ← → Database (Render PostgreSQL)
```

## Part 1: Deploy API on Render

### Step 1: Prepare API for Deployment

1. **Update API configuration** (if needed):
   ```python
   # In src/api/main.py, ensure CORS allows your Netlify domain
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://your-app.netlify.app", "http://localhost:3000"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

2. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

### Step 2: Deploy API on Render

1. **Go to Render**: https://render.com → Sign up with GitHub
2. **Create Web Service**: 
   - Click "New +" → "Web Service"
   - Connect your repository
3. **Configure**:
   - Name: `conversation-eval-api`
   - Environment: `Docker`  
   - Branch: `main`
4. **Environment Variables**:
   - `PORT=8000`
   - `ENVIRONMENT=production`
5. **Deploy**: Click "Create Web Service"

You'll get a URL like: `https://conversation-eval-api.onrender.com`

### Step 3: Add Database (Optional)

1. **Create PostgreSQL**:
   - Click "New +" → "PostgreSQL"
   - Name: `conversation-eval-db`
2. **Connect to API**:
   - Add environment variable `DATABASE_URL`
   - Use the Internal Database URL

## Part 2: Deploy Frontend on Netlify

### Step 1: Prepare Frontend

1. **Update API endpoint in React app**:
   ```javascript
   // In src/ui/src/config.js (create this file)
   export const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://conversation-eval-api.onrender.com';
   ```

2. **Update your React components** to use this config:
   ```javascript
   import { API_BASE_URL } from './config';
   
   // Use API_BASE_URL in your fetch calls
   fetch(`${API_BASE_URL}/evaluate`, {...})
   ```

### Step 2: Deploy on Netlify

**Option A: Drag & Drop (Easiest)**
1. Build your React app:
   ```bash
   cd src/ui
   npm install
   npm run build
   ```
2. Go to https://netlify.com
3. Drag the `build` folder to the deploy area

**Option B: Git Integration (Recommended)**
1. Go to https://netlify.com → "Add new site" → "Import from Git"
2. Connect your GitHub repository
3. Configure build settings:
   - Build command: `cd src/ui && npm ci && npm run build`
   - Publish directory: `src/ui/build`
4. Environment variables:
   - `REACT_APP_API_URL=https://conversation-eval-api.onrender.com`

## Part 3: Test Your Deployment

### Test API (Render)
- Health check: `https://your-api.onrender.com/health`
- API docs: `https://your-api.onrender.com/docs`
- Test endpoint: `https://your-api.onrender.com/`

### Test Frontend (Netlify)
- Visit your Netlify URL: `https://your-app.netlify.app`
- Test API communication through the UI
- Check browser console for any CORS errors

## Part 4: Custom Domains (Optional)

### For API (Render)
1. Go to your service → Settings → Custom Domains
2. Add your API domain (e.g., `api.yourdomain.com`)
3. Update DNS: CNAME record pointing to Render

### For Frontend (Netlify)
1. Site Settings → Domain Management → Add custom domain
2. Add your domain (e.g., `yourdomain.com`)
3. Update DNS: CNAME record pointing to Netlify

## Troubleshooting

### Common Issues

1. **CORS Errors**:
   - Update CORS origins in your API to include Netlify URL
   - Redeploy API on Render

2. **API Not Responding**:
   - Check Render logs
   - Verify environment variables
   - Test API directly

3. **Build Failures**:
   - Check Node.js version compatibility
   - Verify build commands
   - Check environment variables

### Monitoring

- **Render**: Built-in metrics and logs
- **Netlify**: Analytics and deploy logs
- **Uptime**: Use services like UptimeRobot

## Cost Breakdown

### Free Tier Limits
- **Render**: 512MB RAM, sleeps after 15 min inactivity
- **Netlify**: 100GB bandwidth, 300 build minutes/month

### Paid Plans (if needed)
- **Render**: $7/month for always-on service
- **Netlify**: $19/month for Pro features

Your full-stack conversation evaluation system is now live with professional hosting!