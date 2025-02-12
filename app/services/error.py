from fastapi import HTTPException, status as http_status


class NotFoundHTTPException(HTTPException):
    def __init__(self, entity_type: type, details: str = ""):
        super().__init__(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail=f"{entity_type.__name__}{details} not found",
        )
