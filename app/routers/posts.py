from typing import List
from fastapi import status, HTTPException, Depends, Response, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models, database, oauth2


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=List[schemas.PostResponse]
)
async def get_posts(db: Session = Depends(database.get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
async def set_post(
    post: schemas.PostCreate,
    db: Session = Depends(database.get_db),
    user_id: int = Depends(oauth2.get_current_user),
):
    new_post = models.Post(**post.model_dump())
    new_post.owner_id = user_id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get(
    "/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse
)
async def get_post(id: int, db: Session = Depends(database.get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found!",
        )
    else:
        return post


@router.put(
    "/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse
)
async def update_post(
    id: int,
    updated_post: schemas.PostUpdate,
    db: Session = Depends(database.get_db),
    user_id: int = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found!",
        )
    elif user_id != post.first().owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You can update only your posts",
        )
    else:
        post.update(updated_post.model_dump(), synchronize_session=False)
        db.commit()
        return post.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    id: int,
    db: Session = Depends(database.get_db),
    user_id: int = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found!",
        )
    elif user_id != post.first().owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You can delete only your posts",
        )
    else:
        post.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
