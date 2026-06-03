# Deployment Guide: Django Job Portal on Render

## Prerequisites
- GitHub account with your code pushed to a repository
- Render account (create at render.com)

## Step-by-Step Deployment Instructions

### Step 1: Prepare Your Repository
```bash
# Make sure all files are committed
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### Step 2: Create PostgreSQL Database on Render

1. Go to [https://dashboard.render.com](https://dashboard.render.com)
2. Click **New +** button → **PostgreSQL**
3. Fill in the details:
   - **Name**: `jobportal-db` (or your choice)
   - **Database**: `jobportal`
   - **User**: Leave as default
   - **Region**: Choose closest to you
   - **PostgreSQL Version**: 15
4. Click **Create Database**
5. Copy the **Internal Database URL** (you'll need this)

### Step 3: Deploy Web Service on Render

1. Click **New +** button → **Web Service**
2. Connect your GitHub repository:
   - Click "Connect" for your GitHub repo
   - Select the repository containing your Django app
3. Fill in the configuration:
   - **Name**: `jobportal` (or your choice)
   - **Environment**: `Python 3`
   - **Region**: Same as database
   - **Branch**: `main` (or your default branch)
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command**: `gunicorn jobportal.wsgi`

### Step 4: Add Environment Variables

In the Render dashboard for your web service:

1. Scroll down to **Environment**
2. Add each variable (click **Add Environment Variable**):

```
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=<generate-strong-secret-key>
ALLOWED_HOSTS=<your-service-name>.onrender.com
CSRF_TRUSTED_ORIGINS=https://<your-service-name>.onrender.com,https://yourdomain.com
DATABASE_URL=<paste-internal-database-url-from-step-2>
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
PAYMENT_TEST_MODE=True
```

**To generate SECRET_KEY**, run in terminal:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 5: Create Free Plan Resources (Optional)

- Render free tier includes:
  - Web Service: 0.5 CPU, 512 MB RAM
  - PostgreSQL: Included with free tier
  - Caveat: Services spin down after 15 minutes of inactivity

To upgrade to paid plans for always-on service:
1. Go to instance settings
2. Select paid plan (starts at $4-7/month)

### Step 6: Deploy

1. Click **Create Web Service**
2. Render will automatically deploy your app
3. Watch the **Deploy** logs for progress
4. Once complete, you'll get a URL like: `https://jobportal-xxxx.onrender.com`

### Step 7: Post-Deployment Verification

1. Visit your app URL
2. Check logs for any errors: **Dashboard** → **Your Service** → **Logs**
3. Run migrations (if not automatic):
   ```bash
   # In Render dashboard, click "Shell" and run:
   python manage.py migrate
   ```
4. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

### Step 8: Connect Custom Domain (Optional)

1. Go to your service settings
2. Click **Settings** → **Custom Domains**
3. Add your domain and follow DNS instructions

---

## Troubleshooting

### Static Files Not Loading
- Ensure `STATIC_ROOT` and `collectstatic` command is in build step
- WhiteNoise is configured in settings.py

### Database Connection Issues
- Verify DATABASE_URL is set correctly
- Check database is running in Render dashboard

### Application Errors
1. Check logs: Dashboard → Your service → Logs
2. Enable DEBUG temporarily (set DEBUG=True) to see detailed errors
3. Check email/SMTP configuration if email features fail

### Cold Starts (Free Tier)
- Free tier services spin down after 15 minutes
- First request may take 30+ seconds to start
- Upgrade to paid plan for always-on service

---

## Important Notes

1. **Production SECRET_KEY**: Never use the default. Generate a strong one.
2. **Email Configuration**: Console backend is for testing. For production, use SendGrid, Gmail, or similar.
3. **Media Files**: Render doesn't persist files in the working directory. For user uploads:
   - Use AWS S3 or similar cloud storage
   - Or use Render's persistent disks (paid feature)
4. **Database Backups**: Set up automated backups in Render dashboard
5. **Monitoring**: Monitor CPU/RAM usage in Render dashboard to ensure adequate resources

---

## Future Enhancements

1. **Set up CI/CD**: Auto-deploy on every push
2. **Configure error monitoring**: Use Sentry
3. **Set up logging**: Use cloud logging service
4. **Scale database**: Upgrade PostgreSQL as needed
5. **Optimize for production**: Add caching, CDN, etc.

---

## Support

- Render Docs: https://render.com/docs
- Django Deployment: https://docs.djangoproject.com/en/stable/howto/deployment/
