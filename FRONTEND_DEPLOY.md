# Frontend Deployment Guide - Netlify

Your API is already live! Now let's deploy the React frontend to Netlify and connect it to your working API.

## Prerequisites
- Your API is deployed and working on Render
- GitHub account
- Basic React knowledge

## Step 1: Create React Frontend

Since you have the API working, let's create a simple React frontend:

```bash
# In your project root
cd src/ui
npx create-react-app . --template typescript
npm install axios chart.js react-chartjs-2 @mui/material @emotion/react @emotion/styled
```

## Step 2: Create Frontend Components

### API Configuration
Create `src/ui/src/config.ts`:
```typescript
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
```

### API Service
Create `src/ui/src/services/api.ts`:
```typescript
import axios from 'axios';
import { API_BASE_URL } from '../config';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface EvaluationRequest {
  conversation: string;
  context?: string;
  facets?: string[];
}

export interface EvaluationResult {
  overall_score: number;
  confidence: number;
  facet_scores: Record<string, number>;
  reasoning: string;
}

export const evaluateConversation = async (data: EvaluationRequest): Promise<EvaluationResult> => {
  const response = await api.post('/evaluate', data);
  return response.data;
};

export const getHealthStatus = async () => {
  const response = await api.get('/health');
  return response.data;
};

export const getFacets = async () => {
  const response = await api.get('/facets');
  return response.data;
};
```

### Main App Component
Update `src/ui/src/App.tsx`:
```typescript
import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  TextField,
  Button,
  Paper,
  Grid,
  CircularProgress,
  Alert,
  Box
} from '@mui/material';
import { evaluateConversation, getHealthStatus, EvaluationResult } from './services/api';
import './App.css';

function App() {
  const [conversation, setConversation] = useState('');
  const [result, setResult] = useState<EvaluationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [apiStatus, setApiStatus] = useState<string>('checking...');

  useEffect(() => {
    // Check API health on component mount
    checkApiHealth();
  }, []);

  const checkApiHealth = async () => {
    try {
      await getHealthStatus();
      setApiStatus('connected');
    } catch (err) {
      setApiStatus('disconnected');
      setError('API is not accessible. Please check your API URL.');
    }
  };

  const handleEvaluate = async () => {
    if (!conversation.trim()) {
      setError('Please enter a conversation to evaluate');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const evaluationResult = await evaluateConversation({
        conversation: conversation.trim(),
        context: 'Web UI evaluation'
      });
      setResult(evaluationResult);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to evaluate conversation');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h3" component="h1" gutterBottom align="center">
        Conversation Evaluation Benchmark
      </Typography>
      
      <Box mb={2}>
        <Alert severity={apiStatus === 'connected' ? 'success' : 'error'}>
          API Status: {apiStatus}
        </Alert>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
              Enter Conversation
            </Typography>
            <TextField
              fullWidth
              multiline
              rows={8}
              variant="outlined"
              placeholder="Enter the conversation text you want to evaluate..."
              value={conversation}
              onChange={(e) => setConversation(e.target.value)}
              sx={{ mb: 2 }}
            />
            <Button
              variant="contained"
              color="primary"
              onClick={handleEvaluate}
              disabled={loading || apiStatus !== 'connected'}
              fullWidth
              size="large"
            >
              {loading ? <CircularProgress size={24} /> : 'Evaluate Conversation'}
            </Button>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
              Evaluation Results
            </Typography>
            
            {error && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            )}

            {result && (
              <Box>
                <Typography variant="h6" gutterBottom>
                  Overall Score: {result.overall_score.toFixed(2)}/5
                </Typography>
                <Typography variant="body1" gutterBottom>
                  Confidence: {(result.confidence * 100).toFixed(1)}%
                </Typography>
                
                <Typography variant="h6" sx={{ mt: 2, mb: 1 }}>
                  Facet Scores:
                </Typography>
                {Object.entries(result.facet_scores).map(([facet, score]) => (
                  <Typography key={facet} variant="body2">
                    {facet}: {score.toFixed(2)}/5
                  </Typography>
                ))}
                
                {result.reasoning && (
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="h6" gutterBottom>
                      Reasoning:
                    </Typography>
                    <Typography variant="body2" sx={{ fontStyle: 'italic' }}>
                      {result.reasoning}
                    </Typography>
                  </Box>
                )}
              </Box>
            )}

            {!result && !error && !loading && (
              <Typography variant="body1" color="text.secondary">
                Enter a conversation and click "Evaluate" to see results here.
              </Typography>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}

export default App;
```

