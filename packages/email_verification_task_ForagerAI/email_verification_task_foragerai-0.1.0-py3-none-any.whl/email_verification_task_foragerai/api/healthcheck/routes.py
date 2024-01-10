from typing import Any
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def healthcheck() -> Any:
    return {"status_code": 200, "detail": "ok", "result": "working"}
