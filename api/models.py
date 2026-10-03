from pydantic import BaseModel,field_validator
import re

class UserRegister(BaseModel):
    username:str
    password:str
    role:str

    @field_validator("username")
    @classmethod
    def validate_username(cls,value):

        value = value.strip()
    
        if value == "":
            raise ValueError("Username cannot be empty.")
        
        if len(value)<3:
            raise ValueError("Username must be at least 3 characters.")
        
        if len(value)>30:
            raise ValueError("username cannot be more than 30 characters long.")
        
        return value
    
    @field_validator("password")
    @classmethod
    def validate_password(cls,value):
        if len(value)<8:
            raise ValueError("Password must be at least 8 characters long.")
        
        if not re.search(r"[A-Z]",value):
            raise ValueError("Password must contain an uppercase letter.")
        
        if not re.search(r"[a-z]",value):
            raise ValueError("Password must contain a lowercase letter.")
        
        if not re.search(r"\d",value):
            raise ValueError("Password must contain atleast one digit.")
        
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain a special character.")
        
        return value
    
    @field_validator("role")
    @classmethod
    def validate_role(cls,value):
        value=value.lower().strip()
        if value not in ("viewer","analyst"):
            raise ValueError("Invalid role. Role must be either 'viewer' or 'analyst' .")
        return value