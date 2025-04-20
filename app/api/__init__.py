from fastapi import APIRouter

from app.api.admin.views import router as admin_router
from app.api.ping.views import router as ping_router
from app.api.users.views.auth import router as auth_router
from app.api.users.views.elder import router as elder_router
from app.api.users.views.users import router as users_router

router = APIRouter(prefix="/api")

router.include_router(ping_router)
router.include_router(auth_router)
router.include_router(elder_router)
router.include_router(admin_router)
router.include_router(users_router)
