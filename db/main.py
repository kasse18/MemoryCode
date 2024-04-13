from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
import db
import api

app = FastAPI()

class Data_People(BaseModel):
    id: int
    name: str
    biography: str
    epitaph: str


class Data(BaseModel):
    id: int
    queue: str
    biography: str
    epitaph: str

class GetID(BaseModel):
    id: int

@app.post("/create")
async def create_new(item: GetID):
    status = await db.load_data([item.id])
    return {"status": status}

@app.post("/add")
async def add_data(item: Dict[str, str]):
    status = await db.update_data(item)
    return {"status": status}


@app.post("/create_people")
async def create_data_people(item: Dict): # [int, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str]
    status = await db.load_data_people(item)
    return {"status": status}

@app.post("/add_people")
async def add_data_people(item: Dict):
    status = await db.update_data_people(item)
    return {"status": status}

@app.post("/get")
async def return_data(item: GetID):
    status = await db.return_data(item.id)
    return {"data": status}


@app.post("/get_people")
async def return_data_people(item: GetID):
    status = await db.return_data_people(item.id)
    return {"data": status}


@app.post("/check")
async def check(item: GetID):
    status = await db.check_data(item.id)
    if status == "false":
        status = await db.load_data_users(item.id)

    if status == "ok":
        status = "false"

    return {"data": status}

@app.post("/add_user_data")
async def check_data(item: Dict):
    temp = api.log_in(item)

    if "status" in temp:
        return {"data": "error"}
    else:
        status = await db.add_data_users(list(item.values()))

    return {"data": temp["access_token"]}



@app.get("/random_quetions")
async def random_quetions():
    status = await db.random_quetions()
    return {"data": status}


# -----API-----

@app.post("/log_in")
async def log_in(item: Dict):
    data = await api.log_in(item)
    return data






if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)