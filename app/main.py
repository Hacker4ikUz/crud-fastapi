from fastapi import FastAPI, Depends, HTTPException
import uvicorn
from contextlib import asynccontextmanager
from . import schemas, crud, database
from .deps import get_db



@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.init_models()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/users", response_model=schemas.User)
async def create_user(schema: schemas.CreateUser, db=Depends(get_db)):
    return await crud.create_user(db, schema)


@app.get("/users", response_model=list[schemas.PublicUser])
async def get_users(db=Depends(get_db)) -> list[schemas.User]:
    return await crud.get_users(db)


@app.get("/users/{id}", response_model=schemas.PublicUser)
async def get_user(id: int, db=Depends(get_db)) -> schemas.User:
    user = await crud.get_user(db, id)
    if not user:
        raise HTTPException(404, "User not found")
    return user


@app.put("/users/{id}", response_model=schemas.User)
async def update_user(id: int, data: schemas.UpdateUser, db=Depends(get_db)) -> schemas.User:
    user = await crud.update_user(db, id, data.name, data.password)
    if not user:
        raise HTTPException(404, "User not found")
    return user


@app.delete("/users/{id}", response_model=schemas.User)
async def delete_user(id: int, db=Depends(get_db)):
    user = await crud.delete_user(db, id)
    if not user:
        raise HTTPException(404, "User not found")

    return user




if __name__ == "__main__":
    uvicorn.run("app.main:app", port=8080, reload=True)