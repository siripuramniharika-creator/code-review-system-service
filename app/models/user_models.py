from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str
class SignupRequest(BaseModel):
    fullname: str
    email: str
    password: str
    contact: str
    security_question: str
    security_answer: str
class ForgotPasswordRequest(BaseModel):
    email: str
    security_question: str  
    security_answer: str
    new_password: str