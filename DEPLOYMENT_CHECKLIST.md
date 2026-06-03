# Render Deployment Checklist

## Pre-Deployment (Do Before Pushing to GitHub)

- [ ] Generate a strong SECRET_KEY:
  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```
  Save this value somewhere safe

- [ ] Verify all changes committed:
  ```bash
  git status  # Should be clean
  ```

- [ ] Push to GitHub:
  ```bash
  git add .
  git commit -m "Prepare for Render deployment"
  git push origin main
  ```

## Render Setup (Step by Step)

### 1. Create Account & Initial Setup
- [ ] Sign up at https://render.com (free)
- [ ] Connect your GitHub account
- [ ] Authorize Render to access your repositories

### 2. Create PostgreSQL Database
- [ ] In Render Dashboard, click **New +** → **PostgreSQL**
- [ ] Fill in details:
  - [ ] Name: `jobportal-db`
  - [ ] Database: `jobportal`
  - [ ] Region: Select closest to you
- [ ] Click **Create Database**
- [ ] Copy the **Internal Database URL** (looks like: `postgresql://user:password@...`)
- [ ] Save it - you'll need this in Step 3

### 3. Create Web Service
- [ ] Click **New +** → **Web Service**
- [ ] Connect GitHub repository:
  - [ ] Click "Connect" and select your repository
  - [ ] Select branch: `main`
- [ ] Configure service:
  - [ ] Name: `jobportal`
  - [ ] Environment: `Python 3`
  - [ ] Region: **Same as your database**
  - [ ] Build Command: 
    ```
    pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
    ```
  - [ ] Start Command: 
    ```
    gunicorn jobportal.wsgi
    ```

### 4. Add Environment Variables
In the Web Service settings, scroll to **Environment** section:

- [ ] `ENVIRONMENT` = `production`
- [ ] `DEBUG` = `False`
- [ ] `SECRET_KEY` = `<paste-your-generated-key>`
- [ ] `ALLOWED_HOSTS` = `<your-service-name>.onrender.com`
- [ ] `CSRF_TRUSTED_ORIGINS` = `https://<your-service-name>.onrender.com`
- [ ] `DATABASE_URL` = `<paste-internal-database-url-from-step-2>`
- [ ] `EMAIL_BACKEND` = `django.core.mail.backends.console.EmailBackend`
- [ ] `PAYMENT_TEST_MODE` = `True`

### 5. Deploy
- [ ] Click **Create Web Service**
- [ ] Render starts building automatically
- [ ] Watch the **Build** logs for progress
- [ ] Once deployed, you get a URL: `https://<name>-<random>.onrender.com`

## Post-Deployment Verification

- [ ] Visit your app URL in browser
- [ ] Check if it loads without errors
- [ ] View **Logs** if there are issues
- [ ] Create superuser:
  - [ ] In Render dashboard, click the **Shell** button
  - [ ] Run: `python manage.py createsuperuser`
  - [ ] Follow prompts
- [ ] Test admin panel: `https://your-app-url.com/admin`
- [ ] Test login with superuser credentials
- [ ] Test key features (job listings, applications, etc.)

## Optional: Connect Custom Domain

- [ ] Go to Web Service **Settings**
- [ ] Click **Custom Domains**
- [ ] Add your domain (e.g., `yourdomain.com`)
- [ ] Follow DNS instructions
- [ ] Update email configuration if needed

## Ongoing Maintenance

- [ ] Monitor Render dashboard for CPU/RAM usage
- [ ] Check logs regularly for errors
- [ ] Set up monitoring/alerts (optional)
- [ ] Plan for database backups
- [ ] Consider upgrading to paid plan if cold starts are a problem

## Troubleshooting

If deployment fails:
1. [ ] Check **Logs** in Render dashboard
2. [ ] Search for error messages
3. [ ] Verify environment variables are set correctly
4. [ ] Ensure database URL is correct
5. [ ] Check SECRET_KEY is not default value

Common issues:
- [ ] Static files not loading → Check `collectstatic` in build command
- [ ] Database errors → Verify DATABASE_URL environment variable
- [ ] 502 error → Check logs, may be build or startup issue
- [ ] Slow first request → Normal on free tier (service starting up)

---

## You're All Set! 🎉

Once verified, your Django Job Portal is live on the internet!

For help, refer to:
- `DEPLOYMENT_RENDER.md` - Detailed guide
- `RENDER_SETUP_SUMMARY.md` - Quick reference
