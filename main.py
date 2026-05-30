from urllib import request

from fastapi import Depends, FastAPI, HTTPException, Request, Form, status
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr
from fastapi.responses import RedirectResponse
from sympy import Order
from sqlalchemy.orm import Session
from database import get_db
from model_db import User, Inventory, Order
app = FastAPI()
from pathlib import Path

templates = Jinja2Templates(directory="templates")

@app.get("/login")
def get_login_page(request: Request):
    print("LOGIN ROUTE HIT")
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "test": "123"}
    )
from dependancies import create_access_token, get_current_user ,create_employees , delete_employees , update_employees


@app.post("/login")
def login(email: str = Form(...), password: str = Form(...)):
    print(f"Email received: {email}")
    print(f"Password received: {password}")
    
    token = create_access_token({"sub": email})
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True, secure=False)
    return response

@app.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request}
    )

@app.get("/profile")
def profile(request: Request):
    return templates.TemplateResponse(
        "profile.html",
        {"request": request}
    )

@app.get("/orders")
def orders(request: Request):
    return templates.TemplateResponse(
        "orders.html",
        {"request": request}
    )
from schemas import OrdersCreate, orders
from schemas import OrdersCreate
from model_db import Inventory, Order

@app.post("/orders")
def create_order(
    request: Request,
    item: str = Form(...),
    quantity: int = Form(...),
    db: Session = Depends(get_db)
):
    
    current_user = get_current_user(request)

    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than zero")
    inventory_item = db.query(Inventory).filter(Inventory.item == item).first()
    if not inventory_item:
        raise HTTPException(status_code=404, detail="Item not found in inventory")
    
    if inventory_item.quantity < quantity:
        raise HTTPException(status_code=400, detail="Not enough items in inventory")
    
    Inventory.quantity -= quantity
    new_order = Order(email=current_user, item=item, quantity=quantity)

    db.add(new_order)
    db.commit()

    return RedirectResponse(
        url="/orders",
        status_code=status.HTTP_302_FOUND
    )

from model_db import Inventory

@app.get("/inventory")
def inventory(request: Request, db: Session = Depends(get_db)):

    items = db.query(Inventory).all()
    print("ENDPOINT HIT")
    return templates.TemplateResponse(
        "inventory.html",
        {"request": request, "items": items}
    )

@app.get("/employees")
def employees(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()
    return templates.TemplateResponse(
        "employees.html",
        {"request": request,
         "users": users}
    )


@app.post("/employees")
async def employees(request: Request, db: Session = Depends(get_db)):

    form = await request.form()

    action = form.get("action")

    if action == "create" or action is None:
        email = form.get("email")
        name = form.get("name")

        is_admin = 1 if form.get("is_admin") == "on" else 0

        create_employees(
            email=email,
            name=name,
            is_admin=is_admin,
            db=db
        )

    elif action == "update":

        employee_id = int(form.get("employee_id"))
        email = form.get("email")
        name = form.get("name")

        is_admin = 1 if form.get("is_admin") == "on" else 0

        update_employees(
            employee_id=employee_id,
            email=email,
            name=name,
            is_admin=is_admin,
            db=db
        )

    elif action == "delete":

        employee_id = int(form.get("employee_id"))

        delete_employees(employee_id, db=db)

    return RedirectResponse(
        url="/employees",
        status_code=302
    )