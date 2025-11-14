# Vercel Deployment Checklist

## ✅ Pre-Deployment Verification

### Local Setup
- [x] All Vercel configuration files created
  - [x] `vercel.json` - Vercel configuration
  - [x] `api/index.py` - Serverless entry point
  - [x] `.vercelignore` - Exclusion list
- [x] Requirements file verified (`requirements.txt`)
- [x] Flask app structure verified
- [x] Static files present
- [x] Templates present
- [x] Verification script passed (7/7 checks)

### GitHub Repository
- [ ] All changes committed to Git
- [ ] Changes pushed to GitHub (main branch)
- [ ] Repository is public or accessible to Vercel

## 🚀 Deployment Steps

### 1. Vercel Dashboard Setup
- [ ] Sign in to [vercel.com](https://vercel.com)
- [ ] Click "Add New Project"
- [ ] Import Git repository: `SiddhantB10/EcoReborn`
- [ ] Select repository and click "Import"

### 2. Configure Project Settings
- [ ] Framework Preset: **Other**
- [ ] Root Directory: `./` (default)
- [ ] Build Command: (leave empty)
- [ ] Output Directory: (leave empty)
- [ ] Install Command: `pip install -r requirements.txt` (auto-detected)

### 3. Environment Variables (Required)

#### Essential Variables (Must Set):
```
SECRET_KEY=<generate-random-64-char-string>
MONGODB_URI=mongodb+srv://db_user:db_pass@ecoreborndb.yag1cpa.mongodb.net/
MONGODB_DB_NAME=ecoreborn
FLASK_ENV=production
```

#### Optional Email Variables:
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password
SMTP_FROM=noreply@ecoreborn.com
ADMIN_EMAIL=admin@ecoreborn.com
```

#### Optional Advanced Variables:
```
APP_URL=https://your-project.vercel.app
MAX_FILE_SIZE=2097152
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
```

### 4. Deploy
- [ ] Click "Deploy" button
- [ ] Wait for build to complete (~1-2 minutes)
- [ ] Check for any build errors in logs

## ✅ Post-Deployment Verification

### 5. Test Deployment
- [ ] Visit Vercel deployment URL (e.g., `https://ecoreborn.vercel.app`)
- [ ] Homepage loads correctly
- [ ] Static files (CSS, images) load correctly
- [ ] Navigation works
- [ ] Login page loads
- [ ] Signup page loads
- [ ] Services page loads
- [ ] Contact page loads

### 6. Test Functionality
- [ ] Test signup (create new account)
- [ ] Test login (use created account)
- [ ] Test logout
- [ ] Test password reset request
- [ ] Test contact form submission
- [ ] Test newsletter subscription
- [ ] Test service request submission
- [ ] Test dashboard access (if applicable)

### 7. Database Initialization
- [ ] Connect to MongoDB Atlas dashboard
- [ ] Verify database `ecoreborn` exists
- [ ] Check if collections exist (6 total):
  - [ ] users
  - [ ] password_reset_tokens
  - [ ] contact_messages
  - [ ] service_requests
  - [ ] newsletter_subscribers
  - [ ] login_attempts
- [ ] If collections missing, run `init_db.py` locally with production MongoDB URI

### 8. Monitor First Hour
- [ ] Check Vercel logs for errors
- [ ] Test all major user flows
- [ ] Verify MongoDB connections in Atlas dashboard
- [ ] Check function execution times (cold start vs warm)

## 🔧 Troubleshooting

### If Deployment Fails:
1. Check Vercel build logs for specific errors
2. Verify all environment variables are set correctly
3. Ensure `requirements.txt` has all dependencies
4. Check Python version compatibility

### If Site Loads but Crashes:
1. Check Vercel Function logs (Dashboard → Your Project → Logs)
2. Verify MongoDB connection string and credentials
3. Check MongoDB Atlas IP whitelist includes `0.0.0.0/0`
4. Verify SECRET_KEY is set in environment variables

### If Forms Don't Work:
1. Verify SECRET_KEY is set (required for CSRF protection)
2. Check APP_URL matches your Vercel domain
3. Ensure cookies are enabled in browser
4. Check SESSION_COOKIE_SECURE=True for HTTPS sites

### If Static Files Don't Load:
1. Check browser console for 404 errors
2. Verify files are in `/static` directory
3. Check `.vercelignore` doesn't exclude static files
4. Clear browser cache and hard reload (Ctrl+Shift+R)

## 📊 Monitoring & Maintenance

### Regular Checks:
- [ ] Monitor Vercel dashboard for errors
- [ ] Check MongoDB Atlas for unusual activity
- [ ] Review function execution times
- [ ] Monitor bandwidth usage

### Monthly:
- [ ] Review and rotate SECRET_KEY if needed
- [ ] Update dependencies in `requirements.txt`
- [ ] Check for Python/Flask security updates
- [ ] Review MongoDB Atlas storage usage

## 🎯 Success Criteria

✅ Deployment is successful when:
1. All pages load without errors
2. User registration and login work
3. Forms submit successfully
4. Database operations succeed
5. No errors in Vercel logs
6. Response times are acceptable (<2s cold start, <200ms warm)

## 📚 Reference Documents

- **Full Guide**: `VERCEL_DEPLOYMENT.md`
- **Verification**: Run `python verify_vercel.py`
- **Environment**: See `.env.example` for all variables

## 🆘 Support Resources

- Vercel Docs: https://vercel.com/docs
- Flask on Vercel: https://vercel.com/guides/flask
- MongoDB Atlas: https://docs.atlas.mongodb.com
- Project Issues: https://github.com/SiddhantB10/EcoReborn/issues

---

**Current Status**: ✅ All pre-deployment checks passed
**Next Step**: Push to GitHub and deploy via Vercel dashboard
