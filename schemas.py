from pydantic import EmailStr , BaseModel

class login(BaseModel):
    email : EmailStr
    password : str

    class config:
        from_Attribute = True

class orders(BaseModel):
    id : int
    item : str
    quantity : int
    user_id : int

    class config:
        from_Attribute = True

class OrdersCreate(BaseModel):
    item : str
    quantity : int