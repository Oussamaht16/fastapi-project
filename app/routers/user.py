from typing import List
from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/",
    response_model=List[
        schemas.User
    ],  # response_model is used to validate the response data
)
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.Users).all()
    return users


# post a user data
# hna zadna response_model f dectinnary bach nthakmo fi wach iwali baed request
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserIn, db: Session = Depends(get_db)):
    """# hash the password before saving it to the database
    hashed_password = pwd_context.hash(user.password)
    # create a new user object with the hashed password
    user.password = hashed_password  # replace the password with the hashed password
    # hadi tari9a fi halat makach utils"""

    hash_password = utils.hash_password(user.password)
    user.password = hash_password

    new_user = models.Users(**user.dict())  # ** for unpack the dictionary
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# get a user data by id
@router.get("/{id}", response_model=schemas.User)
def get_userdata_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id {id} not found",
        )
    return user


# delete a user by id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id {id} not found",
        )
    # delete.post(synchronize_session=False) # this is for async
    # but we are not using async so we can use this
    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update a user by id
@router.put("/{id}", response_model=schemas.User)
def update_user(id: int, user: schemas.UserIn, db: Session = Depends(get_db)):
    user_query = db.query(models.Users).filter(models.Users.id == id)
    existing_user = user_query.first()

    if existing_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found",
        )

    user_query.update(user.dict(), synchronize_session=False)

    db.commit()
    return user_query.first()
