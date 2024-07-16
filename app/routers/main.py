from fastapi import APIRouter


router = APIRouter()


@router.get("/")
def welcome():
    return {"Messae": "Lucid Dreams Fast API"}