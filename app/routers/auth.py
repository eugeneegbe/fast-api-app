from fastapi import APIRouter, Depends, HTTPException, status
from models.user import User, UserCreate
from utils.auth import create_access_token, verify_password

router = APIRouter()

@router.post("/signup")
def signup(user: UserCreate):
    print(**user.dict())
    # Create a new user
    db_user = User(**user.dict())
    # Save the user to the database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Generate an access token
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token}


@router.post("/login")
def login(user: UserCreate):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token}
