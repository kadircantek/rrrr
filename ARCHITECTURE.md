# AI Trader - Project Architecture

## Overview
Full-stack trading automation platform with React frontend and Firebase backend.

## Tech Stack

### Frontend
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite 5
- **UI Library**: shadcn/ui + Radix UI
- **Styling**: Tailwind CSS
- **State Management**: React Context API
- **Routing**: React Router v6
- **i18n**: i18next (TR/EN support)
- **Charts**: Recharts
- **Deployment**: Render.com (Web Service)

### Backend
- **Authentication**: Firebase Auth (Email/Password + Google OAuth)
- **Database**: Firebase Realtime Database
- **Storage**: Firebase Storage
- **Serverless Functions**: Firebase Cloud Functions
- **Payment**: Paddle or LemonSqueezy

### External APIs
- **Exchanges**: Binance, Bybit, OKX, Coinbase, MEXC
- **Trading Strategy**: EMA 9/21 crossover

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Render.com (Web Service)                │
│                                                             │
│  ┌───────────────────────────────────────────────────┐   │
│  │         React Frontend (Vite Build)               │   │
│  │  - Dashboard UI                                    │   │
│  │  - Auth Pages                                      │   │
│  │  - Trading Controls                                │   │
│  │  - Real-time Charts                                │   │
│  └───────────────┬───────────────────────────────────┘   │
│                  │                                         │
└──────────────────┼─────────────────────────────────────────┘
                   │
                   ▼
    ┌──────────────────────────────────────┐
    │      Firebase Backend Services        │
    ├──────────────────────────────────────┤
    │  • Authentication (Auth)              │
    │  • Realtime Database                  │
    │  • Cloud Functions (Trading Logic)    │
    │  • Storage (User Files)               │
    └──────┬───────────────────────────┬────┘
           │                           │
           ▼                           ▼
    ┌─────────────┐          ┌─────────────────┐
    │  Exchange   │          │  Payment APIs   │
    │  APIs       │          │  (Paddle/Lemon) │
    │  (Binance,  │          └─────────────────┘
    │   Bybit,    │
    │   etc.)     │
    └─────────────┘
```

## Current Status

### ✅ Completed
1. **Frontend Structure**
   - Component architecture with shadcn/ui
   - Responsive design system
   - Dark/light theme toggle
   - Multi-language support (TR/EN)
   - Error boundary implementation
   
2. **Authentication System**
   - Email/password signup & login
   - Google OAuth integration
   - Password reset functionality
   - Protected routes
   - User session management

3. **Firebase Integration**
   - Auth configured and active
   - Realtime Database connected
   - Security rules template ready

4. **UI Components**
   - Dashboard layout
   - Stats cards
   - Position cards
   - Auth pages
   - Language switcher
   - Theme toggle

5. **Subscription System (Structure)**
   - Payment integration skeleton (Paddle/LemonSqueezy)
   - Subscription hook (`useSubscription`)
   - Tier-based access control (free/pro/unlimited)
   - Rate limiting configuration

6. **Deployment Ready**
   - Build configuration optimized
   - Environment variable templates
   - Deployment guide (DEPLOYMENT.md)

### 🔄 Pending Implementation

1. **Exchange API Adapters** (Priority: HIGH)
   - Binance API integration
   - API key encryption/storage in Firebase
   - Position open/close functions
   - Real-time price feeds

2. **EMA Trading Strategy** (Priority: HIGH)
   - Firebase Cloud Function implementation
   - EMA 9/21 calculation logic
   - TP/SL management
   - Position monitoring (scheduled function)

3. **Real-time Dashboard Data** (Priority: HIGH)
   - Firebase data fetching hooks
   - WebSocket price updates
   - Live P&L calculations
   - Trade history display

4. **Payment Webhooks** (Priority: MEDIUM)
   - Paddle/LemonSqueezy webhook handlers
   - Subscription status updates in Firebase
   - Payment success/failure notifications

5. **Firebase Cloud Functions** (Priority: HIGH)
   ```bash
   # Initialize in project
   firebase init functions
   
   # Deploy functions
   firebase deploy --only functions
   ```

6. **Firebase Security Rules** (Priority: HIGH)
   - User-specific read/write rules
   - API key protection
   - Admin role setup (if needed)

## File Structure

```
├── src/
│   ├── components/
│   │   ├── ui/                    # shadcn/ui components
│   │   ├── ErrorBoundary.tsx      # Error handling
│   │   ├── Features.tsx
│   │   ├── Hero.tsx
│   │   ├── LanguageSwitcher.tsx   # i18n toggle
│   │   ├── PositionCard.tsx       # Trading positions
│   │   ├── Pricing.tsx
│   │   ├── StatsCard.tsx          # Dashboard stats
│   │   └── ThemeToggle.tsx        # Dark/light mode
│   │
│   ├── contexts/
│   │   └── AuthContext.tsx        # Firebase Auth provider
│   │
│   ├── hooks/
│   │   ├── use-mobile.tsx
│   │   ├── use-toast.ts
│   │   └── useSubscription.ts     # Subscription management
│   │
│   ├── lib/
│   │   ├── apiConfig.ts           # API endpoints & rate limits
│   │   ├── firebase.ts            # Firebase initialization
│   │   ├── i18n.ts                # Internationalization
│   │   ├── payment.ts             # Payment provider config
│   │   └── utils.ts
│   │
│   ├── locales/
│   │   ├── en.json                # English translations
│   │   └── tr.json                # Turkish translations
│   │
│   ├── pages/
│   │   ├── Auth.tsx               # Login/Signup page
│   │   ├── Dashboard.tsx          # Main dashboard
│   │   ├── Index.tsx              # Landing page
│   │   └── NotFound.tsx
│   │
│   ├── App.tsx                    # Main app component
│   └── main.tsx                   # Entry point
│
├── .env.production.example        # Production env template
├── ARCHITECTURE.md                # This file
├── DEPLOYMENT.md                  # Deployment guide
├── NEXT_STEPS.md                  # Implementation roadmap
└── vite.config.ts                 # Vite configuration
```

## Environment Variables

### Required for Render Deployment

```bash
# Firebase (from Firebase Console)
VITE_FIREBASE_API_KEY=
VITE_FIREBASE_AUTH_DOMAIN=
VITE_FIREBASE_DATABASE_URL=
VITE_FIREBASE_PROJECT_ID=
VITE_FIREBASE_STORAGE_BUCKET=
VITE_FIREBASE_MESSAGING_SENDER_ID=
VITE_FIREBASE_APP_ID=
VITE_FIREBASE_MEASUREMENT_ID=

