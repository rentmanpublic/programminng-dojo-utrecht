from fastapi import FastAPI
import rotor
import requests
from pydantic import BaseModel

app = FastAPI()

# reflector = {
#     "from": [],
#     "to": []
# }

class Position(BaseModel):
    wire: str 
    pos: str


class States(BaseModel):
    reflector: str 
    r1_position: Position
    r2_position: Position
    r3_position: Position

global_states = {
    "reflector": None,
    "r1_position": None,
    "r2_position": None,
    "r3_position": None,
}

rotor = "https://unevanescently-vehicular-lin.ngrok-free.dev"

# @app.get("/")
# def read(q: str, configuration: str | None = None):
#     return {"q": q, "configuration": str}

# to rotor
@app.post("/send")
def send_key(k: str):
    # rotors call 321
    forward_response = requests.post(f'{rotor}/forward', json={
        "char": k,
        "rotor_state": f'{global_states["r1_position"]['pos']},{global_states["r2_position"]['pos']},{global_states["r3_position"]['pos']}'
    }).json()

    print(forward_response)

    # todo: reflector call
    character = reflect(forward_response["char"])

    # todo: rotors call 321
    backward_response = requests.post(f'{rotor}/backward', json={
        "key": character,
        "state": forward_response["state"]
    }).json()

    r1,r2,r3 = backward_response["state"].split(",")

    global_states['r1_position']['pos'] = r1
    global_states['r2_position']['pos'] = r2 
    global_states['r3_position']['pos'] = r3

def reflect(input_char):

    return input_char
    # todo: do reflection stuff here

# set states
@app.post("/states")
def set_state(states: States):
    print(states)
    global global_states
    
    global_states = states

    # response = requests.get('http://rotor/', data={
    #     "key": k,
    #     "state": gloabl_states
    # }).json()
    return True

# get states
@app.get("/states")
def states():
    return global_states