from fastapi import APIRouter, HTTPException, Path, Body
from typing import List, Optional, Dict

from email_verification_task_ForagerAI.crud import EmailResultCRUD
from email_verification_task_ForagerAI import schemas


router = APIRouter()
# Instantiate the CRUD class
email_result_crud = EmailResultCRUD()


@router.post("/emails/", response_model=schemas.EmailCheckResult)
async def create_email_result(
    email: Optional[str] = None, domain: Optional[str] = None
):
    """Create a new email result.

    Args:
        email (str): The data to be associated with the new email result.
        domain (str): The data to be associated with the new domain result.

    Returns:
        EmailCheckResult: The created email or domain result.
    """
    try:
        return await email_result_crud.create(email=email, domain=domain)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="You must specify an email address or domain.",
        )


@router.get("/emails/{email_domain}", response_model=schemas.EmailCheckResult)
async def read_email_result(email_domain: str):
    """Retrieve an email result.

    Args:
        email_domain (str): The string of the email result to retrieve.

    Returns:
        EmailCheckResult: The requested email result.
    """
    try:
        return await email_result_crud.read(email_domain)
    except ValueError:
        raise HTTPException(status_code=400, detail="Result not found")


@router.get("/emails/", response_model=List[schemas.EmailCheckResult])
async def read_all_email_results():
    """Retrieve all stored email results.

    Returns:
        List[EmailCheckResult]: A list of all email results.
    """
    try:
        return await email_result_crud.read_all()
    except ValueError:
        raise HTTPException(status_code=400, detail="Result not found")


@router.put("/emails/{email_domain}", response_model=schemas.EmailCheckResult)
async def update_email_result(
    email_domain: str = Path(..., description="Email address or domain to update"),
    update_data: schemas.UpdateEmailResult = Body(
        ..., description="Data to update the result"
    ),
):
    """
    Updates the verification result record for the specified email address or domain.

    Args:
        email_domain (str): The email address or domain to update.
        update_data (UpdateEmailResult): The data to update the result.

    Returns:
        EmailCheckResult: The updated check result.
    """
    try:
        return await email_result_crud.update(
            email_domain=email_domain, update_data=update_data
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Result not found")


@router.delete("/emails/{email_domain}", response_model=Dict[str, str])
async def delete_email_result(email_domain: str):
    """Delete an email result.

    Args:
        email_domain (str): The string of the email result to delete.

    Returns:
        EmailCheckResult: The deleted email result.
    """
    try:
        await email_result_crud.delete(email_domain)
        return {"message": "Deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
