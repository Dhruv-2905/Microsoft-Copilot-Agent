import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from fastapi import HTTPException

def decode_jwt_token(token: str):
    """
    Decodes a JWT token without verification and returns the 'name' value as a string.
    """
    try:
        decoded = jwt.decode(token, options={"verify_signature": False})
        # Return the 'name' value as a string
        # return {"decoded_token": decoded}
        return decoded.get("name", "")
    except ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token has expired.")
    except InvalidTokenError as e:
        raise HTTPException(status_code=400, detail=f"Invalid token: {e}")

