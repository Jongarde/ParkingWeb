from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader, Template
from appComponents import Reservation, BrandListRequest
from usermanMySQL import loginEmployee, registerEmployee
import datetime
import json
import os
import imageio

app = FastAPI()

env = Environment(loader=FileSystemLoader("templates"))
login_template = env.get_template("login.html")
register_template = env.get_template("register.html")
template = Template(open("templates/main.html").read())

@app.get("/login")
def login():
    return HTMLResponse(login_template.render())

@app.post("/login")
async def login(request: Request):
    data = await request.json()
    dni = data["dni"]
    psw = data["pasw"]
    user = loginEmployee(dni, psw)
    if user:
        return {"success": True}
    else:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

@app.get("/register")
def register():
    return HTMLResponse(register_template.render())

@app.post("/register")
async def register(request: Request):
    data = await request.json()
    dni = data["dni"]
    name = data["name"]
    email = data["email"]
    pasw = data["pasw"]
    r_pasw = data["r_pasw"]
    user = registerEmployee(dni, name, email, pasw, r_pasw)
    if user:
        return {"success": True}
    else:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

@app.get("/test")
def register():
    return {"message": "Register or Login Success!! :)"}


@app.post("/reservations")
def makeReservation(reservation: Reservation):
    return {"message": f"The car with the registration number {reservation.registration_plate} has reserved the space nº{reservation.id_parkingLot} from {datetime.datetime.fromtimestamp(reservation.start_reservation)} to {datetime.datetime.fromtimestamp(reservation.end_reservation)}"}

@app.post("/brands")
def process_brands(request: BrandListRequest):
    file_path = "slots.json"
    if os.path.getsize(file_path) == 0:
        slot_number = 36
        slots = []
        for i in range(slot_number):
            slots.append(0)
        with open(file_path, "w") as file:
            json.dump(slots, file)

    received_brands = request.brands
    with open("brands.json", "w") as f:
        json.dump(received_brands, f)
    return {"success": True}

@app.get("/brands")
def get_brands():
    with open("slots.json", "r") as f:
        slots = json.load(f)
    with open("brands.json", "r") as f:
        brands = json.load(f)
    content = template.render(my_list=brands, slot_list=slots)
    return HTMLResponse(content=content, status_code=200, headers={"content-type": "text/html"})
