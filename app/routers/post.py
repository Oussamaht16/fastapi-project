from typing import List, Optional
from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import func  # hadi hia count


# hada l code , """ user_id: int = Depends(oauth2.get_current_user) """ ki thato dakhal function lkhasa b request ihatam elik lazm tkon login bch ymchilk request sinon yaetik unauthorized trfad tokan o bch trfad token lazam user name o password ikono kif kif mea li rahom dakhal database


router = APIRouter(prefix="/posts", tags=["posts"])
# prefix drnah bch n9so kol khtra nktbo posts


# dok rah n3awdo les request tawaena malawal
# get posts
@router.get(
    "/",
    response_model=List[
        schemas.PostVote
    ],  # response_model is used to validate the response data
)
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    # limit : int = 10,  # this is used to limit the number of posts returned
    """posts = (
        db.query(models.Post)
        .filter(
            models.Post.owner_id == current_user.id,
            models.Post.title.ilike(f"%{search}%"),
        )
        .limit(limit)
        .offset(skip)
        .all()
        # ilike is used for case-insensitive search
        # contains is used for case-sensitive search contains(search)
    )"""  # get all posts for the current user

    # contains kili darna == search bch n9drou ndirou search fi title

    # hada l query li rah ya3tina votes ta3 kol post
    results = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .filter(models.Post.title.ilike(f"%{search}%"))
        .group_by(models.Post.id)
        .limit(limit)
        .offset(skip)
        .all()
    )
    # print(results)

    return results


# post a post
# hna zadna response_model f dectinnary bach nthakmo fi wach iwali baed request
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """new_post = models.Post(
        title=post.title, content=post.content, published=post.published
    )"""
    # had star bch 3indama ay ahad yosajil dokhol bi hisabih mobacharata yakon ladayh lha9 fi request
    new_post = models.Post(
        owner_id=current_user.id, **post.dict()
    )  # ** for unpack the dictionary
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# apres hada ga3 bch tbeat post la database lazm tafth header
# Authorization = Bearer(space) then paste the token you got from the /login endpoint
# wala troh auth then bearer then paste your token


# get a post by id
@router.get("/{id}", response_model=schemas.PostVote)
def get_post_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .filter(models.Post.id == id)
        .group_by(models.Post.id)
        .first()
    )

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found",
        )

    return post


# delete a post by id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found",
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    # delete.post(synchronize_session=False) # this is for async
    # but we are not using async so we can use this
    db.delete(post)
    # post_query.delete(synchronize_session=False)  # this is for sync
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update a post by id
@router.put("/{id}")
def update_post(
    id: int,
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    existing_post = post_query.first()

    if existing_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found",
        )

    if existing_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    post_query.update(post.dict(), synchronize_session=False)

    db.commit()
    return post_query.first()


# madamak ktabt current_user: int = Depends(oauth2.get_current_user) dakhal l function lokn ma dakhalch token request taek mata3tik hata resultat