### Package.json Updates
Update `src/ui/package.json` to include the new dependencies:
```json
{
  "name": "conversation-evaluation-ui",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "@emotion/react": "^11.11.1",
    "@emotion/styled": "^11.11.0",
    "@mui/material": "^5.14.20",
    "@testing-library/jest-dom": "^5.17.0",
    "@testing-library/react": "^13.4.0",
    "@testing-library/user-event": "^13.5.0",
    "@types/jest": "^27.5.2",
    "@types/node": "^16.18.68",
    "@types/react": "^18.2.42",
    "@types/react-dom": "^18.2.17",
    "axios": "^1.6.2",
    "chart.js": "^4.4.0",
    "react": "^18.2.0",
    "react-chartjs-2": "^5.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "typescript": "^4.9.5",
    "web-vitals": "^2.1.4"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
```

## Step 3: Test Frontend Locally

```bash
cd src/ui
npm install
npm start
```

Visit `http://localhost:3000` and test with your API.

## Step 4: Deploy to Netlify

### Option A: Drag & Drop (Quick)
```bash
# Build the app
cd src/ui
npm run build

# Go to netlify.com and drag the 'build' folder
```

### Option B: Git Integration (Recommended)

1. **Commit your changes**:
```bash
git add .
git commit -m "Add React frontend"
git push origin main
```

2. **Deploy on Netlify**:
   - Go to https://netlify.com
   - Click "Add new site" → "Import from Git"
   - Connect your GitHub account
   - Select your repository

3. **Configure Build Settings**:
   - **Build command**: `cd src/ui && npm ci && npm run build`
   - **Publish directory**: `src/ui/build`
   - **Base directory**: Leave empty

4. **Environment Variables**:
   - Click "Site settings" → "Environment variables"
   - Add: `REACT_APP_API_URL = https://your-api.onrender.com`
   - Replace with your actual Render API URL

5. **Deploy**:
   - Click "Deploy site"
   - Wait 2-3 minutes for build

## Step 5: Update API CORS Settings

Your API needs to allow requests from Netlify. Update your API's CORS settings:

In `src/api/main.py`, find the CORS middleware and add your Netlify URL:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-app-name.netlify.app",  # Replace with your actual Netlify URL
        "http://localhost:3000",  # For local development
        "*"  # Remove this in production for security
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Redeploy your API on Render after this change.

## Step 6: Test Your Live Frontend

1. **Get your Netlify URL** (something like `https://amazing-cupcake-123456.netlify.app`)
2. **Visit your frontend**
3. **Test the connection** - you should see "API Status: connected"
4. **Test evaluation** - enter some text and click "Evaluate Conversation"

## Step 7: Custom Domain (Optional)

1. **Buy a domain** (Namecheap, GoDaddy, etc.)
2. **In Netlify**:
   - Site settings → Domain management
   - Add custom domain
3. **Update DNS**:
   - Add CNAME record pointing to Netlify

## Troubleshooting

### CORS Errors
- Update `allow_origins` in your API
- Redeploy API on Render
- Check browser console for specific errors

### Build Failures
- Check Node.js version (use Node 18)
- Verify all dependencies are installed
- Check build logs in Netlify

### API Connection Issues
- Verify your `REACT_APP_API_URL` environment variable
- Test API health endpoint directly
- Check network tab in browser developer tools

## Final URLs

After deployment, you'll have:
- **Frontend**: `https://your-app.netlify.app`
- **API**: `https://your-api.onrender.com` (already working)
- **API Docs**: `https://your-api.onrender.com/docs`

Your complete conversation evaluation system is now live with a professional web interface!