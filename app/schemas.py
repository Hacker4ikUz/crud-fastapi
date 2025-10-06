from pydantic import BaseModel, Field



class BaseUser(BaseModel):
    name: str
    password: str


class CreateUser(BaseUser):
    ...


class UpdateUser(BaseModel):
    name: str | None = Field(None, max_length=16)
    password: str | None = Field(None)


class User(BaseUser):
    id: int

    class Config:
        from_attributes = True


class PublicUser(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
