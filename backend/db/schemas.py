
"""
Schemas:
Data class used for input/output validation in FastAPI

Used for...
- API request validation
- API response formatting
"""


from pydantic import BaseModel


class RegisterUser(BaseModel):
    username: str
    password: str


class CreateClimb(BaseModel):
    user_id: int
    name: str


# # ROUTES\


# app = FastAPI()


# @app.post("/register")
# def register_user(user: RegisterUser, db: Session = Depends(get_db)):
#     if db.query(User).filter_by(username=user.username).first():
#         raise HTTPException(status_code=400, detail="Username already exists")

#     new_user = User(username=user.username, password=user.password)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return {"status": "registered", "user_id": new_user.id}


# @app.post("/create-climb")
# def create_climb(climb: CreateClimb, db: Session = Depends(get_db)):
#     user = db.query(User).filter_by(id=climb.user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     new_climb = MyClimb(name=climb.name, user_id=user.id)
#     db.add(new_climb)
#     db.commit()
#     return {"status": "climb created", "climb_id": new_climb.id}
