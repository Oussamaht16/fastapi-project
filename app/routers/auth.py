from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils, oauth2
from fastapi.security import OAuth2PasswordRequestForm


# had l fichier conqois login ha9i9i rah nhato email o password o nchofo ida y9bal wla lala


router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
# def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
# hadi la methode rah nastaghnaw eliha ba3d majabna mn fast apisecurity

# rana badalna library dok ki ndiro request mnkhaznoch f body
# wa lakin nkhazno fi form data


def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):

    user = (
        db.query(models.Users)
        .filter(
            models.Users.email == user_credentials.username
        )  # OAuth2PasswordRequestForm uses 'username' for email
        .first()
    )
    """ user = (
        db.query(models.Users)
        .filter(
            models.Users.email == user_credentials.email
        )  
        .first()
    ) """

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid credentials"
        )
    if utils.verify_password(user_credentials.password, user.password) is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid credentials"
        )

    # create a token
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    # return the token
    return {"access_token": access_token, "token_type": "bearer"}
