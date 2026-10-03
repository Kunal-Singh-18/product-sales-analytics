from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from api.database import get_connection
from api.models import UserRegister

from api.security import (
    hash_password,
    verify_password,
    create_access_token
)

router=APIRouter()

@router.post('/register',status_code=201)
def register(user: UserRegister):
    connection = get_connection()
    cursor=connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            select id
            from users 
            where username = %s
            """,
            (user.username,)
        )
        
        existing_user = cursor.fetchone()

        if existing_user:
            raise HTTPException(
                status_code=409,
                detail = "this username already exists. "
            )
        
        hashed_password = hash_password(user.password)

        cursor.execute(
            """
            insert into users(
            username,
            password,
            role
            )
            values(
            %s,
            %s,
            %s
            )
            """,
            (
                user.username,
                hashed_password,
                user.role
            )
        )

        connection.commit()

        return {
            "message":"user registered successfully !"
        }

    finally:
        cursor.close()
        connection.close()

@router.post('/login')
def login(form_data : OAuth2PasswordRequestForm = Depends()):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            select
              username,
              password,
              role
            from users
            where username = %s
            """,
            (
                form_data.username,
            )
        )
        
        user=cursor.fetchone()

        if user is None:
            raise HTTPException(
                status_code= 401,
                detail = "invalid username or password."
            )
        
        if not verify_password(form_data.password,user["password"]):
            raise HTTPException(
                status_code=401,
                detail = "invalid username or password."
            )

        access_token = create_access_token(
            {
                "sub":user["username"],
                "role":user["role"]           
            }
        )

        return {
            "access_token" : access_token,
            "token_type" : "bearer",
            "username": user["username"],
            "role": user["role"]
        }
    finally:
        cursor.close()
        connection.close()
