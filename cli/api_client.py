import requests

BASE_URL = "http://127.0.0.1:8000"

def register_user(username:str,
                  password:str,
                  role:str):
    payload={
        "username":username,
        "password":password,
        "role":role
    }

    try:
        response=requests.post(f"{BASE_URL}/register",json=payload,timeout=10)

        return {
            "success":True,
            "response":response
        }
    
    except requests.RequestException:
        
        return {
            "success": False,
            "message":"could not connect to the api server."
        }
    
def login_user(username:str,
                password:str):
    payload={
        "username":username,
        "password":password,
    }

    try:
        response=requests.post(f"{BASE_URL}/login",data=payload,timeout=10)

        return {
            "success":True,
            "response":response
        }
    
    except requests.RequestException:
        return {
            "success": False,
            "message":"could not connect to the api server."
        }
    
def get_sales(token: str,params:dict = None):
    
    headers={
        "Authorization":f"Bearer {token}"
    }

    try:

        response=requests.get(f"{BASE_URL}/sales",headers=headers,params=params,timeout=10)

        return {
            "success": True,
            "response": response
        }

    except requests.RequestException:

        return {
            "success":False,
            "message":"could not connect to the api server."
        }

def get_analytics(token: str,params:dict = None):
    
    headers={
        "Authorization":f"Bearer {token}"
    }

    try:

        response=requests.get(f"{BASE_URL}/analytics",headers=headers,params=params,timeout=10)

        return {
            "success": True,
            "response": response
        }

    except requests.RequestException:
        
        return {
            "success":False,
            "message":"could not connect to the api server."
        }