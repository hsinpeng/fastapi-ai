from fastapi import HTTPException
from fastapi.params import Header
from typing import Optional

def pagination_parms(keyword:Optional[str]=None, last:int=0, limit:int=50):
    return {
        "keyword":keyword,
        "last":last,
        "limit":limit
    }

def test_verify_token(verify_header:str = Header()):
    if verify_header != "1234567890":
        raise HTTPException(status_code=403, detail="Forbidden")
    return verify_header