# Full-Stack Deployment Guide: Frontend + API

Deploy your complete conversation evaluation system with React frontend on Netlify and Python API on Render.

## Architecture
```
React Frontend (Netlify) ← → Python API (Render) ← → PostgreSQL (Render)
```

## Part 1: Deploy API Backend on Render

### Step 1: Deploy API
1. **Go to Render**: https://render.com → Login with GitHub
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
   - `CORS_ORIGINS=["https://your-frontend.netlify.app"]`
5. **Deploy**: Takes 3-5 minutes

**Your API will be live at**: `https://conversation-eval-api.onrender.com`

### Step 2: Add Database (Optional)
1. **Create PostgreSQL**: "New +" → "PostgreSQL" → Name: `conversation-eval-db`
2. **Connect**: Add `DATABASE_URL` environment variable to your API service

## Part 2: Deploy Frontend on Netlify

### Step 1: Prepare Frontend
First, let's create a simple React frontend for your API:

```bash
# Create React app in your project
cd src/ui
npx create-react-app . --template typescript
```

### Step 2: Configure API Endpoint
Create `src/ui/src/config.ts`:
```typescript
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
```

### Step 3: Build and Deploy
**Option A: Drag & Drop (Quick)**
```bash
cd src/ui
npm install
npm run build
```
- Go to https://netlify.com
- Drag the `build` folder to deploy

**Option B: Git Integration (Recommended)**
1. **Netlify**: https://netlify.com → "Add new site" → "Import from Git"
2. **Build Settings**:
   - Build command: `cd src/ui && npm ci && npm run build`
   - Publish directory: `src/ui/build`
3. **Environment Variables**:
   - `REACT_APP_API_URL=https://conversation-eval-api.onrender.com`

**Your Frontend will be live at**: `https://conversation-eval.netlify.app`

## Part 3: Connect Frontend to API

### Update CORS in API
In `src/api/main.py`, update CORS settings:
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

### Example Frontend Integration
```typescript
// src/ui/src/services/api.ts
import { API_BASE_URL } from '../config';

export const evaluateConversation = async (text: string) => {
  const response = await fetch(`${API_BASE_URL}/evaluate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ conversation: text }),
  });
  return response.json();
};
```

## Complete Deployment Steps

### 1. Update Your Repository
```bash
# Add frontend configuration
echo "REACT_APP_API_URL=https://conversation-eval-api.onrender.com" > src/ui/.env.production

# Commit changes
git add .
git commit -m "Add frontend and deployment configs"
git push origin main
```

### 2. Deploy API (Render)
- Visit render.com → Create Web Service → Connect GitHub
- Configure as Docker environment
- Set environment variables
- Deploy!

### 3. Deploy Frontend (Netlify)
- Visit netlify.com → New site from Git
- Connect GitHub repository
- Configure build settings
- Deploy!

### 4. Test Everything
- **Frontend**: Visit your Netlify URL
- **API**: Visit your Render URL + `/docs`
- **Integration**: Test API calls from frontend

## URLs You'll Get

- **Frontend**: `https://conversation-eval.netlify.app`
- **API**: `https://conversation-eval-api.onrender.com`
- **API Docs**: `https://conversation-eval-api.onrender.com/docs`

## Benefits of This Setup

### Netlify (Frontend)
✅ Global CDN for fast loading  
✅ Automatic deployments on git push  
✅ Custom domains included  
✅ 100GB bandwidth free  

### Render (API)
✅ Docker support  
✅ Managed PostgreSQL  
✅ Automatic SSL  
✅ 99.9% uptime SLA  

### Cost
- **Development**: Completely FREE
- **Production**: $7/month for always-on API (optional)

## Troubleshooting

### CORS Issues
- Update `allow_origins` in your API
- Redeploy API on Render

### Build Failures
- Check Node.js version in Netlify
- Verify build commands
- Check environment variables

Your full-stack conversation evaluation system will be live with professional hosting!