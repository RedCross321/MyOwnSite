# from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine, get_db
from fastapi import Depends, FastAPI, HTTPException, status
from models import User
from schemas import UserCreate, UserRead
from security import get_password_hash
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )


@app.get("/health")
def root():
    return {"status": "ok"}


@app.get("/api")
def api_greeting():
    return {"text": "Первая рабочая страница"}


@app.post("/api/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)) -> UserRead:
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже зарегистрирован.",
        )
    hashed_pwd = get_password_hash(user_in.password)
    new_user = User(email=user_in.email, password=hashed_pwd, is_active=True)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
