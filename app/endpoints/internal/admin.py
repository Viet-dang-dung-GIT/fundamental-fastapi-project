from fastapi import APIRouter

# because it's shared with other project in the organization, can't modify it
# and add a prefix, tags , response , dependencies,etc. directly to APIRouter
# so we want to set custom prefix include APIRouter that all its path operation start /admin
# secure with dependencies in main.py admin.router
router = APIRouter()


@router.post("/")
async def update_admin():
    return {"message": "Admin getting schwifty"}
