from fastapi import HTTPException, Depends

from email_verification_task_ForagerAI.crud import BaseCRUD
from email_verification_task_ForagerAI.services import HunterClient
from email_verification_task_ForagerAI.utils import results_storage
from email_verification_task_ForagerAI import schemas

from typing import List, Optional, Any

client = HunterClient()


class EmailResultCRUD(BaseCRUD):
    async def create(
        self, email: Optional[str] = None, domain: Optional[str] = None
    ) -> schemas.EmailCheckResult:
        """Creates a new validation result record for an email address or domain.

        Args:
            email (Optional[str]): The email address to validate.
            domain (Optional[str]): The domain to search for email addresses.

        Returns:
            EmailCheckResult: The result of the check.

        Raises:
            HTTPException: If an error occurred or no data was transferred.
        """
        # Check if a record already exists with this email address or domain
        identifier = email if email is not None else domain

        if not identifier:
            raise HTTPException(
                status_code=400, detail="You must specify an email address or domain."
            )

        if identifier in results_storage:
            return schemas.EmailCheckResult(
                id=identifier, data=results_storage[identifier]
            )

        if email:
            result_data = await client.verify_email(email)
        elif domain:
            result_data = await client.search_email(domain)
        else:
            raise HTTPException(
                status_code=400, detail="You must specify an email address or domain."
            )

        if not result_data:
            raise HTTPException(
                status_code=400,
                detail="Data retrieval failed. Run a verification request.",
            )

        results_storage[identifier] = result_data
        return schemas.EmailCheckResult(id=identifier, data=result_data)

    async def read(self, result_id: str) -> schemas.EmailCheckResult:
        """Reads an email result from the storage by its string.

        Args:
            result_id (str): The string of the email or the domain result to retrieve.

        Returns:
            EmailCheckResult: The retrieved email result.
        """
        data = results_storage.get(result_id)
        return schemas.EmailCheckResult(id=result_id, data=data)

    async def read_all(self) -> List[schemas.EmailCheckResult]:
        """Retrieves all email results from the storage.

        Returns:
            List[EmailCheckResult]: A list of all stored email results.
        """
        return [
            schemas.EmailCheckResult(id=key, data=value)
            for key, value in results_storage.items()
        ]

    async def update(
        self, email_domain: str, update_data: schemas.UpdateEmailResult
    ) -> schemas.EmailCheckResult:
        """
        Updates an existing record of the check result.

        Args:
            email_domain (str): The identifier of the record to update.
            update_data (UpdateEmailResult): The data to update.

        Returns:
            EmailCheckResult: The updated check result.

        Raises:
            HTTPException: If the record was not found.
        """
        if email_domain not in results_storage:
            raise HTTPException(status_code=400, detail="No result found.")

        for key, value in update_data.model_dump(exclude_unset=True).items():
            results_storage[email_domain][key] = value

        return schemas.EmailCheckResult(
            id=email_domain, data=results_storage[email_domain]
        )

    async def delete(self, email_domain: str) -> Any:
        """Deletes an email result from the storage.

        Args:
            email_domain (str): The string of the email result to delete.

        Raises:
            ValueError: If no result is found to delete.
        """
        if email_domain not in results_storage:
            raise ValueError("No result found.")
        del results_storage[email_domain]
