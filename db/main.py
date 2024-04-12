from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
import db

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

