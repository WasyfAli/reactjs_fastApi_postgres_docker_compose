from pydantic import BaseModel

class StudentCreate(BaseModel):
    name: str
    email: str

class StudentOut(StudentCreate):
    id: int

    class Config:
        orm_mode = True
