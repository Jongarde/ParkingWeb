from fastapi import FastAPI, Request, HTTPException, Path
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader, Template
from appComponents import BrandListRequest
from usermanMySQL import loginEmployee, registerEmployee
from comprobations import checkDNI, checkRegistration, checkDate, getPrice
import json
import os

app = FastAPI()

env = Environment(loader=FileSystemLoader("templates"))
login_template = env.get_template("login.html")
register_template = env.get_template("register.html")
reservation_checker_template = env.get_template("reservation.html")
template = Template(open("templates/main.html").read())
detail_template = Template(open("templates/reservation_detail.html").read())

@app.get("/login", tags=["employees"])
def login():
    return HTMLResponse(login_template.render())

@app.post("/login", tags=["employees"])
async def login(request: Request):
    data = await request.json()
    dni = data["dni"]
    psw = data["pasw"]
    user = loginEmployee(dni, psw)
    if user:
        return {"success": True}
    else:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

@app.get("/register", tags=["employees"])
def register():
    return HTMLResponse(register_template.render())

@app.post("/register", tags=["employees"])
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

@app.get("/reservations", tags=["clients"])
def register():
    return HTMLResponse(reservation_checker_template.render())

@app.post("/reservations", tags=["employees"])
async def makeReservation(request: Request):
    data = await request.json()
    dni = data["dni"]
    r_plate = data["r_plate"]
    endtime = data["endtime"]
    enddate = data["enddate"]
    brand = data["brand"]
    randomIndex = data["randomIndex"]

    with open("reservations.json", "r") as f:
        reservations = json.load(f)
    for r in reservations:
        if(checkDate(r["enddate"], r["endtime"]) == False):
            slot_index = r["slot"]
            with open("slots.json", "r") as f:
                slots = json.load(f)
            slots[slot_index] = 0
            with open("slots.json", "w") as f:
                json.dump(slots, f)
            reservations.remove(r)
            with open("reservations.json", "w") as f:
                json.dump(reservations, f)

    if(checkDNI(dni) and checkRegistration(r_plate) and checkDate(enddate, endtime)):
        success = True
    else:
        success = False

    if(success):
        with open("reservations.json", "r") as f:
            reservations = json.load(f)
        reservations.append({
            "dni": dni, 
            "registration": r_plate, 
            "endtime": endtime, 
            "enddate": enddate, 
            "brand": brand, 
            "slot": randomIndex,
            "price": round(getPrice(enddate, endtime), 2)
        })
        with open("reservations.json", "w") as f:
            json.dump(reservations, f)

        with open("slots.json", "r") as f:
            slots = json.load(f)
        slots[randomIndex] = 1
        with open("slots.json", "w") as f:
            json.dump(slots, f)
        return {"success": True}
    else:
        raise HTTPException(status_code=401, detail="Reservation could not be completed")

@app.post("/checker", tags=["clients"])
async def register(request: Request):
    data = await request.json()
    r_plate = data["r_plate"]
    if(checkRegistration(r_plate)):
        return {"success": True}
    else:
        raise HTTPException(status_code=401, detail="Wrong registration plate format")

@app.get("/reservations/{r_plate}", tags=["clients"])
async def read_item(r_plate: str = Path(..., title="The registration plate of the vehicle parked")):
    with open("reservations.json", "r") as f:
        reservations = json.load(f)
    rese = None
    for r in reservations:
        if(r["registration"]==r_plate):
            rese = r
    if(rese is None):
        return {"message": "No values for the registration plate provided"}
    else:
        content = detail_template.render(dict=rese)
        return HTMLResponse(content=content, status_code=200, headers={"content-type": "text/html"})

@app.get("/brands", tags=["employees"])
def get_brands():
    with open("slots.json", "r") as f:
        slots = json.load(f)
    with open("brands.json", "r") as f:
        brands = json.load(f)
    content = template.render(my_list=brands, slot_list=slots)
    return HTMLResponse(content=content, status_code=200, headers={"content-type": "text/html"})

@app.post("/brands", tags=["employees"])
def process_brands(request: BrandListRequest):
    file_path = "reservations.json"
    if os.path.getsize(file_path) == 0:
        reservations = []
        with open(file_path, "w") as f:
            json.dump(reservations, f)

    file_path = "slots.json"
    if os.path.getsize(file_path) == 0:
        slot_number = 36
        slots = []
        for i in range(slot_number):
            slots.append(0)
        with open(file_path, "w") as f:
            json.dump(slots, f)

    received_brands = request.brands
    with open("brands.json", "w") as f:
        json.dump(received_brands, f)
    return {"success": True}

