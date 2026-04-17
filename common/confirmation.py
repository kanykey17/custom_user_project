from .redis_client import redis_client

def save_code(email, code):
    key = f"confirm_code:{email}"
    redis_client.setex(key, 300, code)



def verify_code(email, code):
    key = f"confirm_code:{email}"
    stored_code = redis_client.get(key)

    if not stored_code:
        return False

    if stored_code == code:
        redis_client.delete(key)  
        return True

    return False