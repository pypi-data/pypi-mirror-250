from fastapi import APIRouter, Body

from email_verification_task_ForagerAI.services import HunterClient
from email_verification_task_ForagerAI import schemas
from email_verification_task_ForagerAI.utils import results_storage

router = APIRouter()
client = HunterClient()


@router.post("/email/verify", response_model=schemas.EmailCheckResult)
async def verify_email(body: schemas.EmailRequest = Body(..., embed=True)):
    """
    Verifies the email address.

    Args:
        body (schemas.EmailRequest): The email address to verify.

    Returns:
        EmailCheckResult: The result of email verification.
    """
    result: dict = await client.verify_email(body.email)
    return schemas.EmailCheckResult(id=body.email, data=result)


@router.post("/domain/search", response_model=schemas.EmailCheckResult)
async def search_email(body: schemas.DomainRequest = Body(..., embed=True)):
    """
    Search for email addresses by domain.

    Args:
        body (schemas.DomainRequest): The domain to search for email addresses.

    Returns:
        EmailCheckResult: The result of the email search.
    """
    result: dict = await client.search_email(body.domain)
    return schemas.EmailCheckResult(id=body.domain, data=result)
