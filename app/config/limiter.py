from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request

# IP-based limiter
ip_limiter = Limiter(key_func=get_remote_address)

# User-based limiter
def get_user_key(request: Request):
    user = getattr(request.state, "user", None)
    if user:
        return str(user.id)
    return request.client.host  

user_limiter = Limiter(key_func=get_user_key)
