def user_schema(user) -> dict:
  return {
    "id": str(user["_id"]),
    "name": user["name"],
    "last_name": user["last_name"],
    "username": user["username"],
    "email": user["email"],
    "password": user["password"],
    "role": user["role"]
  }

def users_schema(users) -> list:
  return [user_schema(user) for user in users]