# Payment Provider (choose one)
VITE_PADDLE_VENDOR_ID=
VITE_LEMONSQUEEZY_STORE_ID=

# App Info
VITE_APP_VERSION=1.0.0
VITE_APP_ENV=production
```

## Deployment Commands

### Local Development
```bash
npm run dev          # Start dev server
npm run build        # Build for production
npm run preview      # Preview production build
```

### Render Deployment
- **Build Command**: `npm run build`
- **Start Command**: `npm run preview`
- **Service Type**: Web Service
- **Environment**: Node 18.x+

## Security Considerations

1. **Firebase Security Rules**
   - Enable RLS (Row-Level Security)
   - User can only access their own data
   - API keys encrypted before storage

2. **API Key Protection**
   - Never commit .env files
   - Use Firebase encryption for exchange API keys
   - Implement rate limiting per subscription tier

3. **Authentication**
   - Firebase Auth handles token management
   - Automatic session refresh
   - Secure password reset flow

## Subscription Tiers

| Feature | Free | Pro | Unlimited |
|---------|------|-----|-----------|
| Price | $0 | $29/mo | $99/mo |
| Positions | 1 | 10 | Unlimited |
| Exchanges | 1 | 5 | Unlimited |
| API Requests/min | 10 | 60 | 300 |
| EMA Strategy | ❌ | ✅ | ✅ |
| Custom Strategies | ❌ | ❌ | ✅ |
| Priority Support | ❌ | ❌ | ✅ |

## Next Priority Tasks

1. **Implement Binance API adapter** (src/lib/exchanges/binance.ts)
2. **Create Firebase Cloud Functions** for EMA strategy
3. **Add real-time data fetching** to Dashboard
4. **Set up Firebase Security Rules**
5. **Integrate payment webhooks** (Paddle or LemonSqueezy)
6. **Test end-to-end flow** (signup → payment → trading)

## Resources

- [Firebase Console](https://console.firebase.google.com/)
- [Render Dashboard](https://dashboard.render.com/)
- [Paddle Docs](https://developer.paddle.com/)
- [LemonSqueezy Docs](https://docs.lemonsqueezy.com/)
- [Binance API Docs](https://binance-docs.github.io/apidocs/)
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Full deployment instructions
- [NEXT_STEPS.md](./NEXT_STEPS.md) - Detailed implementation tasks
