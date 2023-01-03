from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader
from appComponents import Reservation
from usermanMySQL import loginEmployee
import datetime

app = FastAPI()

env = Environment(loader=FileSystemLoader("templates"))
login_template = env.get_template("login.html")

@app.get("/login")
def login():
    return HTMLResponse(login_template.render())

@app.get("/register")
def register():
    return {"message": "On work"}

@app.post("/login")
async def login(request: Request):
    data = await request.json()
    dni = data["dni"]
    psw = data["psw"]
    user = loginEmployee(dni, psw)
    if user:
        return {"success": True}
    else:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

@app.post("/reservations")
def makeReservation(reservation: Reservation):
    return {"message": f"The car with the registration number {reservation.registration_plate} has reserved the space nº{reservation.id_parkingLot} from {datetime.datetime.fromtimestamp(reservation.start_reservation)} to {datetime.datetime.fromtimestamp(reservation.end_reservation)}"}