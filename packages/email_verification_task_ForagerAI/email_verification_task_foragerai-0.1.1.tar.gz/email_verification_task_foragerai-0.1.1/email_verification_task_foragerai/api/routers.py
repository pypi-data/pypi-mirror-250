from fastapi import APIRouter
from email_verification_task_ForagerAI.api import check_emails, healthcheck, crud

api_router = APIRouter()

api_router.include_router(
    healthcheck.router, tags=["healthcheck"]
)

api_router.include_router(
    check_emails.router, tags=["check_emails"]
)

api_router.include_router(
    crud.router, tags=["crud"]
)
