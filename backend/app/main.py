from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, database, schemas
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)

# CORS for React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/students", response_model=schemas.StudentOut)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.get("/students", response_model=list[schemas.StudentOut])
def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()
