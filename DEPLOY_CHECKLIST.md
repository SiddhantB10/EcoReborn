# 🚀 Quick Deployment Checklist

Use this checklist before deploying to production.

## ✅ Pre-Deployment Checklist

### 1. Environment Variables
- [ ] Generate secure `SECRET_KEY` (64+ characters)
- [ ] Update `MONGODB_URI` with real credentials
- [ ] Replace `db_user` and `db_pass` in MongoDB URI
- [ ] Set `FLASK_ENV=production`
- [ ] Set correct `APP_URL` (your domain)
- [ ] Set `SESSION_COOKIE_SECURE=True`

### 2. MongoDB Atlas
- [ ] Database created
- [ ] User has read/write permissions
- [ ] IP whitelist configured (0.0.0.0/0 for cloud platforms)
- [ ] Connection string tested

### 3. Application
- [ ] All requirements in `requirements.txt`
- [ ] Database initialized (`python init_db.py`)
- [ ] Static files working locally
- [ ] All routes tested locally

### 4. Security
- [ ] `.env` file in `.gitignore`
- [ ] Strong SECRET_KEY generated
- [ ] CSRF protection enabled
- [ ] Rate limiting configured
- [ ] File upload limits set

### 5. Git Repository
- [ ] All changes committed
- [ ] Pushed to GitHub
- [ ] `.env` NOT committed (check with `git status`)

---

## 🎯 Platform-Specific

### For Render:
- [ ] `build.sh` has execute permissions
- [ ] `Procfile` present
- [ ] Environment variables added in dashboard
- [ ] Branch set to `main`

### For Vercel:
- [ ] `vercel.json` configured
- [ ] Environment variables added
- [ ] Python runtime specified

---

## 🧪 Post-Deployment Testing

After deployment, test:

- [ ] Home page loads
- [ ] Static files (CSS, images) display correctly
- [ ] User signup works
- [ ] User login works
- [ ] Dashboard accessible after login
- [ ] Contact form submits
- [ ] Logout works
- [ ] Password reset flow (if email configured)

---

## 📊 Monitoring

After deployment:

- [ ] Check application logs
- [ ] Monitor MongoDB connections
- [ ] Test from different devices
- [ ] Check response times
- [ ] Verify HTTPS is working

---

## 🐛 If Something Goes Wrong

1. Check deployment logs in platform dashboard
2. Verify environment variables are set correctly
3. Test MongoDB connection from logs
4. Check that IP is whitelisted in MongoDB Atlas
5. Review error messages in application logs

---

## 📞 Need Help?

Refer to:
- [DEPLOYMENT.md](DEPLOYMENT.md) - Full deployment guide
- [START_HERE.md](START_HERE.md) - Getting started guide
- Platform documentation (Render/Vercel)

---

**Good luck with your deployment! 🎉**
