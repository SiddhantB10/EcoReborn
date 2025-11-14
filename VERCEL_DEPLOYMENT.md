# Vercel Deployment Guide for EcoReborn

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **MongoDB Atlas**: Active cluster with connection string
3. **GitHub Repository**: Code pushed to GitHub (SiddhantB10/EcoReborn)

## Quick Deployment Steps

### Step 1: Install Vercel CLI (Optional)

```bash
npm install -g vercel
```

### Step 2: Deploy via Vercel Dashboard (Recommended)

1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click **"Add New Project"**
3. Select **"Import Git Repository"**
4. Choose your GitHub repository: `SiddhantB10/EcoReborn`
5. Configure the project:
   - **Framework Preset**: Other
   - **Root Directory**: `./` (leave as default)
   - **Build Command**: (leave empty)
   - **Output Directory**: (leave empty)

### Step 3: Configure Environment Variables

Add the following environment variables in Vercel dashboard:

#### Required Variables:

```
SECRET_KEY=your-secret-key-here-make-it-long-and-random
MONGODB_URI=mongodb+srv://db_user:db_pass@ecoreborndb.yag1cpa.mongodb.net/
MONGODB_DB_NAME=ecoreborn
FLASK_ENV=production
```

#### Optional Variables (Email):

```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password
SMTP_FROM=noreply@ecoreborn.com
ADMIN_EMAIL=admin@ecoreborn.com
```

#### Optional Variables (Advanced):

```
APP_URL=https://your-app.vercel.app
MAX_FILE_SIZE=2097152
UPLOAD_FOLDER=./uploads
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
PERMANENT_SESSION_LIFETIME=3600
```

### Step 4: Deploy

Click **"Deploy"** and wait for the build to complete (usually 1-2 minutes).

### Step 5: Initialize Database

After first deployment:

1. Go to your Vercel project settings
2. Navigate to the **"Deployments"** tab
3. Click on your latest deployment
4. You'll need to initialize the database manually using MongoDB Atlas:
   - Connect to your MongoDB Atlas cluster
   - Use MongoDB Compass or the web interface
   - Run the collections creation manually or use a local Python script

**Alternative**: Run `init_db.py` locally pointing to production MongoDB:

```bash
# Set production MongoDB URI temporarily
set MONGODB_URI=mongodb+srv://db_user:db_pass@ecoreborndb.yag1cpa.mongodb.net/
python init_db.py
```

### Step 6: Verify Deployment

1. Visit your Vercel deployment URL (e.g., `https://ecoreborn.vercel.app`)
2. Check that:
   - Homepage loads correctly
   - Static files (CSS, images) are working
   - Navigation works
   - Forms submit correctly
   - Login/signup functionality works

## Deployment Files

### Required Files:

- ✅ `vercel.json` - Vercel configuration
- ✅ `api/index.py` - Serverless entry point
- ✅ `requirements.txt` - Python dependencies
- ✅ `.vercelignore` - Files to exclude from deployment

### Files Removed (Render-specific):

- ❌ `render.yaml` - Not needed for Vercel
- ❌ `Procfile` - Not needed for Vercel
- ❌ `build.sh` - Not needed for Vercel

## How It Works

### Vercel + Flask Architecture:

1. **Serverless Functions**: Vercel runs Flask as a serverless function
2. **Cold Starts**: First request may be slower (cold start)
3. **Request Handling**: Each request spins up a function instance
4. **Static Files**: Served directly from `/static` directory
5. **No Persistent Storage**: Use MongoDB Atlas for all data

### Important Differences from Render:

- **No Always-On Server**: Functions spin down after requests
- **No Background Tasks**: Can't run scheduled jobs (use external cron services)
- **Cold Starts**: Initial requests may be slower
- **File Uploads**: Temporary only, use cloud storage (S3, Cloudinary) for production
- **Logs**: Available in Vercel dashboard under "Logs" tab

## Troubleshooting

### Issue: 404 Not Found

**Solution**: Check `vercel.json` routes configuration is correct.

### Issue: Module Not Found

**Solution**: Ensure all dependencies are in `requirements.txt` and deployment succeeded.

### Issue: Database Connection Failed

**Solution**: 
- Verify MongoDB Atlas IP whitelist includes `0.0.0.0/0` (all IPs)
- Check MONGODB_URI environment variable is set correctly
- Ensure database user has read/write permissions

### Issue: Static Files Not Loading

**Solution**: 
- Verify files are in `/static` directory
- Check `.vercelignore` doesn't exclude static files
- Clear browser cache

### Issue: Forms Not Working (CSRF Errors)

**Solution**: 
- Ensure SECRET_KEY is set in environment variables
- Check APP_URL matches your Vercel domain
- Verify SESSION_COOKIE_SECURE is set to `True` for HTTPS

## Automatic Deployments

Vercel automatically deploys when you push to GitHub:

- **Production**: Pushes to `main` branch → Production deployment
- **Preview**: Pushes to other branches → Preview deployment
- **Pull Requests**: Automatic preview deployments for PRs

## Custom Domain (Optional)

1. Go to Project Settings → Domains
2. Add your custom domain
3. Configure DNS records as shown
4. Update `APP_URL` environment variable

## Monitoring

- **Logs**: Vercel Dashboard → Your Project → Logs
- **Analytics**: Vercel Dashboard → Your Project → Analytics
- **Performance**: Built-in Web Vitals tracking

## Security Checklist

- ✅ SECRET_KEY is strong and random
- ✅ FLASK_ENV=production
- ✅ SESSION_COOKIE_SECURE=True
- ✅ MongoDB Atlas IP whitelist configured
- ✅ Database user has minimal required permissions
- ✅ SMTP credentials secured (use app passwords, not main password)

## Cost

- **Hobby Plan**: Free tier includes:
  - 100GB bandwidth/month
  - 100 hours serverless function execution
  - Automatic HTTPS
  - Preview deployments

- **Pro Plan**: $20/month for higher limits

## Support

- Vercel Docs: [vercel.com/docs](https://vercel.com/docs)
- MongoDB Atlas: [docs.atlas.mongodb.com](https://docs.atlas.mongodb.com)
- Flask on Vercel: [vercel.com/guides/flask](https://vercel.com/guides/flask)

## Next Steps

1. Deploy to Vercel using the dashboard
2. Configure environment variables
3. Initialize database collections
4. Test all functionality
5. Set up custom domain (optional)
6. Monitor logs for any issues

---

**Note**: For file uploads in production, consider using a cloud storage service like AWS S3, Cloudinary, or Vercel Blob Storage, as Vercel's filesystem is read-only and temporary.
