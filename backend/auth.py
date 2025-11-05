"""
Authentication and Authorization Module
Handles JWT and Firebase token verification
"""
from fastapi import HTTPException, Header
import jwt
from datetime import datetime, timedelta
import httpx
import os

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY", "AIzaSyDqAsiITYyPK9bTuGGz7aVBkZ7oLB2Kt3U")

def create_jwt_token(user_id: str, email: str) -> str:
    """Create JWT token for user authentication"""
    payload = {
        "user_id": user_id,
        "email": email,
        "exp": datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_jwt_token(token: str) -> dict:
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def verify_firebase_token_with_identitytoolkit(id_token: str) -> dict:
    """
    Verify Firebase ID token by calling Google Identity Toolkit.
    Returns minimal user info on success.
    """
    if not FIREBASE_API_KEY:
        raise HTTPException(status_code=500, detail="Missing FIREBASE_API_KEY on server")
    
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={FIREBASE_API_KEY}",
                json={"idToken": id_token},
                timeout=10.0,
            )
        
        if resp.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid Firebase ID token")
        
        data = resp.json()
        users = data.get("users", [])
        
        if not users:
            raise HTTPException(status_code=401, detail="Invalid Firebase ID token")
        
        u = users[0]
        return {
            "user_id": u.get("localId"),
            "email": u.get("email"),
            "firebase_uid": u.get("localId")
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Firebase token verification error: {str(e)}")
        raise HTTPException(status_code=401, detail="Failed to verify Firebase token")

async def get_current_user(authorization: str = Header(None)):
    """
    Dependency to get current authenticated user.
    Supports both local JWT and Firebase ID token.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401, 
            detail="Missing or invalid authorization header"
        )
    
    token = authorization.replace("Bearer ", "")

    # Try local JWT first
    try:
        return verify_jwt_token(token)
    except HTTPException:
        # Fallback to Firebase ID token
        return await verify_firebase_token_with_identitytoolkit(token)

async def get_user_plan(user_id: str) -> str:
    """
    Get user's subscription plan from Firebase Realtime Database.
    Returns: 'free', 'pro', or 'enterprise'
    """
    try:
        import firebase_admin
        from firebase_admin import db
        
        # Initialize Firebase Admin if not already done
        try:
            firebase_admin.get_app()
        except ValueError:
            # App not initialized
            import firebase_admin
            from firebase_admin import credentials
            
            firebase_db_url = os.getenv("FIREBASE_DATABASE_URL")
            if not firebase_db_url:
                return "free"
            
            cred = credentials.Certificate({
                "type": "service_account",
                "project_id": os.getenv("FIREBASE_PROJECT_ID"),
                "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
                "private_key": os.getenv("FIREBASE_PRIVATE_KEY", "").replace("\\n", "\n"),
                "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
                "client_id": os.getenv("FIREBASE_CLIENT_ID"),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            })
            
            firebase_admin.initialize_app(cred, {
                'databaseURL': firebase_db_url
            })
        
        # Get subscription from Firebase
        ref = db.reference(f'/user_subscriptions/{user_id}')
        subscription = ref.get()
        
        if subscription and isinstance(subscription, dict):
            return subscription.get('tier', 'free')
        
        return "free"
        
    except Exception as e:
        print(f"Error fetching user plan: {str(e)}")
        return "free"

def check_plan_limits(plan: str, current_positions: int) -> dict:
    """
    Check if user can open more positions based on their plan
    
    Returns: {
        "can_open": bool,
        "max_positions": int,
        "message": str
    }
    """
    plan_limits = {
        "free": 1,
        "pro": 10,
        "enterprise": 50
    }
    
    max_positions = plan_limits.get(plan, 1)
    can_open = current_positions < max_positions
    
    return {
        "can_open": can_open,
        "max_positions": max_positions,
        "current_positions": current_positions,
        "message": f"Your {plan.upper()} plan allows {max_positions} open position(s). Currently: {current_positions}"
    }

async def set_user_plan(user_id: str, plan: str) -> dict:
    """
    Set user's subscription plan in Firebase (Admin function)
    """
    try:
        import firebase_admin
        from firebase_admin import db
        
        if plan not in ['free', 'pro', 'enterprise']:
            raise ValueError("Invalid plan. Must be: free, pro, or enterprise")
        
        # Initialize Firebase Admin if needed
        try:
            firebase_admin.get_app()
        except ValueError:
            return {"success": False, "error": "Firebase not initialized"}
        
        # Set subscription in Firebase
        ref = db.reference(f'/user_subscriptions/{user_id}')
        subscription_data = {
            'tier': plan,
            'startDate': datetime.utcnow().isoformat(),
            'status': 'active',
        }
        
        if plan != 'free':
            # Add 30 days expiration for paid plans
            expiration = datetime.utcnow() + timedelta(days=30)
            subscription_data['endDate'] = expiration.isoformat()
        
        ref.set(subscription_data)
        
        return {
            "success": True,
            "plan": plan,
            "message": f"User plan updated to {plan}"
        }
        
    except Exception as e:
        print(f"Error setting user plan: {str(e)}")
        return {"success": False, "error": str(e)}
