import re
from datetime import datetime

def checkDNI(dni):
    if(len(dni) != 9):
        return False
    else:
        alphabet = "TRWAGMYFPDXBNJZSQVHLCKE"
        letter_idx = int(dni[:8])%23
        if(alphabet[letter_idx] != dni[8:]):
            return False
        else:
            return True

def checkRegistration(r_plate):
    if(len(r_plate) != 7):
        return False
    else:
        pattern = "^[0-9]{4}[BCDFGHJKLMNPQRSTVWXYZ]{3}$"
        if(re.match(pattern, r_plate)):
            return True
        else:
            return False

def convertDate(date, time):
    complete_date = date + " " + time
    complete_date_parsed = datetime.strptime(complete_date, "%Y-%m-%d %H:%M")
    return complete_date_parsed

def checkDate(date, time):
    complete_date = convertDate(date, time)

    if(complete_date > datetime.now()):
        return True
    else:
        return False

def getPrice(date, time):
    price_per_second = 4/3600
    end_date = convertDate(date, time)
    price = (end_date-datetime.now()).total_seconds()*price_per_second

    return price