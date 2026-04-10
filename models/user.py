from pydantic import BaseModel



class CreateUserRequest(BaseModel):
    username: str
    password: str
    email: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str