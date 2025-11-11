# 🚀 Deployment Guide for EcoReborn

This guide covers deployment to **Render** - the recommended platform for Flask applications.

**Live App:** https://ecoreborn.onrender.com

---

## 📋 Prerequisites

Before deploying, ensure you have:

1. ✅ MongoDB Atlas account with database set up
2. ✅ GitHub repository pushed (already done!)
3. ✅ All environment variables ready

---

## 🎨 Deploy to Render

Render provides excellent support for Python web applications with automatic deployments from GitHub.

### Step 1: Create Render Account

1. Go to [Render.com](https://render.com)
2. Sign up with your GitHub account

### Step 2: Create New Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `SiddhantB10/EcoReborn`
3. Configure the service:

   **Basic Settings:**
   - **Name**: `ecoreborn` (or your preferred name)
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Runtime**: `Python 3`
   
   **Build & Deploy:**
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn app:app`

### Step 3: Set Environment Variables

In the Render dashboard, add these environment variables:

```bash
# Required
SECRET_KEY=<generate-a-secure-random-key>
MONGODB_URI=mongodb+srv://db_user:db_pass@ecoreborndb.yag1cpa.mongodb.net/ecoreborn?retryWrites=true&w=majority
MONGODB_DB_NAME=ecoreborn
FLASK_ENV=production
APP_URL=https://ecoreborn.onrender.com

# Session Configuration
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
PERMANENT_SESSION_LIFETIME=3600

# Optional: Email Configuration
SMTP_HOST=your-smtp-host
SMTP_PORT=587
SMTP_USER=your-email@example.com
SMTP_PASS=your-email-password
SMTP_FROM=noreply@ecoreborn.com
ADMIN_EMAIL=admin@ecoreborn.com

# Upload Configuration
UPLOAD_FOLDER=./uploads
MAX_FILE_SIZE=2097152

# Rate Limiting
RATELIMIT_STORAGE_URL=memory://
```

**Generate SECRET_KEY:**
```python
python -c "import secrets; print(secrets.token_hex(32))"
```

### Step 4: Deploy

1. Click **"Create Web Service"**
2. Render will automatically deploy your application
3. Wait for the build to complete (usually 2-5 minutes)
4. Your app will be live at: **https://ecoreborn.onrender.com**

### Step 5: Initialize Database

After first deployment:
1. Go to your Render dashboard
2. Open the **Shell** tab
3. Run: `python init_db.py`

---

##  Security Checklist

Before going live, ensure:

- ✅ Change `SECRET_KEY` to a strong random value
- ✅ Set `FLASK_ENV=production`
- ✅ Update MongoDB credentials (replace `db_user` and `db_pass`)
- ✅ Whitelist deployment server IP in MongoDB Atlas
- ✅ Set `SESSION_COOKIE_SECURE=True` for HTTPS
- ✅ Update `APP_URL` to your actual domain
- ✅ Configure email settings for password reset (optional)

---

## 📊 MongoDB Atlas Configuration

### Whitelist IP Addresses

1. Go to MongoDB Atlas → Network Access
2. Click **"Add IP Address"**
3. Add `0.0.0.0/0` (allows all IPs - needed for Render's dynamic IPs)
4. Click **"Confirm"**

### Database User

Ensure your database user has **Read and Write** permissions:
1. MongoDB Atlas → Database Access
2. Edit user → Set role to `readWrite` on `ecoreborn` database

---

## 🧪 Testing Deployment

After deployment, test these features:

1. ✅ Home page loads
2. ✅ Signup creates new user
3. ✅ Login works
4. ✅ Dashboard is accessible
5. ✅ Contact form submits
6. ✅ Forgot password sends email (if configured)
7. ✅ Static files load (CSS, images)

---

## 📝 Deployment Files

The following files support Render deployment:

- `render.yaml` - Render configuration (one-click deploy)
- `Procfile` - Process definition file
- `runtime.txt` - Python version specification (3.11.0)
- `build.sh` - Build script for dependencies
- `requirements.txt` - Python dependencies (includes gunicorn)

---

## 🐛 Troubleshooting

### Build Fails

**Issue**: Build script fails
**Solution**: Check `build.sh` has execute permissions:
```bash
chmod +x build.sh
```

### MongoDB Connection Error

**Issue**: Cannot connect to MongoDB
**Solution**: 
- Verify MongoDB URI is correct
- Check IP whitelist in MongoDB Atlas
- Ensure database user has correct permissions

### Static Files Not Loading

**Issue**: CSS/images don't load
**Solution**:
- Static files are served automatically by Render
- Check that static files are in the `static/` directory

### Environment Variables Not Working

**Issue**: App uses default values
**Solution**:
- Verify all environment variables are set in platform
- Restart the service after adding variables
- Check spelling matches `.env` file exactly

### Rate Limiting Issues

**Issue**: Rate limiter errors
**Solution**: Use `RATELIMIT_STORAGE_URL=memory://` for simple deployments

---

## 🔄 Continuous Deployment

Render supports automatic deployments:

**Automatic Deployment:**
- Automatically deploys when you push to `main` branch
- Check deployment logs in dashboard
- Takes 1-3 minutes to complete
- Zero downtime on paid plans

**Manual Deployment:**
- Can trigger manual deploy from Render dashboard
- Useful for testing without pushing to GitHub

---

## 📞 Support

If you encounter issues:

1. Check deployment logs in platform dashboard
2. Review MongoDB Atlas connection logs
3. Verify all environment variables are set correctly
4. Test locally first with production settings

---

## 🎉 Next Steps

After successful deployment:

1. ✅ Set up custom domain (optional)
2. ✅ Configure SSL certificate (automatic on Render)
3. ✅ Set up monitoring and alerts
4. ✅ Configure backups for MongoDB
5. ✅ Add analytics (optional)
6. ✅ Set up email service (SMTP configuration)

---

**Your app is live at**: https://ecoreborn.onrender.com 🚀
