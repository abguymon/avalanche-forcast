# Railway Deployment Guide for Avalanche Forecast

## 🚀 Deploy to Railway (Free Tier)

### Step 1: Prepare Your Repository
```bash
# Make sure all files are committed
git add .
git commit -m "Ready for Railway deployment"
git push origin main
```

### Step 2: Deploy to Railway
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your `avalanche-forcast` repository
5. Railway will auto-detect Docker and deploy!

### Step 3: Configure Environment
Railway will automatically:
- Build your Docker container
- Deploy your app
- Provide a public URL
- Set up SSL certificate

### Step 4: Access Your App
- Railway provides a URL like: `https://avalanche-forcast-production.up.railway.app`
- Your app will be live and accessible worldwide!

## 🔧 Alternative: Render Deployment

### Step 1: Prepare for Render
```bash
# Create render.yaml for Render
cat > render.yaml << 'EOF'
services:
  - type: web
    name: avalanche-forecast
    env: docker
    dockerfilePath: ./Dockerfile
    plan: free
    healthCheckPath: /api/data
EOF
```

### Step 2: Deploy to Render
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New" → "Web Service"
4. Connect your GitHub repo
5. Select "Docker" as environment
6. Deploy!

## 💰 Cost Comparison

| Service | Free Tier | Best For |
|---------|-----------|----------|
| **Railway** | $5 credit/month | Docker apps, easy setup |
| **Render** | 750 hours/month | Docker, sleeps after inactivity |
| **Fly.io** | 3 shared VMs | Global deployment |
| **Heroku** | $5/month Eco | Traditional Python |

## 🎯 Recommended: Railway

Railway is perfect because:
- ✅ **Free tier** with generous limits
- ✅ **Docker support** (your setup works directly)
- ✅ **Automatic deployments** from GitHub
- ✅ **Custom domains** included
- ✅ **No configuration needed**

Your avalanche forecast app will be live in minutes! 🏔️
