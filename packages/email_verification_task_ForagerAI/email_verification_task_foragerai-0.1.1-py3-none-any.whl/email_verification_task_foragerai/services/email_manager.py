import httpx
from typing import Optional, Dict, Any

from fastapi import HTTPException

from email_verification_task_ForagerAI.core import hunter_settings


class HunterClient:
    def __init__(self):
        self.api_key = hunter_settings.API_KEY
        self.base_url = hunter_settings.BASE_URL
        self.headers = hunter_settings.HEADERS

    async def send_request(
        self,
        method: str,
        url: str,
        params: Dict[str, Any] = None,
        data: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """
        A universal method for making HTTP requests to the Hunter.io API.

        Args:
            method (str): HTTP method (e.g. 'GET', 'POST').
            url (str): URL for the request.
            params (Dict[str, Any], optional): Request parameters for GET requests.
            data (Dict[str, Any], optional): Data for POST requests.

        Returns:
            Dict[str, Any]: Response from the API.

        Raises:
            HTTPException: In case of an error in the API request or response.
        """
        async with httpx.AsyncClient() as client:
            try:
                if method.upper() == "GET":
                    response = await client.get(
                        f"{self.base_url}{url}", params=params, headers=self.headers
                    )
                elif method.upper() == "POST":
                    response = await client.post(
                        f"{self.base_url}{url}", data=data, headers=self.headers
                    )
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")

                response.raise_for_status()
                result = response.json()
                return result["data"]
            except httpx.HTTPStatusError as e:
                # HTTP status code error
                raise HTTPException(status_code=e.response.status_code, detail=str(e))
            except httpx.RequestError as e:
                # Network or connection error
                raise HTTPException(status_code=400, detail=f"Request failed: {str(e)}")

    async def verify_email(self, email: str) -> dict:
        """Asynchronously verify an email address"""
        params = {"email": email, "api_key": self.api_key}
        return await self.send_request("get", "/email-verifier", params)

    async def search_email(self, domain: str) -> dict:
        """Asynchronously search for email addresses associated with a given domain"""
        params = {"domain": domain, "api_key": self.api_key}
        return await self.send_request("get", "/domain-search", params)
