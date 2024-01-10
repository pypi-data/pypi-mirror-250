from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Dict, Optional
import re


class EmailCheckResult(BaseModel):
    id: Optional[str]
    data: Dict


class EmailRequest(BaseModel):
    email: EmailStr


class DomainRequest(BaseModel):
    domain: str

    @field_validator("domain")
    def validate_domain(cls, v):
        if not re.match(
            r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}$", v
        ):
            raise ValueError("Incorrect domain format")
        return v


class UpdateEmailResult(BaseModel):
    status: Optional[str] = Field(
        None, description="Email or domain verification status"
    )
    result: Optional[str] = Field(None, description="The result of the test")
    last_checked: Optional[str] = Field(None, description="Time of the last check")
    data: Optional[Dict] = Field(
        None, description="Additional data or inspection results"
    )
