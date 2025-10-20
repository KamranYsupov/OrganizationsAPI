import secrets

import loguru
from fastapi import Header, HTTPException, Depends

from app.core.config import settings


from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

http_bearer = HTTPBearer()

def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    api_key = credentials.credentials
    loguru.logger.info(f"{api_key} {settings.api_key}")
    if not secrets.compare_digest(api_key, settings.api_key):
        raise HTTPException(status_code=403, detail='Invalid API key')

    return True
