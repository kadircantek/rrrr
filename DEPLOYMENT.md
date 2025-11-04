# Deployment Guide - Render.com (Firebase Backend)

## Architecture Overview
- **Frontend**: React + Vite (deployed on Render as Web Service)
- **Backend**: Firebase (Authentication, Realtime Database, Storage, Cloud Functions)
- **Payment**: Paddle or LemonSqueezy
- **Trading Logic**: Firebase Cloud Functions (Python or Node.js)

## Prerequisites
- GitHub repository connected to Render
- Firebase project configured and active
- Payment provider account (Paddle or LemonSqueezy)

## Step 1: Frontend Deployment (Render Web Service)

1. **Create New Web Service** in Render Dashboard
   - Connect your GitHub repository
   - Service Type: **Web Service** (not Static Site)
   - Build Command: `npm run build`
   - Start Command: `npm run preview`
   - Environment: Node 18.x or higher

2. **Environment Variables** (Add in Render Dashboard)
   ```
   # Firebase Configuration (from Firebase Console)
   VITE_FIREBASE_API_KEY=your-production-api-key
   VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
   VITE_FIREBASE_DATABASE_URL=https://your-project.firebaseio.com
   VITE_FIREBASE_PROJECT_ID=your-project-id
   VITE_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
   VITE_FIREBASE_MESSAGING_SENDER_ID=123456789
   VITE_FIREBASE_APP_ID=your-app-id
   VITE_FIREBASE_MEASUREMENT_ID=G-XXXXXXXXXX
   
   # Payment Provider (Choose one)
   VITE_PADDLE_VENDOR_ID=your-vendor-id
   VITE_LEMONSQUEEZY_STORE_ID=your-store-id
   
   # App Configuration
   VITE_APP_ENV=production
   VITE_APP_VERSION=1.0.0
   ```

3. **Deploy Settings**
   - Auto-Deploy: Yes (on main branch)
   - Health Check Path: `/` (optional)

## Step 2: Firebase Backend Configuration

### Firebase Realtime Database
Your existing Firebase project is already configured. No additional deployment needed.

### Firebase Cloud Functions (for Trading Logic)

1. **Install Firebase CLI** (if not already installed)
   ```bash
   npm install -g firebase-tools
   firebase login
   ```

2. **Initialize Firebase Functions** (in your project root)
   ```bash
   firebase init functions
   ```
   - Select your Firebase project
   - Choose Python or Node.js runtime
   - Install dependencies

3. **Create Trading Strategy Function** (`functions/index.js` or `functions/main.py`)
   ```javascript
   // Example: EMA Strategy Cloud Function
   const functions = require('firebase-functions');
   const admin = require('firebase-admin');
   admin.initializeApp();
   
   exports.calculateEMA = functions.https.onCall(async (data, context) => {
     // EMA 9/21 calculation logic
     const { symbol, period } = data;
     // Implementation here
   });
   ```

4. **Deploy Functions**
   ```bash
   firebase deploy --only functions
   ```

### Firebase Security Rules
Update in Firebase Console > Realtime Database > Rules:

### Example Security Rules:

```json
{
  "rules": {
    "users": {
      "$uid": {
        ".read": "$uid === auth.uid",
        ".write": "$uid === auth.uid",
        "trades": {
          ".indexOn": ["timestamp", "status"]
        },
        "positions": {
          ".indexOn": ["symbol", "status"]
        }
      }
    },
    ".read": false,
    ".write": false
  }
}
```

## Step 3: Payment Integration

### Option A: Paddle
1. Create products in Paddle Dashboard
2. Set webhook URL: `https://your-frontend.onrender.com/api/paddle/webhook`
3. Configure product IDs in environment variables

### Option B: LemonSqueezy
1. Create products in LemonSqueezy
2. Set webhook URL: `https://your-frontend.onrender.com/api/lemonsqueezy/webhook`
3. Configure variant IDs in environment variables

## Step 4: Domain Configuration

1. **Custom Domain** (Optional)
   - Add custom domain in Render Dashboard
   - Update DNS records (CNAME or A record)
   - Enable HTTPS (automatic with Render)

2. **CORS Configuration**
   - Add your domain to Firebase authorized domains
   - Update backend CORS settings to allow your frontend domain

## Step 5: Post-Deployment Checklist

- [ ] Test authentication flow (signup, login, logout)
- [ ] Verify Firebase data read/write
- [ ] Test language switching (EN/TR)
- [ ] Verify payment flow (test mode first)
- [ ] Check all API endpoints
- [ ] Test WebSocket connections (if implemented)
- [ ] Monitor error logs in Render Dashboard
- [ ] Set up monitoring alerts
- [ ] Configure backup strategy for Firebase

## Monitoring & Maintenance

- **Render Dashboard**: Monitor service health, logs, and metrics
- **Firebase Console**: Track database usage, authentication stats
- **Payment Provider**: Monitor subscriptions and revenue
- **Error Tracking**: Consider integrating Sentry or similar

## Rollback Strategy

If deployment fails:
1. Render allows instant rollback to previous deployment
2. Keep Firebase rules versioned
3. Maintain database backups

## Performance Optimization

- Enable Render CDN for static assets
- Optimize bundle size with code splitting
- Use Firebase caching strategies
- Implement proper loading states
- Add service worker for PWA capabilities

## Security Best Practices

- ✅ Never commit .env files
- ✅ Use Firebase security rules
- ✅ Encrypt API keys in database
- ✅ Implement rate limiting
- ✅ Enable HTTPS only
- ✅ Regular dependency updates
- ✅ Monitor for security alerts
