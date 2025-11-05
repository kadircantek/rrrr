"""
Admin API Endpoints
Requires admin authentication for all operations
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import logging

from backend.auth import get_current_user, set_user_plan

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/admin", tags=["admin"])

class UpdatePlanRequest(BaseModel):
    user_id: str
    plan: str  # 'free', 'pro', or 'enterprise'

class UpdateRoleRequest(BaseModel):
    user_id: str
    role: str  # 'admin' or 'user'

async def verify_admin(current_user = Depends(get_current_user)):
    """Verify that the current user is an admin"""
    try:
        import firebase_admin
        from firebase_admin import db
        
        user_id = current_user.get("user_id")
        
        # Check admin role in Firebase
        ref = db.reference(f'/user_roles/{user_id}/role')
        role = ref.get()
        
        if role != 'admin':
            raise HTTPException(status_code=403, detail="Admin access required")
        
        return current_user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error verifying admin: {str(e)}")
        raise HTTPException(status_code=403, detail="Failed to verify admin status")

@router.post("/update-plan")
async def update_user_plan(
    request: UpdatePlanRequest,
    admin_user = Depends(verify_admin)
):
    """
    Update a user's subscription plan (Admin only)
    """
    try:
        result = await set_user_plan(request.user_id, request.plan)
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error", "Failed to update plan"))
        
        return {
            "success": True,
            "message": f"Successfully updated user {request.user_id} to {request.plan} plan"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user plan: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/update-role")
async def update_user_role(
    request: UpdateRoleRequest,
    admin_user = Depends(verify_admin)
):
    """
    Update a user's role (Admin only)
    """
    try:
        import firebase_admin
        from firebase_admin import db
        from datetime import datetime
        
        if request.role not in ['admin', 'user']:
            raise HTTPException(status_code=400, detail="Invalid role. Must be: admin or user")
        
        # Update role in Firebase
        ref = db.reference(f'/user_roles/{request.user_id}')
        ref.set({
            'role': request.role,
            'updatedAt': datetime.utcnow().isoformat()
        })
        
        return {
            "success": True,
            "message": f"Successfully updated user {request.user_id} to {request.role} role"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user role: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
